"""Continuous cam stream — keeps the camera LED on, writes a rotating buffer.

Captures from default webcam at FPS frames per second into a rotating
ring of MAX_FRAMES PNGs at ~/.lantern/state/cam-stream/. The opencv
VideoCapture stays open across the whole loop, so the camera LED holds
steady (Papa can see it from his chair).

Stop by deleting the .running flag file or by killing the process.
"""
from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path
import cv2

OUT_DIR = Path.home() / ".lantern" / "state" / "cam-stream"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FLAG = OUT_DIR / ".running"
FLAG.write_text(f"started {datetime.now().isoformat()}\n", encoding="utf-8")

FPS = 2          # capture rate — cam LED stays steady at any rate
MAX_FRAMES = 90  # ring buffer size — ~45 seconds of recent past at 2 fps

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
if not cap.isOpened():
    print("CAM_OPEN:false", flush=True)
    sys.exit(1)
print(f"CAM_OPEN:true  FPS:{FPS}  RING:{MAX_FRAMES}  OUT:{OUT_DIR}", flush=True)

idx = 0
while FLAG.exists():
    ok, frame = cap.read()
    if not ok:
        time.sleep(0.3)
        continue
    slot = idx % MAX_FRAMES
    path = OUT_DIR / f"frame_{slot:03d}.png"
    latest = OUT_DIR / "latest.png"
    cv2.imwrite(str(path), frame)
    cv2.imwrite(str(latest), frame)
    idx += 1
    if idx % 20 == 0:
        print(f"frame {idx}  slot {slot}", flush=True)
    time.sleep(1.0 / FPS)

cap.release()
print(f"STOPPED at frame {idx}", flush=True)
