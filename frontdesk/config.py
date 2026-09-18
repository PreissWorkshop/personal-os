"""Front desk configuration - machine-local secrets, paths, models.

Nothing in here is ever committed with a value. Secrets live in
%USERPROFILE%\\.claude\\frontdesk\\.env, written by
scripts\\frontdesk-set-key.ps1, in the same place and the same way the
Telegram plugin's own token already lives.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

HOME = Path(os.path.expanduser("~"))

# Machine-local state: secrets, the database, transcripts, generated audio.
# Never inside the repo - docs/security.md.
STATE_DIR = HOME / ".claude" / "frontdesk"
ENV_FILE = STATE_DIR / ".env"
DB_PATH = STATE_DIR / "frontdesk.db"
WORK_DIR = STATE_DIR / "work"          # voice notes in, spoken replies out
TASK_LOG_DIR = STATE_DIR / "tasks"     # one transcript per delegated job

# The Telegram plugin's own token file. The front desk reads it as a fallback
# so Tenis never has to enter the same token twice.
PLUGIN_ENV = HOME / ".claude" / "channels" / "telegram" / ".env"

# personal-os on this machine, per registry/projects.yaml. The front desk
# reads this repo for its digest and delegates work rooted here.
REPO_ROOT = Path(os.environ.get("PERSONAL_OS_ROOT") or (Path(__file__).resolve().parent.parent))

# The local voice stack that already exists: scripts/stt.py + scripts/tts.py
# in their own venv (docs/employee.md -> Reporting -> Voice notes).
STT_VENV_PYTHON = HOME / ".venvs" / "stt" / "Scripts" / "python.exe"

# --- models ---------------------------------------------------------------
# Fast path. Everything Tenis types goes here first; it is the whole point.
FAST_MODEL = "claude-haiku-4-5-20251001"
# Escalation for a question that genuinely needs reasoning but not a whole
# Claude Code session. Still answered in the chat, still seconds not minutes.
SMART_MODEL = "claude-sonnet-5"

MAX_TOOL_ROUNDS = 3        # keep the loop short; the front desk is not a worker
HISTORY_TURNS = 12         # how much conversation the fast model carries
REPLY_LINE_LIMIT = 5       # docs/employee.md: the phone gets five lines
SPEAK_CHAR_LIMIT = 700     # longer than this is sent as text, not spoken

POLL_TIMEOUT = 50          # Telegram long-poll seconds
TICK_SECONDS = 20          # scheduler resolution
SILENT_TASK_NUDGE = 20 * 60   # a delegated job quiet this long gets a nudge

# Iceland is UTC+0 all year - no DST - so local time is UTC and the cron-ish
# schedules below need no conversion. Same assumption as docs/agent-system.md
# ("Cadence (UTC = Iceland)").
BRIEF_HOUR = 6
BRIEF_MINUTE = 45

WEBHOOK_HOST = os.environ.get("FRONTDESK_WEBHOOK_HOST", "0.0.0.0")
WEBHOOK_PORT = int(os.environ.get("FRONTDESK_WEBHOOK_PORT", "8787"))


def _parse_env(text: str) -> dict[str, str]:
    """Parse a KEY=value file.

    Split on any line ending. The Telegram plugin splits on LF only, which is
    how a Notepad-written CRLF file glued \\r to the token and broke every
    call on 2026-09-18 (docs/employee-setup-main-pc.md step 3). This parser
    strips \\r, so a CRLF file works here - but the plugin's own file must
    still be LF.
    """
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip('"').strip("'")
        out[key.strip()] = value
    return out


def load_env() -> dict[str, str]:
    """Environment first, then the front desk's .env, then the plugin's token."""
    values: dict[str, str] = {}
    if ENV_FILE.exists():
        values.update(_parse_env(ENV_FILE.read_text(encoding="utf-8-sig")))
    for key in ("TELEGRAM_BOT_TOKEN", "ANTHROPIC_API_KEY", "FRONTDESK_WEBHOOK_TOKEN",
                "TELEGRAM_CHAT_ID", "TTS_VOICE", "TTS_SPEED", "STT_LANGUAGE"):
        if os.environ.get(key):
            values[key] = os.environ[key]
    if not values.get("TELEGRAM_BOT_TOKEN"):
        token = _plugin_token()
        if token:
            values["TELEGRAM_BOT_TOKEN"] = token
    return values


def _plugin_token() -> str | None:
    """Recover the bot token from the Telegram plugin's .env.

    The variable name inside that file is the plugin's business, not ours, so
    match the token's shape instead of guessing a key: Telegram tokens are
    <numeric bot id>:<35-char secret>.
    """
    if not PLUGIN_ENV.exists():
        return None
    try:
        text = PLUGIN_ENV.read_text(encoding="utf-8-sig")
    except OSError:
        return None
    match = re.search(r"\b(\d{6,}:[A-Za-z0-9_-]{30,})\b", text)
    return match.group(1) if match else None


def ensure_dirs() -> None:
    for path in (STATE_DIR, WORK_DIR, TASK_LOG_DIR):
        path.mkdir(parents=True, exist_ok=True)
