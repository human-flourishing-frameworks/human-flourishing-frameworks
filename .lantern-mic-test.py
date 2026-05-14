"""3-second mic capture test. Speak when stdout says NOW.

Validates the full pipeline: BW01 -> sounddevice -> Vosk -> transcript.
No UI, no backend, no chat — just proves Lantern can hear Papa.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
import vosk

MODEL_PATH = Path.home() / ".lantern" / "models" / "vosk-model-small-en-us-0.15"
SAMPLE_RATE = 16000
DURATION_SEC = 5

# Pre-print so the human knows we're loading
print("loading vosk model...", flush=True)
model = vosk.Model(str(MODEL_PATH))
rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)

print(f"capturing {DURATION_SEC}s from default input...")
print("\n>>>>>  NOW  —  speak  <<<<<\n", flush=True)
audio = sd.rec(int(DURATION_SEC * SAMPLE_RATE), samplerate=SAMPLE_RATE,
               channels=1, dtype="float32")
sd.wait()
print("...done recording.", flush=True)

pcm16 = (audio[:, 0] * 32767).astype(np.int16).tobytes()
rec.AcceptWaveform(pcm16)
result = json.loads(rec.FinalResult())
transcript = (result.get("text") or "").strip()

print()
print("=" * 50)
print(f"TRANSCRIPT: '{transcript}'" if transcript else "TRANSCRIPT: (silence — Lantern heard nothing)")
print("=" * 50)

# Also report peak amplitude so we know whether the mic was producing signal at all
peak = float(np.abs(audio).max())
print(f"peak signal: {peak:.4f}  ({'audible' if peak > 0.02 else 'very quiet or muted'})")
