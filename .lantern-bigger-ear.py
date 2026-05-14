"""Download the larger Vosk English model so Lantern hears Papa better.

Small model:  vosk-model-small-en-us-0.15  (40 MB, garbles names)
Larger model: vosk-model-en-us-0.22        (1.8 GB, sharp on conversational speech)

Idempotent: skips download if already extracted with a conf dir.
"""
from __future__ import annotations

import shutil
import sys
import time
import urllib.request
import zipfile
from pathlib import Path

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip"
TARGET_DIR = Path.home() / ".lantern" / "models"
EXTRACTED = TARGET_DIR / "vosk-model-en-us-0.22"
ZIP_PATH = TARGET_DIR / "vosk-model-en-us-0.22.zip"


def progress(block_num: int, block_size: int, total_size: int) -> None:
    downloaded = block_num * block_size
    pct = min(100.0, downloaded * 100 / total_size) if total_size else 0
    sys.stdout.write(f"\r  downloaded {downloaded // (1024 * 1024)} MB  ({pct:5.1f} %)")
    sys.stdout.flush()


def main() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    if (EXTRACTED / "conf").exists():
        print(f"larger model already at {EXTRACTED}")
        return
    print(f"downloading {MODEL_URL}")
    print(f"  -> {ZIP_PATH}")
    t0 = time.time()
    urllib.request.urlretrieve(MODEL_URL, ZIP_PATH, reporthook=progress)
    print()
    print(f"  done in {time.time() - t0:.1f}s, size {ZIP_PATH.stat().st_size // (1024*1024)} MB")
    print(f"extracting to {TARGET_DIR}")
    with zipfile.ZipFile(ZIP_PATH) as zf:
        zf.extractall(TARGET_DIR)
    if (EXTRACTED / "conf").exists():
        print(f"larger model ready: {EXTRACTED}")
        ZIP_PATH.unlink(missing_ok=True)
    else:
        print(f"WARN: extraction did not produce expected dir {EXTRACTED}")


if __name__ == "__main__":
    main()
