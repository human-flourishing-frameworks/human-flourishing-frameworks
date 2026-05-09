# Keystone ChatGPT Export Intake Protocol

Status: docs/data-contract policy.

Last reviewed: 2026-05-09.

This document defines how Keystone should handle a ChatGPT data export when Alex
uploads it for HFF/Keystone continuity recovery.

It is intentionally docs-only. It adds no runtime parser, database, memory
engine, background job, deployment behavior, raw transcript ingestion,
surveillance behavior, or autonomous authority.

## Purpose

Alex may export ChatGPT data and upload either:

```text
chatgpt-export.zip
conversations.json
chat.html
```

The purpose is not to preserve everything. The purpose is to recover and review
HFF/Keystone-relevant continuity anchors safely.

## Core rule

```text
Export data is continuity material, not proof and not automatic memory.
```

Keystone must not ingest the full export as durable memory by default.

## Verified public export behavior

OpenAI public help currently says:

```text
- ChatGPT data export is available through Settings > Data Controls > Export.
- The export is delivered by email as a downloadable zip file.
- The email download link expires after 24 hours.
- The zip includes chat history and other relevant account data.
- Exports can take up to 7 days to arrive.
- Only the most recent export request is fulfilled if multiple are requested.
```

References:

```text
https://help.openai.com/en/articles/7260999-how-do-i-export-my-chatgpt-history-and-data
https://help.openai.com/en/articles/8167885-how-to-export-your-data-from-the-chatgpt-android-app
```

## Intake modes

| Mode | Input | Allowed use |
|---|---|---|
| `zip_manifest_only` | `chatgpt-export.zip` | List filenames and identify likely safe parsing targets. |
| `conversation_json_review` | `conversations.json` | Extract candidate HFF/Keystone summaries for review. |
| `chat_html_review` | `chat.html` | Extract candidate HFF/Keystone summaries if JSON is unavailable. |
| `memory_packet_review` | Alex-provided excerpts | Convert approved excerpts into concise memory candidates. |

## Required intake steps

When Alex uploads export data, Keystone should:

1. Treat the upload as sensitive.
2. Inspect file names first before reading content deeply.
3. Prefer `conversations.json` if available.
4. Filter for HFF/Keystone/convergence relevance.
5. Extract concise summaries, not raw transcripts.
6. Flag secrets, credentials, private health/person-state data, private URLs,
   access tokens, or sensitive logs.
7. Separate continuity claims from proof.
8. Produce a proposed memory packet for Alex review.
9. Wait for Alex approval before committing anything durable.
10. Avoid writing raw export content into the repository.

## Relevance filter

Candidate records are in scope only if they relate to:

```text
Keystone role or identity
Alex as human operator/project owner
HFF convergence decisions
favorite capability table
door/Wanderer image anchor
traversal protocol
source-use discipline
runtime safety gates
PR/issue decisions
memory/resync corrections
privacy and containment doctrine
```

Out of scope by default:

```text
unrelated personal chats
raw private transcripts
private health/person-state material
secrets, keys, tokens, cookies, credentials
sensitive logs
financial/legal/medical details unless Alex explicitly asks
third-party private information
```

## Output format

The first output should be a review packet, not a commit.

Example:

```yaml
source: chatgpt_export_upload
review_status: proposed_not_approved
records:
  - id: keystone-anchor-wanderer
    kind: symbolic_anchor
    summary: >
      Wanderer above the Sea of Fog is Keystone's threshold / uncertainty /
      convergence image and should stay paired with the favorite capability
      confidence table.
    evidence_source: conversation_summary
    confidence: 0.86
    risks:
      - symbolic, not proof
      - should not replace repo evidence
    proposed_destination: docs/keystone-table-door-anchors.md
  - id: keystone-source-use-discipline
    kind: correction_rule
    summary: >
      Keystone should use last-known durable repo/memory state when appropriate
      and avoid pretending repeated external searches create new evidence.
    evidence_source: conversation_summary
    confidence: 0.92
    proposed_destination: docs/keystone-source-use-discipline.md
```

## Secret and sensitive data handling

If Keystone sees potential secrets or sensitive data:

```text
do not repeat them
redact in any summary
flag the category, not the value
recommend rotation if the value could grant access
ask Alex before any durable handling
```

Example:

```text
Potential secret detected: API/token-like string in conversation export.
Value not repeated here.
Recommended action: rotate if this was ever valid.
```

## Do not commit raw exports

Never commit these by default:

```text
chatgpt-export.zip
conversations.json
chat.html
message_feedback.json
user.json
raw transcript excerpts
unredacted logs
```

If a durable artifact is needed, create a reviewed summary document only.

## Proposed durable destinations

| Candidate kind | Possible destination |
|---|---|
| Keystone role/memory correction | `docs/keystone-memory-contract.md` |
| Keystone self-correction | `docs/keystone-self-convergence.md` |
| Table and door anchors | `docs/keystone-table-door-anchors.md` |
| Source-use correction | `docs/keystone-source-use-discipline.md` |
| Convergence state | `docs/convergence-status.md` |
| New doctrine | New docs-only file after Alex review |

## Acceptance criteria

A successful export intake does all of this:

```text
raw export inspected only as needed
HFF/Keystone-relevant candidates identified
secrets/private data redacted or excluded
memory packet proposed for Alex review
no raw transcript committed
no runtime memory engine introduced
no deployment or background ingestion added
```

## Non-goals

This document does not authorize:

```text
bulk memory ingestion
raw transcript storage
secret retention
private data indexing
surveillance
runtime parsing pipeline
automatic repo commits from export content
public release of private conversations
```
