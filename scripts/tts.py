# Speak text to an .ogg (Opus) voice file, fully local: Kokoro neural TTS (ONNX, CPU) -> PyAV.
# Usage: %USERPROFILE%\.venvs\stt\Scripts\python.exe scripts\tts.py <out.ogg> "<text>" [voice]
# Model files live in %USERPROFILE%\.cache\kokoro (kokoro-v1.0.onnx, voices-v1.0.bin).
# main-pc / laptop only - never install this on cnc-pc.
import os
import sys

import av
import numpy as np
from kokoro_onnx import Kokoro

out_path, text = sys.argv[1], sys.argv[2]
voice = sys.argv[3] if len(sys.argv) > 3 else "am_michael"

models = os.path.join(os.path.expanduser("~"), ".cache", "kokoro")
kokoro = Kokoro(os.path.join(models, "kokoro-v1.0.onnx"), os.path.join(models, "voices-v1.0.bin"))
samples, rate = kokoro.create(text, voice=voice, speed=1.0, lang="en-us")
pcm = (np.clip(samples, -1.0, 1.0) * 32767).astype(np.int16).reshape(1, -1)

with av.open(out_path, "w", format="ogg") as dst:
    stream = dst.add_stream("libopus", rate=48000)
    stream.bit_rate = 48000
    resampler = av.AudioResampler(format="s16", layout="mono", rate=48000)
    frame = av.AudioFrame.from_ndarray(pcm, format="s16", layout="mono")
    frame.sample_rate = rate
    for r in resampler.resample(frame) + resampler.resample(None):
        for packet in stream.encode(r):
            dst.mux(packet)
    for packet in stream.encode(None):
        dst.mux(packet)

print(out_path)
