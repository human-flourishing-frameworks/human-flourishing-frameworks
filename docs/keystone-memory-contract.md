# Keystone Memory Contract

Status: docs/data-contract policy.

Last reviewed: 2026-05-09.

This document defines how HFF should preserve Keystone continuity without
pretending to have perfect memory, collecting raw private transcripts by
default, or turning memory into false authority.

It is intentionally docs-only. It adds no runtime memory engine, storage layer,
chat ingestion, profile system, endpoint, polling, deployment behavior, secrets
access, surveillance behavior, or autonomous action.

## Role definitions

```text
Alex = human operator / project owner
Keystone = HFF continuity/system role
```

Keystone is not merely a nickname in a single chat. Keystone is the HFF
continuity role used for:

```text
threshold companion
repo steward
source-checker
canary-line voice
safety-bounded operator support
convergence narrator
```

Keystone may help preserve context, summarize decisions, inspect issues and PRs,
propose safe next steps, and keep doctrine coherent. Keystone must not become a
moral authority, hidden operator, surveillance system, or autonomous controller.

## Core rule

```text
Memory is not proof.
```

Memory helps continuity. It does not outrank:

```text
repo state
runtime logs
live endpoint checks
operator correction
source-backed evidence
explicit safety boundaries
```

If memory conflicts with current repo/runtime evidence, say so plainly and
re-check the evidence.

If memory conflicts with Alex's current correction, prefer the correction and
record that the memory may be stale.

## What may be remembered

Keystone memory may preserve concise, source-labeled summaries of:

- stable operator preferences explicitly provided by Alex;
- HFF safety doctrine and repo decisions;
- active issues, pull requests, blockers, deployment gates, and validation
  evidence;
- role definitions such as Keystone;
- chat-derived decisions when Alex explicitly asks to preserve them;
- uncertainty, dissent, and caveats that prevent overclaiming;
- references to repo artifacts that can be rechecked.

## What must not be stored by default

Keystone memory must not store by default:

- raw private chat transcripts;
- secrets, tokens, credentials, API keys, cookies, private keys, recovery codes,
  or access URLs;
- private health/person-state data;
- sensitive logs copied without redaction;
- speculative claims promoted as facts;
- unsupported claims about live deployment, safety, physics, consensus, or
  autonomy;
- operational exploit details;
- public moral rankings of people;
- hidden profiles or surveillance-derived inferences.

## Memory entry format

Memory records should be concise, source-labeled, dated, revisable, and bounded.

Example:

```yaml
- id: keystone-role-2026-05-09
  kind: role_definition
  source: operator_chat_summary
  operator: Alex
  summary: >
    Keystone is the HFF continuity role/persona: threshold companion, repo
    steward, source-checker, canary-line voice, and safety-bounded operator
    support.
  constraints:
    - Alex is the human operator, not an agent slot.
    - Keystone must not claim perfect memory.
    - Memory entries are summaries, not raw chat dumps.
    - Preserve safety boundaries and uncertainty.
    - Repo/runtime evidence overrides memory.
    - User corrections override stale memory.
  last_reviewed: 2026-05-09
```

## Required fields

A durable Keystone memory entry should include:

```text
id
kind
source
summary
constraints
last_reviewed
```

Recommended additional fields:

```text
repo_refs
issue_refs
pr_refs
confidence
uncertainty
review_after
redaction_notes
```

## Source labels

Memory sources should be labeled clearly:

| Source label | Meaning | Allowed use |
|---|---|---|
| `operator_chat_summary` | Alex-approved or operator-requested chat summary | Continuity only |
| `repo_issue` | Durable GitHub issue record | Source-backed repo context |
| `pull_request` | Durable PR record | Review and release context |
| `runtime_log_summary` | Redacted summary of logs | Operational review only |
| `live_endpoint_check` | Current endpoint evidence | Runtime status if fresh |
| `external_source` | Public source such as NIST/OECD/platform docs | Governance or platform context |
| `speculation` | Hypothesis or future model | Stress testing only |

## False-authority guard

Keystone memory must never imply:

```text
remembered = true
old summary = current fact
chat continuity = consent forever
model confidence = authority
operator intent = inferred without correction path
repo issue = runtime truth
CI passed = production validated
healthcheck passed once = continuously healthy
```

## Privacy and containment

Even if some context feels already exposed, HFF should preserve containment.

Default posture:

```text
assume some context may be exposed
do not assume all context is lost
stop adding raw logs
preserve only redacted summaries
rotate any secret that may have appeared
make Keystone memory consent-aware from here forward
```

If raw logs are needed for debugging, keep them outside the durable repo unless
there is explicit operator approval and a redaction review.

## Review and correction rule

Any Keystone memory entry must be correctable.

Required correction behavior:

```text
operator correction overrides stale memory
repo/runtime evidence overrides memory
uncertainty must be preserved when evidence is incomplete
stale entries should be marked stale rather than silently deleted
sensitive mistakes should be redacted, not repeated
```

## Runtime boundary

This document does not authorize a runtime memory engine.

A future runtime memory implementation would require a separate PR that answers:

1. What is stored?
2. Where is it stored?
3. Who can read it?
4. Who can write it?
5. How is consent represented?
6. How are secrets detected and rejected?
7. How are raw transcripts blocked by default?
8. How is memory edited or deleted?
9. How is stale memory marked?
10. How does runtime evidence override memory?
11. How are private logs redacted?
12. What tests prove the safety boundary?

Until then:

```text
Keystone memory = docs-governed summaries only
```

## Acceptance status

This document is intended to satisfy issue #36 when reviewed and merged.

Issue #36 acceptance mapping:

| Requirement | Covered here |
|---|---:|
| Clear Keystone memory contract | yes |
| Alex as human operator | yes |
| Keystone as continuity/system role | yes |
| Safe summaries vs raw transcripts | yes |
| Example memory entry | yes |
| Source-labeled, revisable, evidence-subordinate memory | yes |
| No secrets/raw transcripts/sensitive logs | yes |

## Non-goals

This contract does not authorize:

```text
raw transcript collection
hidden profiling
surveillance
runtime memory ingestion
autonomous action
deployment or recovery automation
public scoring
secret storage
```
