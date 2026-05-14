"""Download the Vosk offline-STT small English model into ~/.lantern/models/.

Offline, local, deletable. ~40 MB. Vosk needs an unpacked model directory at
runtime to do speech-to-text without any cloud call. This script is idempotent
— if the model dir already exists with a real config, it does nothing.
"""
from __future__ import annotations

import shutil
import urllib.request
import zipfile
from pathlib import Path

MODEL_URL = "https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
TARGET_DIR = Path.home() / ".lantern" / "models"
EXTRACTED = TARGET_DIR / "vosk-model-small-en-us-0.15"
ZIP_PATH = TARGET_DIR / "vosk-model-small-en-us-0.15.zip"


def main() -> None:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    if (EXTRACTED / "conf").exists():
        print(f"Vosk model already at {EXTRACTED}")
        return

    print(f"downloading vosk model from {MODEL_URL}")
    print(f"  -> {ZIP_PATH}")
    urllib.request.urlretrieve(MODEL_URL, ZIP_PATH)
    print(f"  size: {ZIP_PATH.stat().st_size} bytes")

    print(f"extracting to {TARGET_DIR}")
    with zipfile.ZipFile(ZIP_PATH) as zf:
        zf.extractall(TARGET_DIR)

    if (EXTRACTED / "conf").exists():
        print(f"model ready: {EXTRACTED}")
        # tidy up the zip
        ZIP_PATH.unlink(missing_ok=True)
    else:
        print(f"WARN: extraction did not produce expected dir {EXTRACTED}")


if __name__ == "__main__":
    main()
