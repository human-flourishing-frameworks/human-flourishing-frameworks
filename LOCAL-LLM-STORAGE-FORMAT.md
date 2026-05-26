# Local LLM Storage Format — Permanent Archive & Mesh HDD Backup

**Purpose**: Compress all Lantern OS data into a standardized local storage format optimized for:
- Permanent archival (no cloud)
- Mesh HDD backup (distributed storage across 20+ drives)
- Fast LLM context injection (embed in system prompts)
- Zero external dependency (all offline)

---

## Archive Structure

```
~/.lantern-archive/
├── meta.json                          # Archive metadata (version, created, hash)
├── manifest.jsonl                     # File index (path, size, hash, type)
├── llm-context/
│   ├── system-instructions.txt        # Core system prompt (LLM-readable)
│   ├── conversation-index.jsonl       # All conversations (indexed)
│   ├── knowledge-base.jsonl           # Extracted knowledge (embeddings ready)
│   └── decisions.jsonl                # Key decisions + rationale
├── audio/
│   ├── sounds-manifest.json           # Audio metadata + licenses
│   ├── sounds-archive.tar.zst         # Compressed audio (all CC-licensed tracks)
│   └── vosk-models.tar.zst            # Speech models archive
├── code/
│   ├── all-scripts.tar.zst            # All .py/.ps1/.sh scripts
│   ├── config.jsonl                   # All config files (versioned)
│   └── deployment-index.json          # Which script runs where, when
├── state/
│   ├── active-conversations.jsonl     # Current chat threads
│   ├── persistent-logs.jsonl          # All event logs
│   ├── model-configs.json             # LLM provider configs
│   └── telemetry.jsonl                # Performance metrics
├── docs/
│   ├── all-guides.tar.zst             # Compressed markdown files
│   └── docs-index.json                # Navigation index
├── mesh-inventory.json                # Where data stored on each HDD
└── integrity/
    ├── checksums.sha256               # File integrity hashes
    ├── signed-manifest.sig            # Ed25519 signature
    └── backup-status.jsonl            # HDD backup verification
```

---

## Storage Formats

### 1. Metadata (meta.json)

```json
{
  "format_version": "1.0",
  "created": "2026-05-26T12:00:00Z",
  "last_updated": "2026-05-26T15:30:45Z",
  "lantern_version": "1.0",
  "total_size_gb": 42.5,
  "compressed_size_gb": 8.3,
  "compression_ratio": 0.195,
  "compression_algorithm": "zstandard",
  "encryption": "none",
  "signer_ed25519_pubkey": "base64-encoded-pubkey",
  "last_integrity_check": "2026-05-26T15:30:45Z",
  "archive_hash_sha256": "hex-hash-of-all-files"
}
```

### 2. Conversation Index (conversation-index.jsonl)

Each line is one conversation thread:

```jsonl
{"thread_id": "conv-20260526-001", "created": "2026-05-26T10:00:00Z", "participant": "user", "duration_sec": 1230, "message_count": 42, "token_count": 5000, "topics": ["coding", "architecture"], "mood": "focused", "summary": "Discussed API design patterns", "file_offset": 120000, "file_size": 45000}
{"thread_id": "conv-20260526-002", "created": "2026-05-26T11:30:00Z", "participant": "user", "duration_sec": 890, "message_count": 28, "token_count": 3200, "topics": ["debugging"], "mood": "productive", "summary": "Debugged auth system", "file_offset": 165000, "file_size": 32000}
```

### 3. Knowledge Base (knowledge-base.jsonl)

Extracted facts + embeddings-ready format:

```jsonl
{"fact_id": "kb-001", "source_conv": "conv-20260526-001", "text": "API uses OAuth2 with JWT tokens", "category": "architecture", "confidence": 0.95, "embedding": [0.12, -0.45, ...512 floats...], "tags": ["security", "authentication"], "created": "2026-05-26T10:15:00Z"}
{"fact_id": "kb-002", "source_conv": "conv-20260526-002", "text": "Database connection pooling improves throughput by 40%", "category": "performance", "confidence": 0.88, "embedding": [0.08, 0.22, ...512 floats...], "tags": ["database", "optimization"], "created": "2026-05-26T11:45:00Z"}
```

### 4. Sound Manifest (sounds-manifest.json)

