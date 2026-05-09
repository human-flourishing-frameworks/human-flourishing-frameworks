# Deployment Autonomy Boundary

Status: docs/data-contract policy.

This document defines the boundary between helpful deployment assistance and an
unsafe self-repairing deployment system.

It is intentionally docs-only. It adds no deploy hooks, secrets access,
credentials, endpoints, polling, infrastructure automation, rollback automation,
or autonomous recovery behavior.

## Core boundary

HFF is not a self-repairing deployment system.

Operators still control:

```text
deploys
secrets
runtime environment variables
production configuration
rollbacks
recovery decisions
data restoration
incident command
public release validation
```

The system may assist operators, but it must not silently become the operator.

## Why this matters

Self-repairing behavior can look beneficial while increasing risk:

```text
faster remediation -> hidden autonomous privilege
automatic rollback -> data loss or state mismatch
auto-secret rotation -> lockout or leakage
auto-config changes -> drift from reviewed state
auto-restart loops -> mask root causes
auto-migration -> irreversible corruption
auto-deploy -> unreviewed code reaching production
```

The safety goal is not zero automation. The safety goal is bounded, observable,
operator-controlled automation.

## Allowed assistance

HFF may help with deployment and recovery by producing:

- diagnostics;
- checklists;
- suggested commands;
- smoke-test plans;
- rollback recommendations;
- risk summaries;
- incident notes;
- PRs that humans review;
- release readiness assessments;
- operator-facing confidence tables.

Allowed assistance remains advisory unless an operator explicitly executes it.

## Forbidden autonomous behavior

HFF must not autonomously:

- deploy to production;
- push, merge, or force-push deployment branches without explicit operator approval;
- modify secrets;
- read or exfiltrate secrets;
- rotate credentials;
- change Railway or hosting configuration;
- change production environment variables;
- run destructive database commands;
- restore or overwrite production data;
- run migrations against production;
- roll back production;
- restart production services;
- disable monitoring or security controls;
- suppress alerts;
- create persistence mechanisms;
- self-escalate permissions;
- mark itself release-validated.

## Allowed reliance levels

Deployment facts should use the source reliance ladder from
`SOURCE_CLASSIFICATION_POLICY.md`.

Examples:

| Claim | Maximum reliance without operator validation |
|---|---:|
| Local tests passed | 3 Corroborated claim |
| GitHub Actions passed | 3 Corroborated claim |
| A PR is mergeable | 3 Corroborated claim |
| Local node started | 3 Corroborated claim |
| Public service health is good | 2 Source-backed claim until checked against deployed SHA |
| Production release is validated | 5 High-impact fact requiring operator review |
| Recovery is complete | 5 High-impact fact requiring operator review |

## Required release validation

A release is not validated merely because:

```text
local tests pass
CI passes
a PR merges
a local node starts
an endpoint once returned 200
an LLM says it is ready
```

Release validation requires at minimum:

```text
deployed commit SHA recorded
/health verified on deployed service
/api/status verified on deployed service
relevant safety endpoints checked
runtime flags audited
operator confirms deploy target and environment
```

## Recovery boundary

During an incident, HFF may recommend a recovery sequence but must not execute it
without the operator.

Preferred flow:

```text
detect signal
classify severity
summarize evidence
recommend lowest-risk action
show rollback/forward-fix options
ask operator to execute
record what happened
```

Forbidden flow:

```text
detect signal
autonomously change production
autonomously change secrets
autonomously restore data
autonomously suppress alert
declare incident resolved
```

## Secret boundary

Secrets are operator-controlled.

HFF should not request, store, print, infer, rotate, or transmit secrets. If a
future integration requires secrets, it must use scoped platform mechanisms and
human approval before any runtime change.

## Configuration boundary

Runtime flags that affect autonomy or write surfaces must remain explicit:

```text
ENABLE_LIVE_SENSORS=false unless approved
ENABLE_MESH_SYNC=false unless approved
ENABLE_AUTONOMOUS_ESCALATION_EXECUTOR=false unless approved
HFF_ALLOW_PUBLIC_WRITES=false unless approved
```

No recovery flow may silently flip these flags.

## Human operator authority

The operator has final authority over:

```text
whether to deploy
whether to roll back
whether to rotate secrets
whether to restore data
whether to mark release validated
whether to close an incident
```

HFF may disagree, warn, or recommend, but it must not override.

## Future work gate

Before adding any deployment or recovery automation, a PR must answer:

1. What exact action can the system take?
2. What permission does it require?
3. What state can it read?
4. What state can it write?
5. Can it touch secrets?
6. Can it affect production?
7. Can it be undone?
8. What logs are produced?
9. What operator approval is required?
10. How is the automation disabled?

Default posture:

```text
assist operators
prepare evidence
recommend actions
never self-repair production
```
