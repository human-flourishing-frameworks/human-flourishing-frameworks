# Lantern — Local-First AI Chat + Media Curator for Households

Privacy-first chat stack with integrated media curation: desktop, browser, and dashboard surfaces. Local STT (Vosk), bounded Discord adapter, CC-licensed + synthetic audio library, educational audiobooks + podcasts, and Lantern Kids edition with parental review.

→ **[Foundry Master Plan](../gm-agent-orchestrator/FOUNDRY-PLAN.md)** — shared org model, revenue model, 22 product streams (Lantern is streams #1–4)

## Live URLs

| Surface | URL |
|---|---|
| HFF Dashboard (live) | https://human-flourishing-frameworks.onrender.com/ |
| Lantern OS Dashboard | https://human-flourishing-frameworks.onrender.com/os |
| Art Panels v2 | https://human-flourishing-frameworks.onrender.com/art |
| Health API | https://human-flourishing-frameworks.onrender.com/health |
| System Status API | https://human-flourishing-frameworks.onrender.com/api/status |
| Source Code | https://github.com/human-flourishing-frameworks/human-flourishing-frameworks |

## Product Editions

- **Lantern Desktop** — full chat + media curator, CustomTkinter + Vosk STT (`apps/lantern-desktop/lantern_desktop.py`)
- **Lantern Browser** — same chat, no install required
- **Lantern Dashboard** — local Flask service + Anthropic API bridge
- **Lantern OS Dashboard** — full system view: orchestrator, games, apps, notes, media, art panels
- **Lantern Kids** — age-gated, parental review, no external bridges
- **Lantern Media Curator** — CC-licensed audio, audiobooks, podcasts, video (internet archive + Wikimedia + public domain)
- **Art Panels** — pixel-level CSS art (Lantern Glow, RAG House, Seven Anchors, Convergence Stream)

## What it does

- Local AI chat (no cloud by default; optional Anthropic bridge)
- Continuous speech-to-text (Vosk, bounded window)
- Curated media library: bird calls (Xeno-Canto), classical music (IMSLP), public domain audiobooks (Gutenberg)
- Synthetic soundscapes (stdlib procedural generation, zero ML)
- Parental controls (Kids edition) with explicit curation
- Works offline, respects privacy

## Quick start

```bash
python apps/lantern-desktop/lantern_desktop.py
```

Or run the browser version (if Flask service is running):
```
http://localhost:8765
```

## Local Services (cross-repo)

Services started from the [`lantern-os`](https://github.com/alex-place/lantern-os) repo:

| Service | Port | Status | URL |
|---------|------|--------|-----|
| Lantern Garage | `4177` | Running | http://127.0.0.1:4177 |
| GPT Web API | `3000` | Running | http://127.0.0.1:3000 |
| Discord Radio Bot | — | Needs token | `apps/lantern-discord-radio/bot.py` |

Health check:
```bash
curl http://127.0.0.1:3000/health   # GPT Web API
curl http://127.0.0.1:4177/         # Lantern Garage
```

## Media Library Attribution

See `~/.lantern/sounds/ATTRIBUTION.md` for full CC-license provenance, source URLs, and recordist credits for all audio files.

**Real recordings:** Blue Whale (Wikimedia), Brown Thrasher (Xeno-Canto XC136055), Frogs, Red Fox, Bach BWV 543, Mozart Eine kleine Nachtmusik, regional music  
**Synthetic:** 12 procedural pads (stdlib: scipy, numpy, wave module — no ML, no voice cloning)

## What is intentionally NOT here

- No autonomous medical, legal, or financial advice surfaces
- No covert resource usage
- No production cloud deployment claims
- No overstated IP or patent claims
- No private household content
- No mental health therapy framing

## License

[TBD — AGPL base + proprietary for Kids edition]

---

**Status:** TRL 4 (desktop + browser functional; Kids edition TRL 2)  
**Next:** [Read FOUNDRY-PLAN.md for full org model and revenue plan](../gm-agent-orchestrator/FOUNDRY-PLAN.md)
operator-reviewed
bounded by explicit grants
challengeable
rollback-aware
advisory by default
```

The system must not be described as a production governance authority, moral oracle, surveillance system, enforcement system, or autonomous controller of people.

## What this actually is

A bounded framework for measuring, modeling, and improving outcomes across beings and systems:

- **Sensors** observe outcomes with uncertainty, provenance, and coverage gaps.
- **World model** maintains Bayesian beliefs and updates estimates as measurements arrive.
- **Live sensors** exist but are opt-in with `ENABLE_LIVE_SENSORS`; they are not enabled by default.
- **Autonomous agents** are experimental advisory/research workflows for detecting evidence, verifying records, proposing consensus, and creating audit-backed escalations. They are not public enforcement authority.
- **PBFT consensus** is currently a teaching/research implementation, not hardened production consensus.
- **Ed25519 signing and audit-chain logic** provide tamper-evidence, not tamper-proof storage.
- **Node adoption telemetry** reports liveness/visibility, not trust or authority.
- **Mesh sync** is opt-in and must remain default-closed for write-like behavior.

## What this is not

- Not production-ready governance infrastructure.
- Not a government, court, regulator, standards body, medical authority, legal authority, or financial authority.
- Not endorsed by any government, university, or standards body.
- Not a system for monitoring, policing, ranking, controlling, or enforcing decisions about people.
- Not tracking real violations as authoritative incidents; demo violations are synthetic unless explicitly labeled otherwise.
- Not a truth oracle; claims should be source-backed with confidence and uncertainty.
- Not omniscient; the model only knows what sensors and seed data provide.
- Not a self-repairing deployment system. Operators still control deploys, secrets, and recovery.
- Not proof that visible nodes are verified or security-relevant.
- Not a human transportation, substrate-transfer, or private-symbol system.

## Public surface and accessibility posture

See:

- [`docs/internationalization-and-accessibility.md`](./docs/internationalization-and-accessibility.md)
- [`policies/foundry-user-repo-hardening.v1.json`](./policies/foundry-user-repo-hardening.v1.json)

Key rules:

- public does not mean uncontrolled;
- token-gated does not mean safe;
- consent does not mean permanent;
- a signal does not equal the person;
- APKs/mobile apps are not public by default;
- vehicle control is outside current allowed scope.

## Current state

| Component | Status |
|---|---|
| Flask app + dashboard | Render primary surface; validate with fresh smoke evidence |
| Docker/gunicorn | Uses `${PORT:-5000}` for cloud/local binding |
| Sensor framework | Built |
| Live public API sensors | Implemented, opt-in via `ENABLE_LIVE_SENSORS` |
| Bayesian world model | Built and seeded with cited measurements |
| Autonomous agents | Implemented as bounded research/advisory workflows |
| PBFT consensus | Teaching implementation; happy path only |
| Cryptographic signing | Ed25519 via `cryptography` |
| Audit trail | Tamper-evident hash/audit chain |
| Mesh sync | HTTP peer sync, opt-in via `ENABLE_MESH_SYNC` |
| Adoption telemetry | Self-reported liveness, opt-in via `ENABLE_ADOPTION_SYNC` |
| Demo violations | Synthetic and labeled |

## Quick start

```bash
git clone https://github.com/human-flourishing-frameworks/human-flourishing-frameworks.git
cd human-flourishing-frameworks
pip install -r requirements.txt
python app.py
```

Visit:

```text
http://localhost:5000
```

Docker:

```bash
docker build -t hff .
docker run --rm -p 5000:5000 -e PORT=5000 hff
```

## Configuration

Optional node metadata can help show distribution without publishing raw IP addresses.

| Variable | Default | Purpose |
|---|---|---|
| `NODE_NAME` | `node-<uuid>` | Display name |
| `PLATFORM` | `web` | Runtime surface, such as `web`, `docker`, or `local-dev` |
| `NODE_REGION` | empty | Optional self-reported region or location label |
| `OPERATOR_TYPE` | empty | Optional self-reported operator class, such as `independent`, `lab`, or `cloud` |
| `DEPLOYMENT_TYPE` | empty | Optional self-reported deployment type, such as `railway`, `docker`, or `local` |
| `NODE_PUBLIC_KEY` | generated node key | Node identity key advertised for future admission checks |
| `MIN_CONSENSUS_NODES` | `3` | Minimum verified active nodes needed before consensus can be security-backed |
| `HFF_WRITE_TOKEN` | empty | Privileged token for production state-changing writes |
| `HFF_ADOPTION_ACCEPT_TOKEN` | empty | Lower-privilege token accepted by the central service for adoption telemetry |
| `HFF_ADOPTION_SYNC_TOKEN` | empty | Lower-privilege token used by reporting nodes when posting adoption telemetry |
| `HFF_ALLOW_PUBLIC_WRITES` | empty/false | Demo override that reopens public writes; do not enable on production services |
| `ENABLE_ADOPTION_SYNC` | empty/false | Opt in to posting node liveness metadata to `CENTRAL_SERVER` |
| `CENTRAL_SERVER` | `https://human-flourishing-frameworks.onrender.com` | Adoption telemetry target when sync is enabled |
| `ENABLE_MESH_SYNC` | empty/false | Opt in to background peer mesh sync |
| `ENABLE_LIVE_SENSORS` | empty/false | Opt in to polling external public APIs in the live sensor loop |

To make a local node visible to a central adoption tracker, run it with:

```text
ENABLE_ADOPTION_SYNC=true
CENTRAL_SERVER=<central-service-url>
HFF_ADOPTION_SYNC_TOKEN=<adoption-only-token>
```

The central service should have:

```text
HFF_ADOPTION_ACCEPT_TOKEN=<matching-adoption-only-token>
```

Do not distribute `HFF_WRITE_TOKEN` to reporting nodes. It is reserved for privileged local/admin writes such as autonomous submissions and manual world-model observations.

## API

| Endpoint | Purpose |
|---|---|
| `GET /health` | Health probe |
| `GET /api/status` | Honest system status |
| `GET /api/violations/compas` | Summary of the ProPublica COMPAS analysis (real public dataset) |
| `POST /api/adoption/register` | Register node liveness telemetry; requires adoption grant |
| `GET /api/adoption/stats` | Adoption/liveness statistics |
| `GET /api/adoption/nodes` | Recent visible nodes |
| `POST /api/autonomous/submit` | Submit evidence for autonomous processing; requires write grant |
| `GET /api/autonomous/status` | Agent system status |
| `GET /api/autonomous/rules` | Public rules projection endpoint |
| `GET /api/autonomous/escalations` | Escalation queue |
| `GET /api/autonomous/audit` | Audit trail with chain verification |
| `GET /api/world/status` | World model status |
| `GET /api/world/beliefs` | Current beliefs, filterable |
| `GET /api/world/flourishing` | Flourishing scores by scope |
| `POST /api/world/observe` | Submit sensor measurements; requires write grant |
| `GET /api/world/corrections` | Model self-correction history |
| `GET /api/world/discover` | Anomalies and discovered patterns |

State-changing endpoints are closed by default. In production, send:

```text
Authorization: Bearer <HFF_WRITE_TOKEN>
```

or:

```text
X-HFF-Write-Token: <HFF_WRITE_TOKEN>
```

for privileged writes. Adoption telemetry should use:

```text
Authorization: Bearer <HFF_ADOPTION_ACCEPT_TOKEN>
```

or:

```text
X-HFF-Adoption-Token: <HFF_ADOPTION_ACCEPT_TOKEN>
```

Only set `HFF_ALLOW_PUBLIC_WRITES=true` for local demos or disposable test nodes.

## Architecture

```text
sensors.py              -> observe reality with uncertainty
live_sensors.py         -> optional public API polling
world_model.py          -> Bayesian belief tracking and correction
agent_system.py         -> autonomous detection / verification / escalation
byzantine_consensus.py  -> PBFT-inspired teaching implementation
cryptographic_proof.py  -> Ed25519 signatures and audit-chain utilities
data_sources.py         -> mock data and public dataset references
mesh_network.py         -> opt-in peer-to-peer sync
adoption_tracker.py     -> node liveness registration and stats
app.py                  -> Flask interface
wsgi.py                 -> WSGI entrypoint for production servers when used
```

The loop:

```text
Observe -> Believe -> Predict -> Propose -> Act only when explicitly enabled -> Observe again -> Correct -> Repeat
```

## Node security model

The node network separates visibility from authority:

- **Visible node:** self-reported liveness telemetry, useful for adoption and debugging.
- **Verified node:** admitted by operator-approved or system-approved policy, with a stable identity key.
- **Security node:** verified and recently active; eligible to count toward quorum/security.
- **Forked node:** allowed to run public code, but unaffiliated until admitted.

Near-term rule:

```text
unverified nodes can be counted publicly
verified active nodes count for security
forks are not authoritative unless admitted
```

Future admission should require node keys, version attestation, operator/diversity metadata, revocation support, and an audit event.

## Authority and releases

The GitHub repository is a code proposal surface. A push, branch update, merge, or README edit is not by itself an authoritative operational decision.

Capability-control rules are defined in [`CAPABILITY_CONTROL.md`](./CAPABILITY_CONTROL.md). The system should not hold broad dangerous capabilities by default; dangerous actions require narrow, temporary, audited grants.

Current safety and public-boundary documents include:

- [`SOURCE_CLASSIFICATION_POLICY.md`](./SOURCE_CLASSIFICATION_POLICY.md): reliance should be source-backed with confidence, not treated as absolute truth.
- [`DEPLOYMENT_AUTONOMY_BOUNDARY.md`](./DEPLOYMENT_AUTONOMY_BOUNDARY.md): deployment and recovery remain operator/governance controlled.
- [`PUBLIC_DEPLOYMENT_STRATEGY.md`](./PUBLIC_DEPLOYMENT_STRATEGY.md): Railway is a hosting adapter, not the architecture; public surfaces should stay portable and default-closed.
- [`HUMAN_TRANSPORTATION_BOUNDARY.md`](./HUMAN_TRANSPORTATION_BOUNDARY.md): human-preserving traversal claims require canary, quarantine, continuity, consent, and return evidence.
- [`docs/internationalization-and-accessibility.md`](./docs/internationalization-and-accessibility.md): translation, accessibility, plain-language, and jurisdiction-sensitive public-readiness posture.
- [`policies/foundry-user-repo-hardening.v1.json`](./policies/foundry-user-repo-hardening.v1.json): baseline anti-drift policy for foundry user repositories.
- [`docs/foundry-4m-20-operator-master-plan.md`](./docs/foundry-4m-20-operator-master-plan.md): plain-language 20-operator start plan with resource consent gates.

Authoritative actions require explicit operator approval, especially:

- deploying or redeploying public services;
- changing public claims about node counts, governance, or verification;
- treating `master` as the live truth source;
- moving from self-reported telemetry to verified telemetry;
- announcing a node, report, or consensus result as independently validated.

Today, the operator manages production keys and deployment authority. Any future system-managed key path needs audited key rotation, rollback, recovery, least-privilege access, operator break-glass recovery, and verified multi-node consensus over key changes.

If the running public service and GitHub disagree, say so plainly and treat the running service plus operator approval as the authority until a deliberate release is made.

## Flourishing metrics

The system defines flourishing differently for different scopes:

- **Humans:** health, autonomy, fairness, opportunity
- **Animals:** health, safety, comfort, natural behavior
- **Ecosystems:** biodiversity, stability, resilience

Weights are not fixed. The model updates estimates as configured data and methods change.

These metrics are advisory and value-laden. They are not a ranking of people, cultures, or moral worth. They should be interpreted with source confidence, uncertainty, affected-party context, and challenge paths.

## Contributing

Useful contributions:

1. Connect a real sensor to a real public dataset.
2. Write a data source with attribution and uncertainty bounds.
3. Add tests for auth boundaries, world-model updates, audit-chain verification, and deployment health.
4. Open a focused PR.

## License

No production-use license has been finalized yet. Until an explicit license is added, treat the repository as source-visible research software rather than a broadly licensed production framework.

---

This README should describe only verifiable current behavior. Remove or correct anything that becomes stale.
