"""The front desk: the loop that owns the phone.

    python -m frontdesk

One process, three threads and a poll:
  * the Telegram long-poll (this thread) - answers Tenis
  * a sender - drains the outbox, so a push never waits on a 50s poll
  * the scheduler - reminders, finished jobs, quiet jobs, the morning brief
  * the webhook listener - inbound events from the NVR, CI, anything

It holds no secrets in the repo and can change nothing on disk. Real work is
dispatched to a Claude Code session; see frontdesk/tools.py.
"""

from __future__ import annotations

import logging
import secrets
import signal
import sys
import threading
import time
from pathlib import Path

from . import brain as brain_mod
from . import config, digest, employee, scheduler, state, telegram, tools, voice
from . import webhook as webhook_mod

log = logging.getLogger("frontdesk")

MAX_PAIR_ATTEMPTS = 5

HELP = """Front desk commands:
/status   what has been dispatched and how it went
/brief    the morning brief, now
/voice    voice replies on / off (currently: {voice})
/digest   rebuild the picture of the operation from personal-os
/help     this

Anything else is just talked to. Voice notes work: they are transcribed on
this machine and the transcript is quoted back so a mishearing is visible."""


def _setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


class FrontDesk:
    def __init__(self) -> None:
        config.ensure_dirs()
        env = config.load_env()

        token = env.get("TELEGRAM_BOT_TOKEN")
        if not token:
            raise SystemExit(
                "No Telegram bot token.\n"
                f"Expected TELEGRAM_BOT_TOKEN in {config.ENV_FILE}, or the "
                f"plugin's own token at {config.PLUGIN_ENV}.\n"
                "Run scripts\\frontdesk-set-key.ps1 to store both secrets.")

        api_key = env.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise SystemExit(
                "No ANTHROPIC_API_KEY.\n"
                f"Put it in {config.ENV_FILE} (scripts\\frontdesk-set-key.ps1).\n"
                "This is a console.anthropic.com key, separate from the claude.ai "
                "subscription - the fast model is called directly, not through the CLI.")

        self.tg = telegram.Telegram(token)
        self.brain = brain_mod.Brain(api_key)
        self.chat_id = env.get("TELEGRAM_CHAT_ID") or state.get_meta("chat_id")
        # The code is printed in this window and nowhere else. Anyone who finds
        # the bot can message it, so it must never be sent over the channel it
        # is meant to protect.
        self.pair_code = secrets.token_hex(4)
        self.pair_attempts = 0
        self.voice_replies = state.get_meta("voice_replies", "auto") or "auto"
        self.running = True
        self._sender_wake = threading.Event()

        self.webhook_token = env.get("FRONTDESK_WEBHOOK_TOKEN", "")
        self.scheduler = scheduler.Scheduler(self.push, self.brain)
        self.webhook = None

    # --- outbound ---------------------------------------------------------
    def push(self, text: str) -> None:
        """Queue a message for the phone. Written to the outbox first, so a
        Telegram outage delays it instead of losing it."""
        state.enqueue_push(text)
        state.add_message("assistant", text, self.chat_id, via="push")
        self._sender_wake.set()

    def _sender(self) -> None:
        """Drain the outbox. Separate from the poll loop, which blocks 50s."""
        while self.running:
            if self.chat_id:
                for row in state.pending_pushes():
                    try:
                        self.tg.send(self.chat_id, row["text"])
                        state.mark_push_sent(row["id"])
                    except Exception as exc:  # noqa: BLE001 - retry on the next pass
                        log.warning("push %d not sent: %s", row["id"], exc)
                        break
            self._sender_wake.wait(3)
            self._sender_wake.clear()

    # --- inbound ----------------------------------------------------------
    def poll(self) -> None:
        offset = int(state.get_meta("update_offset", "0") or 0)
        log.info("polling from offset %d", offset)
        while self.running:
            updates = self.tg.get_updates(offset, config.POLL_TIMEOUT)
            for update in updates:
                offset = max(offset, int(update["update_id"]) + 1)
                state.set_meta("update_offset", str(offset))
                try:
                    self.handle(update.get("message") or {})
                except Exception:  # noqa: BLE001 - one bad message must not end the loop
                    log.exception("handling a message failed")
                    if self.chat_id:
                        try:
                            self.tg.send(self.chat_id,
                                         "Something broke handling that. Nothing was "
                                         "dispatched. Check the front desk window.")
                        except Exception:  # noqa: BLE001
                            pass

    def handle(self, message: dict) -> None:
        if not message:
            return
        chat = str((message.get("chat") or {}).get("id") or "")
        if not chat:
            return

        text = (message.get("text") or message.get("caption") or "").strip()
        note = message.get("voice") or message.get("audio")

        # --- who may talk to it ------------------------------------------
        if not self.chat_id:
            if self.pair_attempts >= MAX_PAIR_ATTEMPTS:
                # Locked for this run. Restarting the front desk mints a new
                # code, which is the intended way back in.
                log.warning("pairing is locked after %d wrong codes; chat %s "
                            "tried again", self.pair_attempts, chat)
                return
            if text.lower().startswith("/pair "):
                if secrets.compare_digest(text.split(None, 1)[1].strip(),
                                          self.pair_code):
                    self.chat_id = chat
                    state.set_meta("chat_id", chat)
                    log.info("paired to chat %s", chat)
                    self.tg.send(chat, "Paired. I am the front desk. Ask me anything.")
                    self._sender_wake.set()
                else:
                    self.pair_attempts += 1
                    left = MAX_PAIR_ATTEMPTS - self.pair_attempts
                    log.warning("wrong pairing code from chat %s (%d attempt(s) left)",
                                chat, left)
                    self.tg.send(chat, "Wrong code."
                                 if left else "Wrong code. Pairing is locked; "
                                              "restart the front desk to try again.")
                return
            # Deliberately does NOT say what the code is: the window on main-pc
            # does. Telling the channel would hand it to whoever found the bot.
            log.warning("unpaired chat %s tried to talk. The pairing code is %s "
                        "- send it from the phone as: /pair %s",
                        chat, self.pair_code, self.pair_code)
            self.tg.send(chat, "Not paired. The pairing code is printed on the "
                               "machine running this; send it as /pair <code>.")
            return

        if chat != self.chat_id:
            # Allowlist of exactly one, the same posture as the Telegram
            # plugin's `access policy allowlist`.
            log.warning("ignored a message from chat %s (paired to %s)", chat, self.chat_id)
            return

        self.tg.typing(chat)

        # --- voice in -----------------------------------------------------
        spoke = False
        if note and not text:
            spoke = True
            text = self._transcribe(chat, note)
            if not text:
                return

        if not text:
            return

        if text.startswith("/"):
            if self._command(chat, text):
                return

        state.add_message("user", text, chat, via="voice" if spoke else "text")

        started = time.time()
        answer = self.brain.respond(text, lambda line: self._send_now(chat, line))
        log.info("answered in %.2fs", time.time() - started)

        if not answer:
            return
        state.add_message("assistant", answer, chat)
        self._deliver(chat, answer, spoken_input=spoke)

    def _send_now(self, chat: str, line: str) -> None:
        """A line that must not wait for the turn to finish - the `reply` on a
        delegate or a remind."""
        try:
            self.tg.send(chat, line)
            state.add_message("assistant", line, chat, via="ack")
        except Exception as exc:  # noqa: BLE001
            log.warning("immediate reply failed, queueing it: %s", exc)
            state.enqueue_push(line)
            self._sender_wake.set()

    def _transcribe(self, chat: str, note: dict) -> str:
        self.tg.typing(chat, "typing")
        audio = self.tg.download(note.get("file_id", ""), config.WORK_DIR)
        if not audio:
            self.tg.send(chat, "I could not download that voice note.")
            return ""
        env = config.load_env()
        try:
            text, lang, prob = voice.transcribe(audio, env.get("STT_LANGUAGE") or None)
        except voice.VoiceUnavailable as exc:
            log.warning("stt unavailable: %s", exc)
            self.tg.send(chat, "Voice is not set up on this machine yet - type it instead.")
            return ""
        if not text:
            self.tg.send(chat, "That came through empty. Say it again?")
            return ""
        # Quote the transcript back, always: docs/employee.md's rule, so a
        # mishearing is visible before it becomes a wrong answer.
        flag = "" if prob >= 0.75 else f"  [low confidence {prob:.2f}]"
        self.tg.send(chat, f"heard ({lang}){flag}: {text}")
        return text

    def _deliver(self, chat: str, answer: str, spoken_input: bool) -> None:
        want_voice = self.voice_replies == "on" or (
            self.voice_replies == "auto" and spoken_input)
        if want_voice:
            path = voice.speak(answer)
            if path:
                try:
                    self.tg.send_voice(chat, Path(path), answer[:900])
                    return
                except Exception as exc:  # noqa: BLE001 - fall through to text
                    log.warning("sendVoice failed: %s", exc)
        self.tg.send(chat, answer)

    # --- commands ---------------------------------------------------------
    def _command(self, chat: str, text: str) -> bool:
        cmd, _, rest = text.partition(" ")
        cmd = cmd.lower().lstrip("/").split("@")[0]
        rest = rest.strip()

        if cmd == "help":
            self.tg.send(chat, HELP.format(voice=self.voice_replies))
            return True
        if cmd == "status":
            self.tg.send(chat, employee.summary())
            return True
        if cmd == "brief":
            text_out = self.brain.compose(scheduler.BRIEF_INSTRUCTION)
            self.tg.send(chat, text_out or "Nothing to report.")
            return True
        if cmd == "digest":
            digest.get(force=True)
            self.tg.send(chat, f"Rebuilt from personal-os ({len(digest.get())} chars).")
            return True
        if cmd == "voice":
            if rest in ("on", "off", "auto"):
                self.voice_replies = rest
                state.set_meta("voice_replies", rest)
                self.tg.send(chat, f"Voice replies: {rest}.")
            else:
                self.tg.send(chat, f"Voice replies are {self.voice_replies}. "
                                   f"Use /voice on, /voice off or /voice auto.")
            return True
        if cmd == "pair":
            self.tg.send(chat, "Already paired.")
            return True
        return False   # not a command: let the model see it

    # --- lifecycle --------------------------------------------------------
    def start(self) -> None:
        log.info("personal-os root: %s", config.REPO_ROOT)
        log.info("state: %s", config.STATE_DIR)
        binary = employee.claude_binary()
        log.info("worker CLI: %s", binary or "NOT FOUND - delegation will fail")
        log.info("voice stack: %s", "ready" if voice.available()
                 else f"absent ({config.STT_VENV_PYTHON})")
        log.info("digest: %d chars", len(digest.get()))

        if not self.chat_id:
            log.warning("NOT PAIRED. From your phone, message the bot: /pair %s",
                        self.pair_code)
        else:
            log.info("paired to chat %s", self.chat_id)

        threading.Thread(target=self._sender, name="sender", daemon=True).start()
        self.scheduler.start()
        self.webhook = webhook_mod.start(self.push, self.webhook_token)
        self.poll()

    def stop(self, *_args) -> None:
        log.info("shutting down")
        self.running = False
        self.scheduler.stop()
        self._sender_wake.set()
        if self.webhook:
            self.webhook.shutdown()


def main() -> int:
    _setup_logging()
    desk = FrontDesk()
    signal.signal(signal.SIGINT, desk.stop)
    signal.signal(signal.SIGTERM, desk.stop)
    try:
        desk.start()
    except KeyboardInterrupt:
        desk.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