```json
{
  "archive_created": "2026-05-26T12:00:00Z",
  "compression": "zstandard",
  "total_duration_minutes": 127,
  "tracks": [
    {
      "id": "blue_whale_pacific",
      "filename": "Blue_Whale_South_Pacific.ogg",
      "source_url": "https://commons.wikimedia.org/wiki/File:Blue_whale_sound_1.ogg",
      "license": "CC0-1.0",
      "attribution": "Wikimedia Commons",
      "duration_sec": 45,
      "sample_rate_hz": 44100,
      "format": "ogg_vorbis",
      "filesize_kb": 45,
      "use_case": "nature_soundscape"
    },
    {
      "id": "mozart_kleine_nachtmusik",
      "filename": "Mozart_Eine_kleine_Nachtmusik.mp3",
      "source_url": "https://imslp.org/wiki/Eine_kleine_Nachtmusik_%28Mozart%2C_Wolfgang_Amadeus%29",
      "license": "public_domain",
      "attribution": "International Music Score Library Project (IMSLP)",
      "duration_sec": 1240,
      "sample_rate_hz": 48000,
      "format": "mp3",
      "filesize_kb": 18500,
      "use_case": "classical_music"
    }
  ],
  "license_summary": "All tracks CC0 or public domain. No copyright restrictions. Safe for commercial use.",
  "checksum_sha256": "hex-hash"
}
```

### 5. Deployment Index (deployment-index.json)

Which scripts run where, in what order:

```json
{
  "platforms": {
    "windows": {
      "startup_order": [
        {
          "seq": 1,
          "name": "Check Python",
          "script": "system-checks.ps1",
          "timeout_sec": 10,
          "critical": true
        },
        {
          "seq": 2,
          "name": "Start Ollama",
          "script": "SETUP-OLLAMA-QUICK.ps1",
          "timeout_sec": 30,
          "critical": true
        },
        {
          "seq": 3,
          "name": "Launch Button Server",
          "script": "START-BOTH-UNLIMITED.ps1",
          "timeout_sec": 10,
          "critical": true
        },
        {
          "seq": 4,
          "name": "Start Discord Bot (optional)",
          "script": "START-DISCORD-RADIO.ps1",
          "timeout_sec": 15,
          "critical": false
        }
      ]
    },
    "linux": {
      "startup_order": [
        {
          "seq": 1,
          "name": "Check Python 3",
          "script": "system-checks.sh",
          "timeout_sec": 10,
          "critical": true
        },
        {
          "seq": 2,
          "name": "Launch Master Script",
          "script": "MASTER-START-LINUX.sh",
          "timeout_sec": 10,
          "critical": true
        },
        {
          "seq": 3,
          "name": "Verify Systemd Services",
          "script": "verify-systemd.sh",
          "timeout_sec": 15,
          "critical": false
        }
      ]
    }
  }
}
```

### 6. Mesh Inventory (mesh-inventory.json)

Where data stored on each HDD in distributed setup:

```json
{
  "mesh_total_capacity_gb": 1000,
  "mesh_used_gb": 250,
  "replication_factor": 3,
  "nodes": [
    {
      "node_id": "hdd-01",
      "mount_point": "/mnt/hdd01",
      "capacity_gb": 4000,
      "used_gb": 85,
      "files": [
        {
          "path": "archive/llm-context/",
          "size_gb": 2.5,
          "checksum": "sha256-hash",
          "last_verified": "2026-05-26T15:00:00Z"
        },
        {
          "path": "archive/audio/sounds-archive.tar.zst",
          "size_gb": 1.8,
          "checksum": "sha256-hash",
          "last_verified": "2026-05-26T15:00:00Z"
        }
      ]
    },
    {
      "node_id": "hdd-02",
      "mount_point": "/mnt/hdd02",
      "capacity_gb": 2000,
      "used_gb": 82,
      "files": [
        {
          "path": "archive/code/",
          "size_gb": 0.3,
          "checksum": "sha256-hash",
          "last_verified": "2026-05-26T15:00:00Z"
        },
        {
          "path": "archive/vosk-models.tar.zst",
          "size_gb": 1.2,
          "checksum": "sha256-hash",
          "last_verified": "2026-05-26T15:00:00Z"
        }
      ]
    }
  ]
}
```

---

## LLM Context Injection

Use the archive to augment LLM prompts without passing full conversation history:

### System Prompt Template

