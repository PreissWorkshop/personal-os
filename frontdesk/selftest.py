"""Offline self-test - everything that can be checked without a network.

    python -m frontdesk.selftest

It uses a throwaway state directory, so it never touches the live database,
and it makes no Telegram or model call. What it cannot prove is the two live
legs: the API key and the bot token. Those are checked by starting the front
desk, and the log says plainly whether each one is present.
"""

from __future__ import annotations

import sys
import tempfile
import time
from pathlib import Path

from . import config

PASS, FAIL = [], []


def check(name: str, condition: bool, detail: str = "") -> None:
    (PASS if condition else FAIL).append(name)
    mark = "ok  " if condition else "FAIL"
    print(f"  {mark} {name}" + (f"  - {detail}" if detail and not condition else ""))


def main() -> int:
    sandbox = Path(tempfile.mkdtemp(prefix="frontdesk-selftest-"))
    config.STATE_DIR = sandbox
    config.DB_PATH = sandbox / "test.db"
    config.WORK_DIR = sandbox / "work"
    config.TASK_LOG_DIR = sandbox / "tasks"
    config.ENV_FILE = sandbox / ".env"

    from . import digest, employee, scheduler, state, telegram, tools, voice, webhook

    print("config")
    crlf = "# comment\r\nTELEGRAM_BOT_TOKEN=\"123456:abc\"\r\n\r\nFOO=bar\r\n"
    parsed = config._parse_env(crlf)
    check("CRLF and quotes parse", parsed.get("TELEGRAM_BOT_TOKEN") == "123456:abc",
          repr(parsed))
    check("comments and blanks skipped", parsed.get("FOO") == "bar" and len(parsed) == 2,
          repr(parsed))

    print("\nstate")
    state._conn = None
    state.connect()
    task_id = state.create_task("do a thing")
    state.start_task(task_id, str(sandbox / "log.txt"))
    check("task starts running", state.get_task(task_id)["status"] == "running")
    check("open_tasks sees it", any(r["id"] == task_id for r in state.open_tasks()))
    state.finish_task(task_id, "done", "five line report")
    check("task finishes", state.get_task(task_id)["status"] == "done")
    check("finished job is unreported", any(r["id"] == task_id
                                           for r in state.unreported_finished()))
    state.mark_reported(task_id)
    check("marking reported clears it", not state.unreported_finished())

    state.remember("Kokoro voice", "bm_george at 1.2x")
    check("fact stored and found", bool(state.search_facts("kokoro")))
    state.remember("Kokoro voice", "changed")
    check("fact overwrites, not duplicates",
          len([r for r in state.all_facts() if r["key"] == "kokoro voice"]) == 1)

    reminder_id = state.add_reminder(time.time() - 5, "call the supplier")
    check("due reminder is due", any(r["id"] == reminder_id
                                     for r in state.due_reminders(time.time())))
    state.mark_reminder_sent(reminder_id)
    check("sent reminder stops being due", not state.due_reminders(time.time()))

    state.enqueue_push("hello")
    pushes = state.pending_pushes()
    check("outbox queues", len(pushes) == 1 and pushes[0]["text"] == "hello")
    state.mark_push_sent(pushes[0]["id"])
    check("outbox drains", not state.pending_pushes())

    state.set_meta("update_offset", "42")
    check("meta round-trips", state.get_meta("update_offset") == "42")

    print("\nconversation history (Messages API rules)")
    state._run("DELETE FROM messages")
    state.add_message("assistant", "morning brief")      # a push, before he speaks
    state.add_message("assistant", "job #1 finished")    # a second push
    state.add_message("user", "what was that?")
    state.add_message("assistant", "job 1 was the suite")
    state.add_message("user", "and now?")
    history = state.recent_messages(20)
    check("history starts with a user message",
          history and history[0]["role"] == "user", repr(history))
    check("no two consecutive rows share a role",
          all(history[i]["role"] != history[i + 1]["role"]
              for i in range(len(history) - 1)), repr(history))
    check("leading pushes are dropped, not reordered",
          "morning brief" not in " ".join(m["content"] for m in history), repr(history))
    state._run("DELETE FROM messages")
    state.add_message("user", "one")
    state.add_message("user", "two")
    merged = state.recent_messages(20)
    check("a run of the same role merges into one message",
          len(merged) == 1 and merged[0]["content"] == "one\ntwo", repr(merged))
    state.add_message("assistant", "   ")
    check("an empty message is skipped", len(state.recent_messages(20)) == 1)
    state._run("DELETE FROM messages")

    print("\ntime parsing")
    now = time.time()
    due, human = tools.parse_when("in 25 minutes")
    check("'in 25 minutes'", due is not None and 1490 < due - now < 1510, human)
    due, _ = tools.parse_when("in 3 hours")
    check("'in 3 hours'", due is not None and 10790 < due - now < 10810)
    due, _ = tools.parse_when("2 days")
    check("'2 days' without 'in'", due is not None and 172700 < due - now < 172900)
    due, _ = tools.parse_when("tomorrow 08:30")
    check("'tomorrow 08:30' is in the future", due is not None and due > now)
    due, _ = tools.parse_when("2026-12-24T09:00:00Z")
    check("ISO timestamp", due is not None)
    due, reason = tools.parse_when("sometime after lunch")
    check("unreadable time is refused, not guessed", due is None, reason)
    due, reason = tools.parse_when("")
    check("empty time is refused", due is None)

    print("\ndigest")
    text = digest.get(force=True)
    check("digest builds from the real repo", len(text) > 200, f"{len(text)} chars")
    check("digest respects its cap", len(text) <= digest.MAX_CHARS + 32,
          f"{len(text)} chars")
    check("digest names the machines", "PREISSWORKSHOP" in text or "main-pc" in text)
    check("digest carries the gates", "Shipping HelmCNC" in text
          and "Spending money" in text)
    check("digest lists the cloud routines", "weekday standup" in text)
    check("no folded-scalar status leaks in", "[>]" not in text and "[|]" not in text)
    check("no done item is listed as open",
          "\u2705" not in text.split("OPEN ITEMS", 1)[-1].split("NEEDS TENIS", 1)[0])
    check("open items are whole sentences, not fragments",
          "Legend:" not in text)
    check("digest quotes no secret-looking value",
          "ANTHROPIC_API_KEY=" not in text and "bot" + "Token" not in text)
    cached = digest.get()
    check("digest caches on mtime", cached is text or cached == text)

    print("\nbullet reconstruction")
    sample = ("## Heading\n\n"
              "- \U0001f512 **A locked item** that wraps over\n"
              "  two lines and keeps going\n"
              "- \u2705 A done item mentioning a \U0001f512 lock later on\n"
              "- \u23f3 An item in progress\n")
    bullets = digest._bullets(sample)
    check("a wrapped bullet is reassembled whole",
          any("two lines and keeps going" in b and "A locked item" in b for b in bullets),
          repr(bullets))
    check("three bullets found, heading excluded", len(bullets) == 3, repr(bullets))

    print("\nregistry lookup")
    check("unknown project falls back to personal-os",
          employee.project_root("no-such-project") == config.REPO_ROOT)
    check("personal-os resolves", employee.project_root(None) == config.REPO_ROOT)
    check("a registry id resolves to a path",
          isinstance(employee.project_root("helm-cnc"), Path))

    print("\nmessage shaping")
    long_text = "\n".join(f"line {i} of a report that will not fit" for i in range(400))
    chunks = telegram._split(long_text, 3900)
    check("long text splits", len(chunks) > 1)
    check("every chunk is inside Telegram's cap", all(len(c) <= 3900 for c in chunks))
    check("splitting loses nothing", "".join(chunks) == long_text)
    check("one unbroken 9000-char line still splits",
          all(len(c) <= 3900 for c in telegram._split("x" * 9000, 3900)))

    five = scheduler._five_lines("a\nb\nc\nd\ne\nf\ng")
    check("report is cut to five lines", five.count("\n") == 5 and "(+2 more" in five)
    check("a short report is untouched", scheduler._five_lines("a\nb") == "a\nb")

    print("\ninbound events")
    fire = webhook._format({"camera_name": "Shop", "kind": "fire",
                            "started_at": 1758200000, "zones": "bench"})
    check("NVR fire event is unmistakable", "POSSIBLE FIRE" in fire and "Shop" in fire)
    check("fire event carries its caveat", "not a smoke alarm" in fire)
    person = webhook._format({"camera": "Shop", "kind": "person"})
    check("NVR person event", person.startswith("Person"))
    check("plain text event", webhook._format({"text": "CI failed", "source": "gh"})
          == "[gh] CI failed")
    check("unknown shape still delivers", "Event:" in webhook._format({"a": 1}))

    print("\nvoice and worker (reported, not required on this machine)")
    print(f"  --   STT/TTS venv: {'present' if voice.available() else 'absent'}"
          f" ({config.STT_VENV_PYTHON})")
    print(f"  --   worker CLI:   {employee.claude_binary() or 'not found'}")
    check("Icelandic text is not spoken by an English voice",
          voice._looks_icelandic("Sæll, þetta er prófun"))
    check("English text is speakable", not voice._looks_icelandic("Hello, this is a test"))


    print("\nturn loop (stubbed model - the live API leg is not tested here)")
    _turn_loop(check)

    print(f"\n{len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        print("failed: " + ", ".join(FAIL))
    return 1 if FAIL else 0



class _Block:
    """Minimal stand-in for a content block from the SDK."""

    def __init__(self, type_, text=None, name=None, input_=None, id_=None):
        self.type = type_
        self.text = text
        self.name = name
        self.input = input_ or {}
        self.id = id_ or "tu_1"


class _Response:
    def __init__(self, content, stop_reason="end_turn"):
        self.content = content
        self.stop_reason = stop_reason
        self.usage = None


class _StubClient:
    """Replays a scripted list of responses and records the models asked for."""

    def __init__(self, script):
        self.script = list(script)
        self.models = []
        self.systems = []
        self.messages = self

    def create(self, **kwargs):
        self.models.append(kwargs.get("model"))
        self.systems.append(kwargs.get("system"))
        return self.script.pop(0)


def _turn_loop(check) -> None:
    from . import brain as brain_mod
    from . import config, employee, state

    # Never actually start a Claude Code session from the self-test.
    dispatched = []
    original = employee.delegate
    employee.delegate = lambda job, project=None: (dispatched.append((job, project))
                                                   or state.create_task(job))
    try:
        brain = brain_mod.Brain.__new__(brain_mod.Brain)

        # 1. a plain answer, no tools
        brain.client = _StubClient([_Response([_Block("text", text="Two jobs open.")])])
        sent = []
        answer = brain.respond("what is open?", sent.append)
        check("a plain answer comes straight back", answer == "Two jobs open.", answer)
        check("a plain answer sends nothing early", sent == [], repr(sent))

        system = brain.client.systems[0]
        check("system prompt is three blocks", len(system) == 3, str(len(system)))
        check("identity block is cached",
              system[0].get("cache_control", {}).get("type") == "ephemeral")
        check("digest block is cached",
              system[1].get("cache_control", {}).get("type") == "ephemeral")
        check("volatile block is NOT cached", "cache_control" not in system[2])
        check("volatile block carries the clock", "Right now:" in system[2]["text"])

        # 2. delegate: the acknowledgement must land before the turn finishes
        brain.client = _StubClient([
            _Response([_Block("tool_use", name="delegate", id_="tu_a",
                              input_={"job": "run the ScanPen suite",
                                      "reply": "On it - running the ScanPen suite.",
                                      "project": "scan-pen"})],
                      stop_reason="tool_use"),
            _Response([_Block("text", text="Dispatched. I will push the result.")]),
        ])
        sent = []
        answer = brain.respond("run the scanpen suite", sent.append)
        check("delegate acknowledges immediately",
              sent == ["On it - running the ScanPen suite."], repr(sent))
        check("delegate actually dispatched",
              dispatched and dispatched[-1][0] == "run the ScanPen suite", repr(dispatched))
        check("delegate passes the project", dispatched[-1][1] == "scan-pen")
        check("the turn still returns a final line",
              "Dispatched" in answer, answer)
        check("delegate stays on the fast model",
              brain.client.models == [config.FAST_MODEL] * 2, repr(brain.client.models))

        # 3. escalate: the second round must use the stronger model
        brain.client = _StubClient([
            _Response([_Block("tool_use", name="escalate", id_="tu_b",
                              input_={"question": "H.264 or H.265 for the shop camera?"})],
                      stop_reason="tool_use"),
            _Response([_Block("text", text="H.264. Browsers will not play HEVC.")]),
        ])
        sent = []
        answer = brain.respond("which codec?", sent.append)
        check("escalation switches to the stronger model",
              brain.client.models == [config.FAST_MODEL, config.SMART_MODEL],
              repr(brain.client.models))
        check("escalated answer is returned", "H.264" in answer, answer)

        # 4. a tool that throws must not take the turn down
        def _boom(*_a, **_k):
            raise RuntimeError("disk on fire")

        brain.client = _StubClient([
            _Response([_Block("tool_use", name="task_status", id_="tu_c", input_={})],
                      stop_reason="tool_use"),
            _Response([_Block("text", text="Could not read the job list.")]),
        ])
        import logging

        import frontdesk.tools as tools_mod
        saved = tools_mod.run
        tools_mod.run = _boom
        # The traceback below is the point of the test; do not print it.
        logging.disable(logging.CRITICAL)
        try:
            answer = brain.respond("what is running?", [].append)
        finally:
            logging.disable(logging.NOTSET)
            tools_mod.run = saved
        check("a throwing tool degrades into an answer",
              "Could not read" in answer, answer)

        # 5. an unreadable reminder time must refuse, not guess
        result = tools_mod.run("remind", {"when": "later on", "what": "x",
                                          "reply": "ok"}, [].append)
        check("a vague reminder time is refused", "Could not read" in result, result)
        check("refusing a reminder stores nothing",
              not any(r["text"] == "x" for r in state.pending_reminders()))
    finally:
        employee.delegate = original


if __name__ == "__main__":
    raise SystemExit(main())
