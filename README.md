# Human Flourishing Frameworks

**An experimental advisory and orchestration framework for source-backed modeling, safety boundaries, and human-flourishing system design.**

> **Status:** early development experimental software. A public deployment is validated only by fresh, surface-specific smoke evidence; it is not production authority infrastructure. Measurements carry uncertainty, node counts are self-reported unless explicitly verified, and GitHub changes are code proposals until deliberately deployed and validated.

Plain-language summary:

HFF is a research and advisory framework for testing source-backed modeling, recovery workflows, deployment boundaries, and human-centered system design. It is not a government, enforcement system, autonomous authority, or production critical infrastructure.

## Current deployment

Primary cloud URL:

```text
https://human-flourishing-frameworks.onrender.com/
```

Health/status checks:

```bash
curl -i https://human-flourishing-frameworks.onrender.com/health
curl -i https://human-flourishing-frameworks.onrender.com/api/status
```

The container is started with gunicorn and binds to the injected `PORT`, falling back to `5000` for local Docker runs.

Railway may appear in older logs or historical deploys, but Render is the primary public surface currently covered by the repo smoke scripts.

Public deployment claims should always be backed by fresh smoke evidence because deployments, routes, and hosting providers can drift over time.

## Capability and authority boundary

HFF can support more than passive research workflows, but capability is not authority.

HFF can help:

- model sources, uncertainty, evidence, risks, and candidate actions;
- run bounded local or deployment-support workflows when explicitly enabled and operator-reviewed;
- support operator-reviewed decisions with logs, tests, and audit evidence;
- expose status, beliefs, synthetic demos, and advisory results;
- test safety boundaries, release posture, and system convergence.

HFF does not have public authority over people, communities, institutions, or living systems.

Public-facing use should remain:

```text
source-backed
uncertainty-aware
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
- Not a human transportation, substrate-transfer, or cosmic-door system; those topics are documented only as safety boundaries and evidence classifications.

## Public surface and accessibility posture

See:

- [`docs/public-surface-policy.md`](./docs/public-surface-policy.md)
- [`docs/internationalization-and-accessibility.md`](./docs/internationalization-and-accessibility.md)

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

## License

No production-use license has been finalized yet. Until an explicit license is added, treat the repository as source-visible research software rather than a broadly licensed production framework.

---

This README should describe only verifiable current behavior. Remove or correct anything that becomes stale.
