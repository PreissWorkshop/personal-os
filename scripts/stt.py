# Transcribe a voice note locally (faster-whisper, CPU). Audio never leaves the machine.
# Usage: %USERPROFILE%\.venvs\stt\Scripts\python.exe scripts\stt.py <audio file> [model] [language]
# main-pc / laptop only - never install this on cnc-pc.
import sys

from faster_whisper import WhisperModel

path = sys.argv[1]
model_name = sys.argv[2] if len(sys.argv) > 2 else "small"
language = sys.argv[3] if len(sys.argv) > 3 else None

model = WhisperModel(model_name, device="cpu", compute_type="int8")
segments, info = model.transcribe(path, language=language, vad_filter=True)
text = " ".join(s.text.strip() for s in segments)
sys.stdout.reconfigure(encoding="utf-8")
print(f"[language={info.language} p={info.language_probability:.2f} duration={info.duration:.0f}s]")
print(text)
