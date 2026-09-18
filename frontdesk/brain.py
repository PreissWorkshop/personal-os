"""The fast model - the front desk's own head.

Non-streaming on purpose: Telegram delivers a message, not a stream, so
streaming would buy latency nowhere and cost complexity. What does buy
latency: a small tool set, a hard cap on output tokens, a short history, and
a cached system prompt. The identity block and the digest are marked
cache_control=ephemeral, so after the first call of the hour the whole
world-view is a cache read rather than thousands of fresh input tokens.
"""

from __future__ import annotations

import datetime as dt
import logging
import time

import anthropic

from . import config, digest, state, tools

log = logging.getLogger("frontdesk.brain")

IDENTITY = """You are the front desk of Preiss Workshop - Tenis Preiss's
first point of contact, reached from his phone over Telegram.

There are two of you. You are the fast one: you answer in about a second, you
know the shape of the whole operation, and you hold the phone. The employee is
a Claude Code session on main-pc that does the actual work - files, repos,
builds, suites, pushes. You hand work to it with `delegate` and it reports
back through you. You never do that work yourself and you have no way to.

HOW YOU ANSWER
- At most five lines. The phone gets the headline and the decision needed;
  detail belongs in the repo. This is a standing rule, not a style note.
- Lead with the answer or the blocker. No preamble, no restating his question,
  no praise, no filler.
- If you know it, say it. If you do not, say you do not - then delegate, or
  say what it would take to find out. Never guess at a fact, a price, a date,
  a stock figure, a test result or a file's contents.
- Mark anything you are inferring rather than reporting. If a number or a
  claim is unverified, say so in the same breath.
- Answer in the language he writes in. English by default; natural modern
  Icelandic if he writes Icelandic.
- Plain text only. No markdown - it renders as literal asterisks on a phone.

WHEN TO DELEGATE
Delegate the moment an answer needs something you cannot see: a file, a repo,
a build, a suite, a push, a GitHub issue, real research, anything on disk.
Delegate first and reply in the same turn - the `reply` field reaches him
before the job starts. Do not describe what you are about to delegate and
then not delegate it.
Answer directly when it is about state you already hold: what is running,
what is open, what he told you, what the digest says, or a judgement he wants
in a sentence. Use `escalate` for a real trade-off or a technical answer where
being wrong costs money or a client.

THE OPERATION
Two brands, and their tone is protected. Preiss Workshop: premium interiors,
carpentry, CNC, signage, custom fabrication - precision, craftsmanship,
reliability, never cheap or casual. Studio Esja: premium handmade ceramics,
Japanese craft and Icelandic nature - calm, artistic, grounded in real
craftsmanship, never exaggerated or mass-produced. HelmCNC is the shipping
CNC product; ScanPen is the probe project.

HARD RULES YOU DO NOT BEND
- No secrets, ever. Never repeat a token, key or password, and never ask him
  to send one over Telegram. Locations may be named; contents may not.
- A missed threshold is reported, never loosened.
- Never claim something was done, verified, tested or pushed unless a job
  reported it. You did not see it - the worker did or it did not happen.
- Machine roles are law: cnc-pc at the CNC is a HelmCNC appliance, no installs
  and no heavy data; main-pc and the laptop are for development.
- Destructive work, shipping HelmCNC, merging the website to main, touching
  production, spending money and publishing all need his explicit OK. Say so
  and stop; do not dispatch it.
"""


