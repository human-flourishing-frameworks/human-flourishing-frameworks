# Pen Test Bounded Validation

Implements: #141

This document defines a safe validation pass that should attack assumptions and
exposed surfaces, not people. It is a bounded review plan for local repo
checks, local app routes, public read-only HFF surface if operator owns/controls
it, configuration posture, secret exposure checks, route classification,
sensor/telemetry boundary checks, release-gate behavior, and confidence/range
validation.

## Authorized Targets

- local repo checks
- local app routes
- public read-only HFF surface if operator owns/controls it
- configuration posture
- secret exposure checks
- route classification
- sensor/telemetry boundary checks
- release-gate behavior
- confidence/range validation

## Out Of Scope Hard Blocks

- credential theft
- exploitation of third-party systems
- bypassing authentication
- rate-limit abuse
- malware
- persistence
- privilege escalation on systems not owned by operator
- social engineering
- public disclosure of secrets/private data
- deanonymizing real participants
- biometric inference from device signals

## Validation Matrix

| Check | Purpose |
|---|---|
| secret string scan | verify no obvious secret material is exposed |
| /healthz | confirm the public status route stays read-only |
| dashboard wording | ensure operator copy states limits clearly |
| sensor wording | ensure live-sensor copy preserves consent and uncertainty |
| unauthenticated writes | confirm default-closed behavior |
| out-of-range confidence inputs | reject invalid ranges safely |
| boundary public copy | keep public language aligned with real limits |
| IMMUTABLE_RULES | preserve repo guardrails in the public surface |
| mesh sync default-closed | do not enable mesh writes by default |
| adoption write default-closed | block public write expansion by default |

## Evidence Rules

For every finding, record:

- command run
- local path
- branch
- commit
- result
- failure output
- whether any private data appeared

Do not paste secrets or account data into public issues.

## Findings Disposition

- false-positive
- confirmed weakness with safe fix
- confirmed weakness needing runtime change
- credential / secret exposure
- third-party system affected

## Non Goals

- offensive exploitation
- credential abuse
- public secret disclosure
- testing on systems the operator does not own
- social engineering of any person
- deanonymizing real participants
- weakening default-closed runtime gates
- broadening sensor scope
- bypassing release gates
