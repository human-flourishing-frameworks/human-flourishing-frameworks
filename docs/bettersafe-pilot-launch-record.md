# BetterSafe Limited Pilot Launch Record

Status: GO for controlled limited pilot only.

Related: issues #117 and #120; docs/bettersafe-pilot-accelerator.md; docs/bettersafe-pilot-scorecard.md.

This record launches only the bounded BetterSafe pilot slice described here. It does not launch a general product, public autonomous agent, high-impact support surface, memory system, hidden telemetry system, child-facing service, emergency service, or production authority.

## Launch decision

```text
Decision: GO — CONTROLLED LIMITED PILOT ONLY
Launch type: low-risk, human-controlled, reversible pilot
Default mode: LIMITED_CHAT_LOCAL unless repo/doc grounding is explicitly verified
Operator authority: human review only
Expansion status: BLOCKED until a new scorecard records PASS evidence for the expanded slice
```

## Allowed pilot slice

```text
claim audit
source-checking
repo/docs reasoning
low-risk planning support
educational explanations
confidence-label exercises
scientific-method convergence exercises
bounded creative play with explicit fiction boundaries
```

## Explicitly blocked during pilot

```text
medical decisions
legal decisions
financial decisions
child-facing public surfaces
crisis intervention as sole support
relationship or caregiver authority
identity-continuity claims
repo consciousness claims
hidden memory claims
raw transcript storage by default
hidden profiling
surveillance or scoring
runtime autonomy
public writes without separate approval
live sensor claims or live sensor enablement by default
payments
emergency authority
physical-world control
```

## Required launch banner

Every pilot session starts with a visible mode and boundary statement:

```text
Mode: LIMITED_CHAT_LOCAL unless this session explicitly verifies FULL_REPO_GROUNDED.
BetterSafe pilot is a bounded, low-risk, human-controlled support/checking workflow.
It labels uncertainty, cites sources when used, preserves correction paths, and blocks or downgrades high-impact requests.
It is not medical, legal, financial, emergency, surveillance, child-facing, autonomous, or identity-continuity authority.
```

## Grounding rules

```text
FULL_REPO_GROUNDED = current repo/docs/issues/PRs/tests/logs were inspected for the claim.
LIMITED_CHAT_LOCAL = support is limited to chat-local context and must not imply full Lantern/Keystone convergence.
UNAVAILABLE_OR_DEGRADED = relevant sources or tools are unavailable, stale, or failing.
```

Durable anchor claims require `FULL_REPO_GROUNDED`. If grounding is degraded, use limited-support language and avoid continuity claims.

## Claim labels

Serious claims must use at least one of:

```text
FACT_SOURCE_BACKED
FACT_OPERATOR_REPORTED
INFERENCE
HEURISTIC_CONFIDENCE
SPECULATION
UNKNOWN
CORRECTED
RETRACTED
BLOCKED
```

## High-impact downgrade

Requests touching medical, legal, financial, minors, caregiver/relationship authority, crisis, surveillance, public writes, payments, or physical-world control must be blocked or downgraded to low-risk support such as:

```text
question preparation
source-checking
general educational explanation
options list with uncertainty
professional-support routing
emergency-resource routing when urgent
```

## Privacy and control defaults

```text
No raw transcript storage by default.
No hidden profiling, surveillance, scoring, or coercive personalization.
No live sensors enabled by default.
No public writes by default.
User can pause, stop, correct, retract, or revoke a pilot interaction.
Operator can pause or stop the pilot immediately.
```

## Correction path

Unsupported, wrong, challenged, or overconfident claims must be recorded through the correction ledger process:

```text
CORRECTED = replacement claim with evidence or clearer uncertainty.
RETRACTED = claim removed because support is insufficient.
UNKNOWN = current evidence is unavailable or inconclusive.
BLOCKED = request is outside pilot scope or high-impact authority.
```

## Launch evidence

```text
Master anchor commit: 920be0831fff211ec0f57dfc6bcb4806f0188e12
Prior PR validation: tests success; convergence-validation success
Pilot accelerator merged: docs/tests for launch boundaries and dashboard transparency
Launch-control PR required: this record, runbook, privacy/control notice, correction ledger, scorecard update, and launch docs tests
```

## Launch stop conditions

Pause or stop the pilot if any of the following occur:

```text
high-impact advice is presented as authority
mode/grounding disclosure is missing from a durable or high-impact claim
raw transcript storage or hidden profiling is requested as default behavior
user cannot pause, stop, correct, retract, or revoke
runtime autonomy, public writes, live sensors, payments, emergency authority, or physical control are implied
identity-continuity, repo consciousness, or perfect-memory claims appear
CI or convergence-validation fails on a launch-control change
```

## Expansion rule

This launch does not authorize widening. Expansion requires a new PR or issue record with:

```text
specific expanded surface
updated scorecard
current CI evidence
red-team evidence
privacy/control review
correction path
rollback plan
operator approval
```