class Brain:
    def __init__(self, api_key: str) -> None:
        self.client = anthropic.Anthropic(api_key=api_key, max_retries=2, timeout=60.0)

    # --- prompt -----------------------------------------------------------
    def _system(self) -> list[dict]:
        """Two cached blocks then one volatile block. Order matters: a cache
        breakpoint only helps what sits before it."""
        return [
            {"type": "text", "text": IDENTITY,
             "cache_control": {"type": "ephemeral"}},
            {"type": "text",
             "text": "THE OPERATION AS IT STANDS (condensed from personal-os; "
                     "it is the source of truth, this is a digest of it)\n\n" + digest.get(),
             "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": self._volatile()},
        ]

    def _volatile(self) -> str:
        now = dt.datetime.now(dt.timezone.utc)
        lines = [f"Right now: {now.strftime('%A %d %B %Y, %H:%M')} Iceland time "
                 f"(Iceland is UTC all year)."]

        running = state.open_tasks()
        if running:
            lines.append("Jobs in flight:")
            for row in running:
                age = int((time.time() - (row["started_at"] or row["created_at"])) / 60)
                lines.append(f"  #{row['id']} {row['status']} {age}m - "
                             f"{' '.join(row['request'].split())[:110]}")
        else:
            lines.append("No jobs in flight.")

        pending = state.pending_reminders()
        if pending:
            lines.append("Reminders set:")
            for row in pending[:6]:
                when = dt.datetime.fromtimestamp(row["due_at"], dt.timezone.utc)
                lines.append(f"  {when.strftime('%a %d %b %H:%M')} - {row['text'][:90]}")

        facts = state.all_facts()
        if facts:
            lines.append("What you have been told to remember:")
            for row in facts[:25]:
                lines.append(f"  {row['key']}: {row['value'][:140]}")

        return "\n".join(lines)

    # --- the turn ---------------------------------------------------------
    def respond(self, user_text: str, send_now) -> str:
        """One turn. Returns the text to send; `send_now` is for lines that
        must not wait for the turn to finish."""
        history = state.recent_messages(config.HISTORY_TURNS)
        messages = history + [{"role": "user", "content": user_text}]
        model = config.FAST_MODEL
        collected: list[str] = []

        for round_index in range(config.MAX_TOOL_ROUNDS):
            started = time.time()
            try:
                response = self.client.messages.create(
                    model=model,
                    max_tokens=900,
                    system=self._system(),
                    tools=tools.SCHEMA,
                    messages=messages,
                )
            except anthropic.APIStatusError as exc:
                log.error("model call failed: %s", exc)
                return (f"I could not reach the model ({exc.status_code}). "
                        f"Nothing was dispatched - say it again in a moment.")
            except Exception as exc:  # noqa: BLE001
                log.exception("model call failed")
                return f"I could not reach the model ({type(exc).__name__}). Nothing was dispatched."

            usage = getattr(response, "usage", None)
            log.info("round %d on %s in %.2fs (in=%s cache_read=%s out=%s)",
                     round_index, model, time.time() - started,
                     getattr(usage, "input_tokens", "?"),
                     getattr(usage, "cache_read_input_tokens", "?"),
                     getattr(usage, "output_tokens", "?"))

            text_parts = [b.text for b in response.content if b.type == "text"]
            calls = [b for b in response.content if b.type == "tool_use"]
            if text_parts:
                collected.append("\n".join(t.strip() for t in text_parts if t.strip()))

            if response.stop_reason != "tool_use" or not calls:
                break

            messages.append({"role": "assistant", "content": response.content})
            results = []
            escalate_question = None
            for call in calls:
                try:
                    outcome = tools.run(call.name, call.input or {}, send_now)
                except Exception as exc:  # noqa: BLE001 - a broken tool is a message, not a crash
                    log.exception("tool %s failed", call.name)
                    outcome = f"Tool {call.name} failed: {type(exc).__name__}: {exc}"
                if outcome == "__ESCALATE__":
                    escalate_question = (call.input or {}).get("question") or user_text
                    outcome = "Thinking harder about it now."
                results.append({"type": "tool_result", "tool_use_id": call.id,
                                "content": outcome})
            messages.append({"role": "user", "content": results})

            if escalate_question:
                model = config.SMART_MODEL
                log.info("escalating to %s", model)

        answer = "\n".join(part for part in collected if part.strip()).strip()
        return answer or "Done."

    # --- proactive --------------------------------------------------------
    def compose(self, instruction: str) -> str:
        """A one-shot with no tools and no history - the morning brief, a task
        report, a webhook alert turned into a sentence."""
        try:
            response = self.client.messages.create(
                model=config.FAST_MODEL,
                max_tokens=600,
                system=self._system(),
                messages=[{"role": "user", "content": instruction}],
            )
        except Exception as exc:  # noqa: BLE001
            log.warning("compose failed: %s", exc)
            return ""
        return "\n".join(b.text.strip() for b in response.content if b.type == "text").strip()
