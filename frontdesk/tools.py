"""The front desk's tools - deliberately few, and none of them dangerous.

The front desk has no shell, no file write, no git and no network beyond
Telegram and the model. Everything that can change the world goes through
`delegate`, which starts a Claude Code session under the auto-mode safety
classifier and docs/employee.md's gates. That is the security property: a
fast model on an open chat channel cannot do damage directly.

`delegate` and `remind` each carry a `reply` field. The front desk sends that
line the instant the tool call arrives, so an acknowledgement never waits on
a second model round trip. That single detail is most of what makes this feel
instant rather than merely quick.
"""

from __future__ import annotations

import datetime as dt
import logging
import re
import time

from . import employee, state

log = logging.getLogger("frontdesk.tools")

SCHEMA = [
    {
        "name": "delegate",
        "description": (
            "Hand a job to a worker session on main-pc. Use this for anything "
            "needing files, a repo, a build, a test suite, research or a push - "
            "i.e. anything you cannot answer from what you already know. "
            "Returns at once; the result is pushed to Tenis when the job "
            "finishes, so do not wait for it and do not promise a timescale you "
            "cannot know."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "job": {
                    "type": "string",
                    "description": (
                        "The complete instruction for the worker. It starts with "
                        "no context beyond docs/employee.md, so name the project, "
                        "the files and the expected outcome explicitly."
                    ),
                },
                "reply": {
                    "type": "string",
                    "description": (
                        "One short line sent to Tenis immediately, before the job "
                        "runs. Say what was dispatched. Never invent a duration."
                    ),
                },
                "project": {
                    "type": "string",
                    "description": (
                        "Project id from the registry the job should be rooted in: "
                        "personal-os, helm-cnc, scan-pen, preiss-website, "
                        "claude-system. Omit for personal-os."
                    ),
                },
            },
            "required": ["job", "reply"],
        },
    },
    {
        "name": "task_status",
        "description": "What has been dispatched recently and how it went. Use when Tenis asks what is running or what happened to a job.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "remind",
        "description": (
            "Set a reminder that pushes to Tenis's phone at a given time. This is "
            "the front desk speaking first, which nothing else in the operation "
            "does - use it whenever he says 'remind me' or names a deadline."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "when": {
                    "type": "string",
                    "description": (
                        "'in 25 minutes', 'in 3 hours', 'in 2 days', 'tomorrow "
                        "08:30', '17:00', or an ISO timestamp. Times are Iceland "
                        "time, which is UTC all year."
                    ),
                },
                "what": {"type": "string", "description": "The reminder text, as he should read it later."},
                "reply": {"type": "string", "description": "One short line confirming it, sent immediately."},
            },
            "required": ["when", "what", "reply"],
        },
    },
    {
        "name": "remember",
        "description": "Store a durable fact about the operation, a preference or a decision, so later messages and reminders can use it. Short key, short value.",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string"},
                "value": {"type": "string"},
            },
            "required": ["key", "value"],
        },
    },
    {
        "name": "recall",
        "description": "Search the stored facts. Use before saying you do not know something.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "escalate",
        "description": (
            "Re-answer this question with the slower, stronger model - still in "
            "the chat, still seconds. Use for a real judgement call, a trade-off, "
            "or a technical answer where being wrong costs money or a client. Do "
            "not use it for work that needs files: that is delegate."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The question to think harder about, restated in full."},
            },
            "required": ["question"],
        },
    },
]


class Immediate(Exception):
    """Carries a line to send to Tenis before the model's turn completes."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.text = text


def run(name: str, args: dict, send_now) -> str:
    """Execute a tool. `send_now(text)` pushes a line to the phone at once."""
    if name == "delegate":
        reply = (args.get("reply") or "").strip()
        if reply:
            send_now(reply)
        task_id = employee.delegate(args.get("job", ""), args.get("project"))
        return (f"Dispatched as job #{task_id}. It runs in the background; its report "
                f"is pushed to Tenis automatically. Do not restate the reply.")

    if name == "task_status":
        return employee.summary()

    if name == "remind":
        due, human = parse_when(args.get("when", ""))
        if due is None:
            return (f"Could not read the time {args.get('when')!r}. Ask Tenis for a "
                    f"clearer one - do not guess a time for a reminder.")
        reminder_id = state.add_reminder(due, args.get("what", "").strip())
        reply = (args.get("reply") or "").strip()
        if reply:
            send_now(reply)
        return f"Reminder #{reminder_id} set for {human}. Do not restate the reply."

    if name == "remember":
        state.remember(args.get("key", ""), args.get("value", ""))
        return "Stored."

    if name == "recall":
        rows = state.search_facts(args.get("query", ""))
        if not rows:
            return "Nothing stored on that."
        return "\n".join(f"{r['key']}: {r['value']}" for r in rows)

    if name == "escalate":
        return "__ESCALATE__"

    return f"Unknown tool {name!r}."


_REL = re.compile(
    r"^\s*(?:in\s+)?(?P<n>\d+(?:\.\d+)?)\s*"
    r"(?P<unit>min|mins|minute|minutes|m|h|hr|hrs|hour|hours|d|day|days|w|week|weeks)\b",
    re.I,
)
_UNIT_SECONDS = {
    "m": 60, "min": 60, "mins": 60, "minute": 60, "minutes": 60,
    "h": 3600, "hr": 3600, "hrs": 3600, "hour": 3600, "hours": 3600,
    "d": 86400, "day": 86400, "days": 86400,
    "w": 604800, "week": 604800, "weeks": 604800,
}
_CLOCK = re.compile(r"^\s*(?P<day>today|tomorrow|tmr)?\s*(?:at\s+)?"
                    r"(?P<h>[01]?\d|2[0-3])[:.](?P<m>[0-5]\d)\s*$", re.I)


def parse_when(text: str) -> tuple[float | None, str]:
    """Return (unix time, human string). (None, reason) if unreadable.

    Iceland keeps UTC all year, so local time needs no offset - the same
    assumption docs/agent-system.md makes for the cloud routines. A time that
    cannot be read is refused rather than guessed: a reminder at the wrong
    hour is worse than no reminder.
    """
    raw = (text or "").strip()
    if not raw:
        return None, "empty"

    match = _REL.match(raw)
    if match:
        seconds = float(match.group("n")) * _UNIT_SECONDS[match.group("unit").lower()]
        due = time.time() + seconds
        return due, _fmt(due)

    match = _CLOCK.match(raw)
    if match:
        now = dt.datetime.now(dt.timezone.utc)
        target = now.replace(hour=int(match.group("h")), minute=int(match.group("m")),
                             second=0, microsecond=0)
        day = (match.group("day") or "").lower()
        if day in ("tomorrow", "tmr"):
            target += dt.timedelta(days=1)
        elif target <= now:
            # A bare past time means the next one round.
            target += dt.timedelta(days=1)
        return target.timestamp(), _fmt(target.timestamp())

    try:
        parsed = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.timestamp(), _fmt(parsed.timestamp())
    except ValueError:
        return None, f"unreadable: {raw!r}"


def _fmt(when: float) -> str:
    stamp = dt.datetime.fromtimestamp(when, dt.timezone.utc)
    return stamp.strftime("%a %d %b %H:%M") + " (Iceland)"
