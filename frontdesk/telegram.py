"""Telegram client - the only process in the operation that talks to the bot.

Telegram allows exactly one poller per bot token (409 Conflict, and messages
are lost to whichever poller won). That is why the employee session drops
`--channels` when the front desk is running: see docs/frontdesk.md and
docs/employee-setup-main-pc.md step 3.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

import requests

log = logging.getLogger("frontdesk.telegram")


class Telegram:
    def __init__(self, token: str) -> None:
        if not token:
            raise ValueError("No Telegram bot token.")
        self.base = f"https://api.telegram.org/bot{token}"
        self.file_base = f"https://api.telegram.org/file/bot{token}"
        self._session = requests.Session()

    # --- low level --------------------------------------------------------
    def _call(self, method: str, timeout: int = 30, **kwargs):
        response = self._session.post(f"{self.base}/{method}", timeout=timeout, **kwargs)
        response.raise_for_status()
        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError(f"Telegram {method} failed: {payload}")
        return payload.get("result")

    # --- receiving --------------------------------------------------------
    def get_updates(self, offset: int, poll_timeout: int) -> list[dict]:
        """Long-poll. Returns [] on a network hiccup rather than raising: a
        dropped poll must never take the front desk down."""
        try:
            return self._call(
                "getUpdates",
                timeout=poll_timeout + 15,
                data={"offset": offset, "timeout": poll_timeout,
                      "allowed_updates": '["message"]'},
            ) or []
        except requests.exceptions.ReadTimeout:
            return []
        except Exception as exc:  # noqa: BLE001 - keep polling
            log.warning("getUpdates failed: %s", exc)
            time.sleep(3)
            return []

    def download(self, file_id: str, dest_dir: Path) -> Path | None:
        """Fetch an attachment (a voice note) to disk. Audio stays local."""
        try:
            info = self._call("getFile", data={"file_id": file_id})
            remote = info["file_path"]
            dest = dest_dir / f"{file_id}{Path(remote).suffix or '.oga'}"
            with self._session.get(f"{self.file_base}/{remote}", timeout=60,
                                   stream=True) as stream:
                stream.raise_for_status()
                with open(dest, "wb") as handle:
                    for chunk in stream.iter_content(65536):
                        handle.write(chunk)
            return dest
        except Exception as exc:  # noqa: BLE001
            log.warning("download of %s failed: %s", file_id, exc)
            return None

    # --- sending ----------------------------------------------------------
    def typing(self, chat_id: str, action: str = "typing") -> None:
        """Fire-and-forget: the phone shows activity within a few hundred ms,
        which is most of what 'feels fast' actually is."""
        try:
            self._call("sendChatAction", timeout=8,
                       data={"chat_id": chat_id, "action": action})
        except Exception:  # noqa: BLE001 - cosmetic only
            pass

    def send(self, chat_id: str, text: str) -> None:
        """Plain text on purpose - no parse_mode. Markdown parsing rejects
        the whole message over one stray underscore in a branch name."""
        if not text.strip():
            return
        for chunk in _split(text, 3900):
            try:
                self._call("sendMessage", timeout=20,
                           data={"chat_id": chat_id, "text": chunk,
                                 "disable_web_page_preview": True})
            except Exception as exc:  # noqa: BLE001
                log.warning("sendMessage failed: %s", exc)
                raise

    def send_voice(self, chat_id: str, path: Path, caption: str = "") -> None:
        with open(path, "rb") as handle:
            self._call("sendVoice", timeout=60,
                       data={"chat_id": chat_id, "caption": caption[:1000]},
                       files={"voice": handle})


def _split(text: str, limit: int) -> list[str]:
    """Split on line boundaries where possible - Telegram's cap is 4096."""
    if len(text) <= limit:
        return [text]
    chunks, current = [], ""
    for line in text.splitlines(keepends=True):
        while len(line) > limit:
            chunks.append(line[:limit])
            line = line[limit:]
        if len(current) + len(line) > limit:
            chunks.append(current)
            current = line
        else:
            current += line
    if current:
        chunks.append(current)
    return chunks
