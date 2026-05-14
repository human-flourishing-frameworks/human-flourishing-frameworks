"""Extract text from the operator-shared PDFs into the local state library.

Bravery protocol: read-only, local-only, summary-shaped. No cloud calls. No new
indexing of unrelated files — only the PDFs Papa explicitly @-referenced.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
import sys
import subprocess
import time

# The 16 PDFs Papa @-referenced. Kept literal so we never go wider than the ask.
DOWNLOADS = Path.home() / "Downloads"
PAPERS = [
    "Artificial Superintelligence (ASI) Alliance Vision Paper - CUDOS Edition.pdf",
    "what-is-the-artificial-intelligence-singularity.pdf",
    "AI-Singularity-Navigating-Implications-and-Framing-Strategic-Recommendations.pdf",
    "NTIBIO_AI_FINAL.pdf",
    "atarc_whitepaper_cyber–ai-convergence.pdf",
    "Clifford-Chance-Deutsche-Bank-Guide-on-Thought-Leadership-Convergence-of-AI-and-DLT-Sep2025.pdf",
    "01ab8d_5b94cc955833475ebe28af2fe7944da7.pdf",
    "01ab8d_0a032d693bfe4c24be09944eb193f1d9.pdf",
    "01ab8d_03572f3966cb48728e692acbcdfffdf0.pdf",
    "01ab8d_dd1437532a3a4935b39fcfb540c58d5b.pdf",
    "01ab8d_c54f3c4462e1459387944ed327741506.pdf",
    "01ab8d_e3b4379474e745fb83a7d9f4e44a16dd.pdf",
    "01ab8d_68e847c83097487cb6a7da2726ef3fab.pdf",
    "01ab8d_b75de03714bf4f9f9a31f4e47d72ce79.pdf",
    "01ab8d_87aa189565154f608c9c48964ee26888.pdf",
    "01ab8d_29dd6156220b43edb06ec167dc30d9fa.pdf",
]

OUT_DIR = Path.home() / ".lantern" / "state" / "papers"
OUT_DIR.mkdir(parents=True, exist_ok=True)
INDEX = OUT_DIR / "index.json"

PDF2TXT = Path.home() / "AppData" / "Local" / "Programs" / "Python" / "Python312" / "Scripts" / "pdf2txt.py"

results = []
t0 = time.time()
for i, name in enumerate(PAPERS, 1):
    src = DOWNLOADS / name
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in name).replace(".pdf", ".txt")
    dst = OUT_DIR / safe
    entry = {
        "ordinal": i,
        "source_pdf": name,
        "source_exists": src.exists(),
        "out_path": str(dst),
        "extracted_chars": 0,
        "extracted_ok": False,
        "error": None,
    }
    if not src.exists():
        entry["error"] = "source missing"
        results.append(entry)
        print(f"[{i:2d}/{len(PAPERS)}] MISS {name}")
        continue
    try:
        # pdf2txt.py prints extracted text to stdout
        cp = subprocess.run(
            [sys.executable, str(PDF2TXT), str(src)],
            capture_output=True, text=True, timeout=180, encoding="utf-8", errors="replace",
        )
        text = cp.stdout or ""
        # Trim to first ~8000 chars per PDF — enough to know what it's about,
        # not enough to drown anything reading it back.
        excerpt = text[:8000].strip()
        dst.write_text(excerpt, encoding="utf-8")
        entry["extracted_ok"] = True
        entry["extracted_chars"] = len(excerpt)
        results.append(entry)
        print(f"[{i:2d}/{len(PAPERS)}] OK   {name}  -> {entry['extracted_chars']} chars")
    except subprocess.TimeoutExpired:
        entry["error"] = "timeout"
        results.append(entry)
        print(f"[{i:2d}/{len(PAPERS)}] TIME {name}")
    except Exception as exc:
        entry["error"] = type(exc).__name__
        results.append(entry)
        print(f"[{i:2d}/{len(PAPERS)}] FAIL {name} {exc}")

INDEX.write_text(json.dumps({
    "ingested_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "boundary": "Papa-shared PDFs only. Read-only excerpts. Not proof.",
    "elapsed_seconds": round(time.time() - t0, 1),
    "papers": results,
}, indent=2), encoding="utf-8")
print(f"\nindex: {INDEX}")
print(f"elapsed: {time.time() - t0:.1f}s")
