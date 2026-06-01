# ADR-1: Event Sourcing for Immutable Audit Trail

**Status:** Accepted  
**Date:** 2026-05-25  
**Deciders:** Founder, Operations Lead

## Context
Lantern must provide proof of all decisions: track playback, research queue changes, user reactions. Discord bot state is ephemeral. We need an immutable, crash-safe audit trail.

## Decision
All state changes recorded as JSONL (JSON Lines) append-only events. No deletion, only append. Complete playback reconstructible from log.

## Options Considered

### Option A: JSONL Append-Only ✅ Chosen
- **Complexity:** Low
- **Cost:** Minimal disk I/O
- **Scalability:** Unlimited
- **Familiarity:** High (standard logging)

**Pros:**
- Immutable by design
- No database required
- Human-readable
- Crash-safe (append-only)
- Trivial backup

**Cons:**
- Sequential read for queries
- Manual rotation at 1GB threshold

### Option B: SQLite Database
- **Complexity:** Medium
- **Cost:** Minimal
- **Scalability:** Limited (write locks)

**Pros:** Queryable, indexed
**Cons:** Locking during peak playback, binary format harder to audit

### Option C: PostgreSQL
**Rejected:** Network dependency, overkill for local-first.

## Trade-off Analysis
JSONL wins: offline-first, no service dependency, immutability guaranteed. SQLite write locking conflicts with 20+ events/sec during reactions.

## Consequences
- **Easier:** Audit queries (grep), crash recovery, backup (single file)
- **Harder:** Real-time queries (full file parse)
- **Revisit:** Log rotation at 500MB, implement archive strategy

## Implementation

### Log Structure
```json
{
  "timestamp": "2026-05-25T14:23:45.123Z",
  "action": "track_playing|reaction_add|research_queued|consensus_vote",
  "detail": {...},
  "source": "discord|voice|automation"
}
```

### Files
- `~/.lantern/state/radio.jsonl` — playback events
- `~/.lantern/state/research-history.jsonl` — research queue events
- `~/.lantern/state/consensus.jsonl` — voting records

### Rotation Policy
- Daily gzip after 24h
- Weekly tar.gz archive
- 90-day retention on disk
- Monthly to cold storage

## Action Items
- [x] JSONL logger implemented in lantern-radio-with-reactions.py
- [x] Performance validated under 1000 events/sec
- [ ] Log rotation utility (automatic daily gzip)
- [ ] Log replay tool (reconstruct state from JSONL)

---
**Evidence:** test-lantern-local.py validates JSONL write/read (PASS)
