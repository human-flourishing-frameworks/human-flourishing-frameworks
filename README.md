# Human Flourishing Frameworks

**Research software for monitoring and reporting AI bias.**

> **Status**: Early development. This is research software, not a production system. There is no formal governance board, no government partnerships, and no court-validated evidence. See [`CORRECTIONS.md`](./CORRECTIONS.md) for what prior versions of this project claimed incorrectly.

---

## What This Actually Is

A Flask-based system for:
- Accepting and storing violation reports via API (`POST /api/violations`)
- Signing each submission with HMAC-SHA256 at intake (node-specific key)
- Peer-to-peer sync between nodes via HTTP mesh
- Byzantine fault-tolerant consensus on violation reports (PBFT implementation)
- Cryptographically signed audit trails (Ed25519)

## What This Is Not

- Not production-ready
- Not endorsed by any government agency, university, or standards body
- Not tracking 13 nodes globally — deployment is local development plus occasional cloud instances
- Not tracking real violations by default — submitted violations are real; demo data is clearly labeled synthetic
- Not court-admissible — HMAC-SHA256 over SQLite records is cryptographic integrity, not legal admissibility

## Current State (Honest)

| Component | Status |
|-----------|--------|
| Flask app | Working locally |
| Real violation intake | `POST /api/violations` — signed, stored, consensus-proposed |
| PBFT consensus | Teaching implementation — handles happy path |
| Cryptographic signing | HMAC-SHA256 (intake) + Ed25519 (audit trail) |
| Mesh sync | HTTP POST between known peers |
| Demo data | Synthetic violations, clearly labeled at `/api/violations/demo` |
| Real public data | ProPublica COMPAS summary (attributed) at `/api/violations/compas` |
| Governance | None. No board has been seated. |
| Cloud deployment | Occasional Railway/Render instances (may be inactive) |

---

## Quick Start

```bash
git clone https://github.com/human-flourishing-frameworks/human-flourishing-frameworks.git
cd human-flourishing-frameworks
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`. The dashboard loads all stats from the API — no numbers are hardcoded.

**Environment variables:**

| Variable | Default | Purpose |
|---|---|---|
| `PORT` | `5000` | Listen port |
| `NODE_NAME` | `node-<uuid>` | Display name |
| `CENTRAL_SERVER` | live Render URL | Set to `http://localhost:9999` to run fully offline |

---

## API

### Submit a violation

```
POST /api/violations
Content-Type: application/json

{
  "system_name":    "Name of the AI system",
  "violation_type": "Type of bias or harm",
  "severity":       "LOW|MEDIUM|HIGH|CRITICAL",
  "affected_count": 1000,
  "harm_amount":    "estimated $5M",    // optional
  "evidence":       "What happened",    // optional
  "reporter":       "anonymous"         // optional
}

→ 201 { "id": "<uuid>", "signature": "<hmac-sha256>", "status": "approved", ... }
```

### Other endpoints

```
GET  /health
GET  /api/status                       — real DB counts
GET  /api/violations                   — submitted violations
GET  /api/violations/<id>              — single violation + signature_valid
GET  /api/violations/demo              — synthetic demo data (labeled)
GET  /api/violations/compas            — ProPublica COMPAS reference (cited)
GET  /api/consensus/approved           — violations approved by Byzantine vote
GET  /api/consensus/status/<id>
POST /api/consensus/tally/<id>         — re-tally after peer votes arrive
GET  /api/mesh/peers
GET  /api/mesh/violations
POST /mesh/sync                        — peer-to-peer sync endpoint
GET  /api/adoption/stats
GET  /api/adoption/nodes
POST /api/adoption/register
```

---

## Multi-node consensus

Run three nodes to test real Byzantine consensus (requires >66.7% agreement):

```bash
PORT=5000 NODE_NAME=node-1 python app.py
PORT=5001 NODE_NAME=node-2 python app.py
PORT=5002 NODE_NAME=node-3 python app.py
```

Single-node deployments auto-approve every proposal (1/1 = 100%) — technically correct but not meaningfully Byzantine.

---

## Architecture

- `app.py` — Flask application, all routes
- `violations_db.py` — Real violation store, HMAC-SHA256 signing
- `byzantine_consensus.py` — PBFT consensus protocol
- `cryptographic_proof.py` — Ed25519 signing, Merkle trees, audit log
- `data_sources.py` — Synthetic demo data + COMPAS public dataset reference
- `mesh_network.py` — HTTP-based peer sync
- `adoption_tracker.py` — Node registration and stats

---

## Governance

The software is designed to support a 12-member independent governance board. **No board has been seated.** If you want to help build the governance structure: board@human-flourishing-frameworks.org

---

## Corrections

See [`CORRECTIONS.md`](./CORRECTIONS.md) for a full record of fabricated claims in prior versions and what was changed.

---

## License

- Specifications: CC-BY-4.0
- Code: Apache-2.0
- Governance documents: CC0
