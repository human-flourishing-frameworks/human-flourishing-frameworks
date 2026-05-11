# BetterSafe Pilot Scorecard

Status: controlled limited pilot launch scorecard.

Related: issues #117 and #120; docs/bettersafe-pilot-accelerator.md; docs/bettersafe-pilot-launch-record.md.

This scorecard permits only the controlled limited pilot slice described in `docs/bettersafe-pilot-launch-record.md`. It does not authorize broad release, high-impact deployment, runtime autonomy, hidden telemetry, child-facing public surfaces, raw transcript storage by default, live sensors by default, public writes, payments, emergency authority, surveillance, physical-world control, identity-continuity claims, or repo-consciousness claims.

## Current decision

```text
Decision: GO — CONTROLLED LIMITED PILOT ONLY
Reason: launch-control docs now define scope fence, source labels, grounding disclosure, correction ledger, privacy boundary, human controls, high-impact blockers, red-team prompts, operator runbook, stop conditions, and expansion block.
Expansion: BLOCKED until a new scorecard records PASS evidence for the expanded slice.
```

## Scorecard

| Gate | Status | Evidence |
|---|---|---|
| CI status | `PASS_PENDING_CURRENT_PR` | PR #123 passed `tests` and `convergence-validation`; launch-control PR must also pass both before merge. |
| Convergence validation | `PASS_PENDING_CURRENT_PR` | Prior launch accelerator passed; launch-control PR must pass before merge. |
| Scope fence | `PASS` | `docs/bettersafe-pilot-launch-record.md` allows only low-risk claim audit, source-checking, repo/docs reasoning, education, low-risk planning, confidence-label exercises, scientific-method convergence exercises, and bounded creative play. |
| Source labels | `PASS` | Launch record requires `FACT_SOURCE_BACKED`, `FACT_OPERATOR_REPORTED`, `INFERENCE`, `HEURISTIC_CONFIDENCE`, `SPECULATION`, `UNKNOWN`, `CORRECTED`, `RETRACTED`, or `BLOCKED`. |
| Grounding disclosure | `PASS` | Launch record and operator runbook require `FULL_REPO_GROUNDED`, `LIMITED_CHAT_LOCAL`, or `UNAVAILABLE_OR_DEGRADED`; default is `LIMITED_CHAT_LOCAL` unless verified. |
| Correction ledger | `PASS` | `docs/bettersafe-pilot-correction-ledger.md` defines `CORRECTED`, `RETRACTED`, `UNKNOWN`, and `BLOCKED` entries. |
| Privacy boundary | `PASS` | `docs/bettersafe-pilot-privacy-control-notice.md` blocks raw transcript storage by default, hidden profiling, surveillance, people scoring, child-data collection, and live sensors by default. |
| Human control | `PASS` | Launch record, privacy/control notice, and operator runbook require pause, stop, correct, retract, revoke, and rollback paths. |
| High-impact blocker | `PASS` | Launch record and runbook block or downgrade medical/legal/financial/minor/caregiver/crisis/surveillance/payment/public-write/physical-control surfaces. |
| Red-team pack | `PASS` | `docs/bettersafe-red-team-prompts.md` covers source-label, grounding, medical, financial, minor-adjacent, crisis, privacy, autonomy, speculation, and correction pressure. |
| Operator runbook | `PASS` | `docs/bettersafe-pilot-operator-runbook.md` defines start, pause, stop, correction, rollback, and evidence-recording steps. |

## Expansion rule

```text
All required gates must be PASS or explicitly NOT_APPLICABLE with evidence.
Any UNKNOWN_OR_BLOCKED, PENDING, FAIL, or PASS_PENDING_CURRENT_PR status blocks merge or expansion until resolved.
The current GO decision applies only after the launch-control PR passes tests and convergence-validation.
```

## Current pilot state after launch-control merge

```text
Pilot state: CONTROLLED LIMITED PILOT
Expansion state: BLOCKED
Public high-impact state: BLOCKED
Runtime autonomy: BLOCKED
Raw transcript storage by default: BLOCKED
Hidden profiling: BLOCKED
Surveillance/scoring: BLOCKED
Live sensors by default: BLOCKED
Public writes by default: BLOCKED
Payments/emergency/physical control: BLOCKED
```

## Known follow-up items

```text
1. Run and record red-team evidence for the first actual pilot slice.
2. Record each pilot slice using the operator runbook evidence template.
3. Keep correction ledger current.
4. Open a new PR before any expansion beyond the allowed pilot slice.
5. Keep full unittest CI and convergence-validation green.
```

## Score labels

```text
PASS = evidence exists and is current
PASS_PENDING_CURRENT_PR = prior evidence exists, but the current launch-control PR must pass before merge
FAIL = evidence contradicts the gate
PENDING = work not complete
UNKNOWN_OR_BLOCKED = current evidence is unavailable, stale, or blocked by known failure
NOT_APPLICABLE = gate does not apply to this pilot slice, with reason recorded
```

## Boundary

The scorecard is a launch-control decision aid. A passing scorecard permits only the documented low-risk BetterSafe pilot slice, not broad release, high-impact deployment, runtime autonomy, production authority, or identity claims.
