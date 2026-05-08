# Human Flourishing Frameworks

**Research software for monitoring and reporting AI bias.**

> **Status**: Early development. This is research software, not a production system. There is no formal governance board, no government partnerships, and no court-validated evidence. Data shown is synthetic unless explicitly labeled otherwise.

## What This Actually Is

A Flask-based framework for:
- Logging reports of AI system bias (currently using mock data)
- Peer-to-peer sync between nodes via HTTP
- Byzantine fault-tolerant consensus on violation reports (PBFT implementation)
- Cryptographically signed audit trails (Ed25519)

## What This Is Not

- Not production-ready
- Not endorsed by any government agency, university, or standards body
- Not "13 nodes deployed globally" — deployment is local development plus 1 Railway instance
- Not tracking real violations — all current data is clearly labeled as mock/demo

## Current State (Honest)

| Component | Status |
|-----------|--------|
| Flask app | Working locally |
| PBFT consensus | Teaching implementation — handles happy path |
| Cryptographic signing | Ed25519 via `cryptography` library |
| Mesh sync | HTTP POST between known peers |
| Mock data | 4 synthetic violations, clearly labeled |
| Real data | ProPublica COMPAS summary (attributed, not our analysis) |
| Governance | None. This is a solo research project. |
| Cloud deployment | 1 Railway instance (may be inactive) |

## Quick Start

```bash
git clone https://github.com/human-flourishing-frameworks/human-flourishing-frameworks.git
cd human-flourishing-frameworks
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

## Architecture

- `app.py` — Main Flask application and dashboard
- `byzantine_consensus.py` — PBFT consensus protocol (teaching implementation)
- `cryptographic_proof.py` — Ed25519 signing, Merkle trees, audit log
- `data_sources.py` — Mock data and public dataset references
- `mesh_network.py` — HTTP-based peer sync
- `adoption_tracker.py` — Node registration and stats

## Data Sources

This project does not generate original bias measurements. Current data:

- **Mock violations**: Clearly labeled synthetic data for testing (`source: "MOCK - Not Real Data"`)
- **COMPAS reference**: Summary of ProPublica's published analysis (Angwin et al., 2016). We did not conduct this research; we cite it.

## Contributing

This project needs honest contributors. If you want to help:
1. Pick a real, public dataset on AI bias
2. Write a proper data source with full attribution
3. Open a PR

## License

[Add actual license here]

---

*Previously, this repository contained fabricated claims about deployment scale, government partnerships, governance boards, and violation data. Those claims have been removed. This README reflects only what is verifiably true.*
