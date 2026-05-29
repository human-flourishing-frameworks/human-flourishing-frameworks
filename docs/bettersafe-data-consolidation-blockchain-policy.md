# BetterSafe Data Consolidation And Blockchain Policy

## Default State

- Raw private data consolidation: BLOCKED
- Public blockchain storage of personal data: BLOCKED
- Public blockchain storage of raw transcripts: BLOCKED
- Public blockchain storage of direct identifiers: BLOCKED
- Default statistical collection from people: BLOCKED
- Opt-in aggregate statistics: NOT_ENABLED_UNTIL_REVIEWED

## Hash Handling

Hashes are not automatically safe. A hash of private data is still treated as
sensitive unless a privacy/security review proves otherwise. Do not put hashes
of private user data on a public blockchain during pilot.

## Future Aggregate Statistics Boundary

Any future statistical path requires explicit opt-in, purpose limitation, data
minimization, aggregate-only output, and a minimum group threshold before
reporting. The starting rule is `minimum_n = 25`. If that threshold is not met,
return `INSUFFICIENT_GROUP_SIZE`. Do not report the value, subgroup detail, or
residual calculation.

## Allowed Operational Evidence

Allowed evidence is limited to non-private operational receipts such as:

- PR number
- commit SHA
- CI status
- smoke-check result
- operator-approved readiness action receipt
- correction ledger entry
- non-private release artifact checksum

This evidence must avoid private user content.

## Review Requirements Before Any Consolidation Change

Before any reviewed expansion, require a documented:

- data inventory
- purpose statement
- collection fields
- retention rule
- consent/opt-in rule
- aggregation threshold
- de-identification risk review
- revocation/deletion handling
- security review
- privacy notice update
- tests proving blocked defaults

## Plain Answers

Are we collecting people's private data statistically?

No. The pilot baseline blocks default people-level statistical collection. Only
after a separate reviewed PR, explicit opt-in, minimum group threshold, and
non-identifying aggregate-only design.

Will private data go on public blockchain?

No. Public chain use is blocked for private, identifying, transcript,
household, health, safety, contact, device, or linkable user data.
