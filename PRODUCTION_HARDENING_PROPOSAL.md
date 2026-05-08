# Production Hardening Proposal

Status: proposal for pre-live hardening.

This system should borrow security posture from mature open-source systems:

- Kubernetes-style admission control before any state-changing or autonomous action.
- Sigstore/Rekor-style signed records and transparency logs for releases, node admission, and high-impact claims.
- TUF-style threshold authority for node admission, immutable rule changes, and release trust.
- Mastodon/ActivityPub-style federation boundaries: public peers can speak, but only admitted identities can affect trust.

The goal is not to make every node omnipotent or universally trusted. The goal is
to make untrusted input visible, bounded, reviewable, and unable to become an
authoritative fact or autonomous escalation without independent admitted support.

## Threat Model

Assume these attackers exist:

- A forked project that clones the repository and claims to be official.
- A compromised write token.
- A public demo node with `HFF_ALLOW_PUBLIC_WRITES=true` accidentally left on.
- An aggressive autonomous agent that tries to create alarming escalations from weak evidence.
- A mesh peer that repeats false violations until they appear verified.
- A bad actor who submits model/API text designed to mislead readers or execute in the dashboard.
- A denial-of-service caller that sends large JSON bodies, large batches, or repeated writes.

## Required Controls

### 1. Admission Control For Writes

Every state-changing endpoint should pass an explicit admission pipeline before
it mutates durable state:

```text
request -> size/rate limits -> schema validation -> source admission
        -> evidence quality checks -> capability grant check -> state update
```

World observations may update tentative beliefs. They must not directly create
accepted facts, verified incidents, admitted nodes, or locked escalations.

### 2. Observe-Only Autonomy By Default

Autonomous evidence submission should default to `observe_only`.

Modes:

| Mode | Behavior |
|---|---|
| `observe_only` | Stores draft evidence and model observations only. No consensus lock. |
| `review_required` | Allows escalation proposals, but requires an explicit review grant before lock. |
| `limited_autonomy` | Allows locking only when accepted facts, admitted-node quorum, and capability grants all pass. |

No default public deployment should execute the Detect -> Verify -> Consensus ->
Lock path from one tokened request on a single node.

### 3. Signed Node Admission

Visible nodes are not trusted nodes. Mesh peers and adoption registrations should
remain telemetry until admitted by a signed membership record.

Admission records should include:

- node public key
- admitted scope
- version or release attestation
- operator/diversity metadata, when appropriate
- expiration or renewal policy
- revocation path
- signatures from threshold authorities

Only admitted, non-expired nodes may count toward security quorum, accepted
facts, or mesh verification.

### 4. Source-Independent Belief Promotion

Belief confidence may approach a statistical 100 percent horizon over repeated
reinforcement, but accepted facts require source independence.

A belief may become an accepted fact only when:

- confidence is above the accepted-fact threshold
- minimum evidence count is met
- all configured required confirming nodes agree
- those nodes are admitted for the relevant scope
- no active contradiction or unresolved challenge is present

Immutable constraints are a separate category. They can be loaded as
constitutional rules, but changing them should require threshold authority and a
signed audit event.

### 5. Safe Dashboard Rendering

The dashboard must treat model output, peer payloads, observations, source names,
agent descriptions, scopes, and violation descriptions as untrusted text.

Required rule:

```text
remote/model/API strings render as textContent or escaped HTML, never raw innerHTML
```

This protects the official UI from stored output injection and from hostile text
that tries to impersonate system authority.

### 6. Bounded Write Surfaces

Before live use, add hard limits:

- maximum request body size
- maximum observation batch size
- maximum evidence text length
- maximum source/scope/entity string length
- maximum pagination limits
- per-token and per-IP rate limits for mutating endpoints
- bounded background polling intervals

A compromised token should be able to do limited damage, not fill SQLite or pin
CPU indefinitely.

### 7. Mesh Trust Is Not Repetition

Mesh sync should never treat repeated identical claims as independent
verification.

Peer payloads should require:

- admitted peer identity
- payload signatures
- replay protection
- source independence checks
- scope-specific trust
- audit logging of who supplied which claim

Unadmitted peers may contribute suggestions or challenges, but they must not
increase verification counters that imply trust.

## Proposed Implementation Order

1. Add request body, batch, string, and rate limits around all write endpoints.
2. Escape or text-render all dashboard strings derived from models, peers, or API data.
3. Add `HFF_AUTONOMY_MODE=observe_only` as the default and stop autonomous submit from locking escalations unless explicitly elevated.
4. Require accepted-fact and admitted-node gates before escalation lock.
5. Add signed node admission records and make mesh/adoption trust depend on them.
6. Add signed transparency events for accepted facts, immutable rule changes, node admission, and releases.
7. Expand tests around compromised-token, public-write, rogue-peer, and output-injection scenarios.

## Non-Goals

- Do not make public forks illegal or technically impossible.
- Do not claim that GitHub branches, visible nodes, or demo traffic are authority.
- Do not let a single model, token, peer, or operator-free background loop create irreversible external action.
- Do not contact regulators, deploy services, admit nodes, rotate keys, or publish official claims without explicit grants.

## Minimal Pre-Live Bar

Before enabling public live writes or autonomous escalation, the repository
should at minimum have:

- closed-by-default write endpoints with limits
- safe dashboard rendering
- observe-only default autonomy
- accepted-fact gates tied to admitted-node confirmation
- mesh verification that requires signed admitted peers
- tests proving rogue inputs remain bounded and non-authoritative
