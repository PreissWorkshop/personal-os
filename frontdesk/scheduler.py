"""The proactive half - the front desk speaking first.

This is the part that does not exist today and that the Claude app cannot do
at all: something in the operation that opens the conversation. Reminders,
finished jobs, jobs that have gone quiet, and a morning brief.
"""

from __future__ import annotations

import datetime as dt
import logging
import threading
import time

from . import config, state, voice

log = logging.getLogger("frontdesk.scheduler")

BRIEF_INSTRUCTION = """Write Tenis's morning brief. At most five lines, plain
text, no markdown, no greeting and no padding.

Cover only what is real: the open LOCKED items that need him, anything a job
reported since yesterday, reminders due today, and the single thing most worth
his attention this morning. If a line would only restate that nothing has
changed, leave it out. If genuinely nothing needs attention, say exactly that
in one line - a quiet day is a valid brief and must not be inflated."""


class Scheduler(threading.Thread):
    def __init__(self, push, brain) -> None:
        super().__init__(name="scheduler", daemon=True)
        self.push = push
        self.brain = brain
        self._stop = threading.Event()

    def stop(self) -> None:
        self._stop.set()

    def run(self) -> None:
        log.info("scheduler up (tick %ss)", config.TICK_SECONDS)
        while not self._stop.is_set():
            try:
                self.tick()
            except Exception:  # noqa: BLE001 - a bad tick must not end the thread
                log.exception("tick failed")
            self._stop.wait(config.TICK_SECONDS)

    def tick(self) -> None:
        now = time.time()
        self._reminders(now)
        self._finished_jobs()
        self._silent_jobs(now)
        self._morning_brief()
        self._housekeeping()

    # --- reminders --------------------------------------------------------
    def _reminders(self, now: float) -> None:
        for row in state.due_reminders(now):
            self.push(f"Reminder: {row['text']}")
            state.mark_reminder_sent(row["id"])

    # --- delegated work ---------------------------------------------------
    def _finished_jobs(self) -> None:
        for row in state.unreported_finished():
            verdict = "finished" if row["status"] == "done" else "FAILED"
            took = ""
            if row["started_at"] and row["finished_at"]:
                took = f" in {int((row['finished_at'] - row['started_at']) / 60)}m"
            body = _five_lines(row["result"] or "(no report)")
            self.push(f"Job #{row['id']} {verdict}{took}.\n{body}")
            state.mark_reported(row["id"])

    def _silent_jobs(self, now: float) -> None:
        """A job that has said nothing for a long while gets one nudge, not a
        stream of them. Silence is the failure mode docs/employee.md calls out:
        never let a surprise land on Tenis late."""
        for row in state.open_tasks():
            started = row["started_at"] or row["created_at"]
            if now - started < config.SILENT_TASK_NUDGE or row["nudged_at"]:
                continue
            minutes = int((now - started) / 60)
            self.push(f"Job #{row['id']} has been running {minutes}m with nothing "
                      f"back yet: {' '.join(row['request'].split())[:90]}")
            state.mark_nudged(row["id"])

    # --- morning brief ----------------------------------------------------
    def _morning_brief(self) -> None:
        now = dt.datetime.now(dt.timezone.utc)
        if (now.hour, now.minute) < (config.BRIEF_HOUR, config.BRIEF_MINUTE):
            return
        today = now.strftime("%Y-%m-%d")
        if state.get_meta("last_brief") == today:
            return
        # Claim the day first: a crash mid-compose must not produce two briefs.
        state.set_meta("last_brief", today)
        text = self.brain.compose(BRIEF_INSTRUCTION) if self.brain else ""
        if text:
            self.push(text)
        else:
            log.warning("morning brief produced nothing; not sending an empty push")

    # --- housekeeping -----------------------------------------------------
    def _housekeeping(self) -> None:
        today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
        if state.get_meta("last_prune") == today:
            return
        state.set_meta("last_prune", today)
        removed = voice.prune()
        if removed:
            log.info("pruned %d old audio files", removed)


def _five_lines(text: str, limit: int = 5) -> str:
    """docs/employee.md: the phone gets at most five lines. The worker writes a
    five-line report, but a crash dump does not obey that, so enforce it."""
    lines = [line.rstrip() for line in text.strip().splitlines() if line.strip()]
    if len(lines) <= limit:
        return "\n".join(lines)
    return "\n".join(lines[:limit]) + f"\n(+{len(lines) - limit} more lines in the transcript)"
