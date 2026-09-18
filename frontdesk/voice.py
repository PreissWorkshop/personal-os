"""Voice in, voice out - wrapping the local stack that already exists.

scripts/stt.py  faster-whisper, CPU, audio never leaves the machine
scripts/tts.py  Kokoro ONNX -> Opus .ogg, voice bm_george at 1.2x (Tenis, 2026-09-18)

Both live in %USERPROFILE%\\.venvs\\stt. main-pc and laptop only - never
cnc-pc (machine roles are law).

KNOWN LIMIT, English only: tts.py passes lang="en-us" and bm_george is an
English voice. Icelandic replies are sent as text, not spoken - marked
[UNVERIFIED - needs check] whether the Kokoro build on this machine carries
any Icelandic voice at all. Whisper does transcribe Icelandic, at materially
worse accuracy than English, which is why the transcript is always quoted
back so a mishearing is visible (docs/employee.md -> Reporting).
"""

from __future__ import annotations

import logging
import re
import subprocess
import time
from pathlib import Path

from . import config

log = logging.getLogger("frontdesk.voice")

_HEADER = re.compile(r"^\[language=(?P<lang>\S+)\s+p=(?P<p>[\d.]+)\s+duration=(?P<dur>[\d.]+)s\]")

# Characters that read as noise when spoken aloud.
_SPEAKABLE = re.compile(r"[*_`#>|]+")


class VoiceUnavailable(RuntimeError):
    pass


def available() -> bool:
    return config.STT_VENV_PYTHON.exists()


def _script(name: str) -> Path:
    return config.REPO_ROOT / "scripts" / name


def transcribe(audio: Path, language: str | None = None,
               model: str = "small") -> tuple[str, str, float]:
    """Return (text, detected_language, probability).

    Raises VoiceUnavailable if the venv is missing, so the caller can fall
    back to telling Tenis to type instead of failing silently.
    """
    if not available():
        raise VoiceUnavailable(
            f"No STT venv at {config.STT_VENV_PYTHON}. "
            "See docs/employee.md -> Reporting -> Voice notes.")
    cmd = [str(config.STT_VENV_PYTHON), str(_script("stt.py")), str(audio), model]
    if language:
        cmd.append(language)
    started = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=300)
    if proc.returncode != 0:
        raise VoiceUnavailable(f"stt.py failed: {(proc.stderr or '').strip()[:400]}")
    lines = [line for line in (proc.stdout or "").splitlines() if line.strip()]
    lang, prob = "?", 0.0
    if lines:
        match = _HEADER.match(lines[0])
        if match:
            lang = match.group("lang")
            prob = float(match.group("p"))
            lines = lines[1:]
    log.info("transcribed %s in %.1fs (lang=%s p=%.2f)", audio.name,
             time.time() - started, lang, prob)
    return " ".join(lines).strip(), lang, prob


def speak(text: str, chat_hint: str = "reply") -> Path | None:
    """Render text to an Opus voice note. None means 'send it as text'.

    Refuses rather than mangles: too long, non-English, or no venv all return
    None and the caller sends text.
    """
    if not available():
        return None
    clean = _SPEAKABLE.sub("", text).strip()
    if not clean or len(clean) > config.SPEAK_CHAR_LIMIT:
        return None
    if _looks_icelandic(clean):
        # bm_george would read Icelandic as if it were English. Text is better
        # than a confident mispronunciation.
        return None
    env = config.load_env()
    out = config.WORK_DIR / f"{chat_hint}-{int(time.time())}.ogg"
    cmd = [str(config.STT_VENV_PYTHON), str(_script("tts.py")), str(out), clean,
           env.get("TTS_VOICE", "bm_george"), env.get("TTS_SPEED", "1.2")]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=180)
    except subprocess.TimeoutExpired:
        log.warning("tts.py timed out")
        return None
    if proc.returncode != 0 or not out.exists():
        log.warning("tts.py failed: %s", (proc.stderr or "").strip()[:400])
        return None
    return out


_ICELANDIC = set("þÞðÐæÆöÖáÁéÉíÍóÓúÚýÝ")


def _looks_icelandic(text: str) -> bool:
    return any(ch in _ICELANDIC for ch in text)


def prune(older_than_hours: float = 48.0) -> int:
    """Voice notes and spoken replies are transient; do not let them pile up."""
    cutoff = time.time() - older_than_hours * 3600
    removed = 0
    if not config.WORK_DIR.exists():
        return 0
    for path in config.WORK_DIR.iterdir():
        try:
            if path.is_file() and path.stat().st_mtime < cutoff:
                path.unlink()
                removed += 1
        except OSError:
            pass
    return removed
