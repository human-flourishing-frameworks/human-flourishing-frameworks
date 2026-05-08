# Human Flourishing Frameworks

**A system that observes outcomes, models causes, and optimizes for the most flourishing across all beings.**

> **Status**: Early development. The architecture is real, the code is honest, the deployment is live. The world model is a scaffold — it needs real sensors connected to real data to become useful. Every measurement carries uncertainty. Every prediction carries caveats. The system gets less wrong over time.

## What This Actually Is

A framework for measuring and improving outcomes — for people, animals, ecosystems, anything that can flourish:

- **Sensors** observe what's actually happening, with uncertainty bounds, provenance, and coverage gaps
- **World model** maintains Bayesian beliefs about the state of flourishing, updates as measurements arrive, self-corrects
- **Autonomous agents** (7, single-responsibility) detect violations, verify evidence, reach consensus, escalate — no human board, no discretion, no override
- **PBFT consensus** ensures agreement across untrusted nodes
- **Ed25519 cryptography** signs every record, chains every audit entry
- **Append-only audit trail** — immutable memory the system can always look back at

## What This Is Not

- Not production-ready
- Not endorsed by any government, university, or standards body
- Not tracking real violations yet — demo data is clearly labeled synthetic
- Not omniscient — the model only knows what the sensors can see, and it says so

## Current State (Honest)

| Component | Status |
|-----------|--------|
| Flask app + dashboard | Deployed on Render |
| Sensor framework | Built, needs real data sources connected |
| Bayesian world model | Built, needs measurements to become useful |
| Autonomous agents (7) | Algorithmic governance, no human board |
| PBFT consensus | Teaching implementation — handles happy path |
| Cryptographic signing | Ed25519 via `cryptography` library |
| Mesh sync | HTTP POST between known peers |
| Flourishing metrics | Defined for humans, animals, ecosystems — weights updatable |
| Real data | ProPublica COMPAS summary (attributed, not our analysis) |
| Demo data | Synthetic violations, clearly labeled |

## Quick Start

```bash
git clone https://github.com/human-flourishing-frameworks/human-flourishing-frameworks.git
cd human-flourishing-frameworks
pip install -r requirements.txt
python app.py
```

Visit http://localhost:5000

## Architecture

```
sensors.py           → Observe reality (with uncertainty)
world_model.py       → Believe, update, predict, correct
agent_system.py      → Act autonomously (detect → verify → consensus → escalate)
byzantine_consensus.py → Trust nothing, verify everything (PBFT)
cryptographic_proof.py → Remember immutably (Ed25519 + Merkle + audit chain)
data_sources.py      → Mock data and public dataset references
mesh_network.py      → Peer-to-peer sync
adoption_tracker.py  → Node registration and stats
app.py               → The interface to all of it
```

**The loop:**

```
Observe → Believe → Predict → Act → Observe again → Correct → Repeat
```

## API

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Is the system running |
| `GET /api/status` | Honest system status |
| `GET /api/violations` | Current violations (mock data, labeled) |
| `POST /api/autonomous/submit` | Submit evidence for autonomous processing |
| `GET /api/autonomous/status` | Agent system status |
| `GET /api/autonomous/rules` | Immutable rules (transparency) |
| `GET /api/autonomous/escalations` | Escalation queue |
| `GET /api/autonomous/audit` | Audit trail with chain verification |
| `GET /api/world/status` | World model status |
| `GET /api/world/beliefs` | Current beliefs (filterable) |
| `GET /api/world/flourishing` | Flourishing scores by scope |
| `POST /api/world/observe` | Submit sensor measurements |
| `GET /api/world/corrections` | Every time the model self-corrected |
| `GET /api/world/discover` | Anomalies and discovered patterns |

## Flourishing Metrics

The system defines flourishing differently for different scopes:

- **Humans**: health, autonomy, fairness, opportunity
- **Animals**: health, safety, comfort, natural behavior
- **Ecosystems**: biodiversity, stability, resilience

Weights are not fixed. The model updates them as it learns what actually correlates with good outcomes.

## Contributing

This project needs honest contributors. If you want to help:
1. Connect a real sensor to a real public dataset
2. Write a proper data source with full attribution and uncertainty bounds
3. Open a PR

## License

[Add actual license here]

---

*Previously, this repository contained fabricated claims about deployment scale, government partnerships, governance boards, and violation data. Those claims have been removed. This README reflects only what is verifiably true. The system is always wrong somewhere — it knows this, and it keeps correcting.*
