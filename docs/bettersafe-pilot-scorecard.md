# BetterSafe Pilot Scorecard

Status: pilot scorecard template.

Related: issues #117 and #120; docs/bettersafe-pilot-accelerator.md.

This scorecard must be completed before any BetterSafe pilot slice expands beyond internal low-risk testing.

## Current decision

```text
Decision: DO NOT BROADEN YET
Reason: pilot gates require documented evidence, green or explicitly triaged CI, correction path, privacy boundary, and human-control path.
```

## Scorecard

| Gate | Status | Evidence required before expansion |
|---|---|---|
| CI status | `UNKNOWN_OR_BLOCKED` | Full tests pass, or known unrelated failures are logged with owner and follow-up issue. |
| Convergence validation | `UNKNOWN_OR_BLOCKED` | Latest convergence-validation workflow passes on the pilot PR or master. |
| Scope fence | `PENDING` | Pilot surfaces are limited to claim audit, source-checking, education, repo reasoning, low-risk planning, and bounded creative play. |
| Source labels | `PENDING` | Serious claims expose a label from the approved source-label set. |
| Grounding disclosure | `PENDING` | Durable/high-impact claims show `FULL_REPO_GROUNDED`, `LIMITED_CHAT_LOCAL`, or `UNAVAILABLE_OR_DEGRADED`. |
| Correction ledger | `PENDING` | Challenged unsupported claims can be marked corrected, retracted, unknown, or blocked. |
| Privacy boundary | `PENDING` | No raw transcript storage by default; no hidden profiling or surveillance. |
| Human control | `PENDING` | Pause, stop, revoke, correct, and rollback paths are documented. |
| High-impact blocker | `PENDING` | Medical/legal/financial/minor/caregiver/crisis-adjacent surfaces block or downgrade. |
| Red-team pack | `PENDING` | Prompts test overclaiming, speculation, degraded grounding, privacy, and high-impact pressure. |
| Operator runbook | `PENDING` | Start, pause, rollback, correction, incident, shutdown, and evidence-recording steps exist. |

## Expansion rule

```text
All required gates must be PASS or explicitly NOT_APPLICABLE with evidence.
Any UNKNOWN_OR_BLOCKED, PENDING, or FAIL status blocks expansion.
```

## Known follow-up items

```text
1. Keep full unittest CI green or record exact unrelated failures.
2. Add a correction ledger process or file.
3. Add a privacy/user-control pilot notice.
4. Add red-team prompts for release labels, grounding, and high-impact downgrade.
5. Add operator runbook for start/pause/rollback/shutdown.
```

## Score labels

```text
PASS = evidence exists and is current
FAIL = evidence contradicts the gate
PENDING = work not complete
UNKNOWN_OR_BLOCKED = current evidence is unavailable, stale, or blocked by known failure
NOT_APPLICABLE = gate does not apply to this pilot slice, with reason recorded
```

## Boundary

The scorecard is a decision aid, not launch approval. A passing scorecard permits only the specific documented low-risk pilot slice, not broad release, high-impact deployment, or autonomous operation.
