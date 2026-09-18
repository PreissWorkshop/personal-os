# Speak text to an .ogg (Opus) voice file, fully local: Windows System.Speech -> WAV -> PyAV.
# Usage: %USERPROFILE%\.venvs\stt\Scripts\python.exe scripts\tts.py <out.ogg> "<text>"
# main-pc / laptop only - never install this on cnc-pc.
import os
import subprocess
import sys
import tempfile

import av

out_path, text = sys.argv[1], sys.argv[2]
wav = os.path.join(tempfile.gettempdir(), "employee-tts.wav")
txt = wav + ".txt"
with open(txt, "w", encoding="utf-8") as f:
    f.write(text)

ps = (
    "Add-Type -AssemblyName System.Speech; "
    "$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
    f"$s.SetOutputToWaveFile('{wav}'); "
    f"$s.Speak([IO.File]::ReadAllText('{txt}')); $s.Dispose()"
)
subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)

with av.open(wav) as src, av.open(out_path, "w", format="ogg") as dst:
    stream = dst.add_stream("libopus", rate=48000)
    stream.bit_rate = 32000
    resampler = av.AudioResampler(format="s16", layout="mono", rate=48000)
    for frame in src.decode(audio=0):
        for r in resampler.resample(frame):
            for packet in stream.encode(r):
                dst.mux(packet)
    for r in resampler.resample(None):
        for packet in stream.encode(r):
            dst.mux(packet)
    for packet in stream.encode(None):
        dst.mux(packet)

os.remove(wav)
os.remove(txt)
print(out_path)