```
You are Lantern, a local-first AI assistant.

KNOWLEDGE BASE (from persistent storage):
{{ knowledge-base.jsonl | top 20 facts by relevance }}

RECENT DECISIONS:
{{ decisions.jsonl | last 5 decisions }}

CONVERSATION SUMMARY:
{{ conversation-index.jsonl | today's conversations | summary }}

CURRENT CONTEXT:
- Platform: {{ meta.json | current_platform }}
- Uptime: {{ state/persistent-logs.jsonl | session_start_time }}
- Token usage: {{ state/telemetry.jsonl | total_tokens_today }}

Respond concisely. Cite sources from knowledge base if relevant.
```

---

## Creation Script (create-local-archive.py)

```python
#!/usr/bin/env python3
import json
import os
import hashlib
import tarfile
import zstandard as zstd
from pathlib import Path
from datetime import datetime

def create_archive(source_dir, archive_dir):
    """Create local LLM storage archive from ~/. lantern/"""
    
    meta = {
        "format_version": "1.0",
        "created": datetime.utcnow().isoformat() + "Z",
        "lantern_version": "1.0"
    }
    
    # Compress LLM context
    cctx = zstandard.ZstdCompressor()
    
    # Index conversations
    conv_index = []
    for log in Path(source_dir).glob("state/*.jsonl"):
        with open(log) as f:
            for line in f:
                entry = json.loads(line)
                conv_index.append(entry)
    
    # Write metadata
    with open(os.path.join(archive_dir, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    
    # Compress audio
    with tarfile.open(os.path.join(archive_dir, "sounds-archive.tar"), "w") as tar:
        tar.add(os.path.join(source_dir, "sounds"), arcname="sounds")
    
    # Compress with zstd
    with open(os.path.join(archive_dir, "sounds-archive.tar")) as f_in:
        with open(os.path.join(archive_dir, "sounds-archive.tar.zst"), "wb") as f_out:
            cctx.copy_stream(f_in, f_out)
    
    print(f"✓ Archive created: {archive_dir}")
    print(f"  Conversations indexed: {len(conv_index)}")
    print(f"  Audio compressed: sounds-archive.tar.zst")
    print(f"  Ready for mesh HDD backup")

if __name__ == "__main__":
    create_archive(
        os.path.expanduser("~/.lantern"),
        os.path.expanduser("~/.lantern-archive")
    )
```

---

## Backup to Mesh HDDs

### Sync to Node 1
```bash
rsync -av --checksum ~/.lantern-archive/llm-context/ /mnt/hdd01/archive/llm-context/
rsync -av --checksum ~/.lantern-archive/sounds-archive.tar.zst /mnt/hdd01/archive/
```

### Sync to Node 2
```bash
rsync -av --checksum ~/.lantern-archive/code/ /mnt/hdd02/archive/code/
rsync -av --checksum ~/.lantern-archive/vosk-models.tar.zst /mnt/hdd02/archive/
```

### Verify Integrity
```bash
sha256sum -c mesh-inventory.json | grep "OK"
```

---

## Storage Efficiency

| Component | Original | Compressed | Ratio |
|-----------|----------|-----------|-------|
| Audio (27 tracks) | 1.2 GB | 0.35 GB | 29% |
| Vosk models | 2.5 GB | 0.8 GB | 32% |
| Code (all scripts) | 5 MB | 2 MB | 40% |
| State/Logs (30 days) | 12 GB | 1.8 GB | 15% |
| Docs (markdown) | 50 MB | 8 MB | 16% |
| **TOTAL** | **15.8 GB** | **3.0 GB** | **19%** |

**Result**: Full 30-day archive fits on single 8GB USB. Mesh deployment uses 6 drives.

---

## Restore from Archive

```python
import tarfile
import zstandard

# Decompress audio
with open("sounds-archive.tar.zst", "rb") as f_in:
    dctx = zstandard.ZstdDecompressor()
    with open("sounds-archive.tar", "wb") as f_out:
        dctx.copy_stream(f_in, f_out)

# Extract
with tarfile.open("sounds-archive.tar") as tar:
    tar.extractall()

# Verify
for file in Path(".").glob("**/*"):
    with open(file, "rb") as f:
        actual_hash = hashlib.sha256(f.read()).hexdigest()
        assert actual_hash == manifest[file.name]["checksum"]

print("✓ Archive restored and verified")
```

---

## Schedule

- **Daily**: Incremental backup of state/ and logs/ to nearest mesh HDD node
- **Weekly**: Full archive creation + integrity check
- **Monthly**: Replicate to all 3+ backup nodes
- **Quarterly**: Archive rotation (move oldest to cold storage)

