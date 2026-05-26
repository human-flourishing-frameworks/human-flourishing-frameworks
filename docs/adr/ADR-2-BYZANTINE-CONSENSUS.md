# ADR-2: Byzantine Fault Tolerant Consensus for Research Queue Acceptance

**Status:** Accepted  
**Date:** 2026-05-25  
**Deciders:** Founder, Research Team Lead

## Context
Research material sourced from multiple channels: web scraping, human submission, Claude API validation. Single source could fail or inject bad data. Need consensus that tolerates 1 Byzantine fault.

## Decision
Implement 2-of-3 BFT voting for research queue acceptance.
- **Voter 1:** Web auto-fetch (source validity)
- **Voter 2:** Human team review (quality check)
- **Voter 3:** Claude API validation (relevance + safety)

If any 2 agree on item + priority, item enters queue. Consensus decision logged to JSONL with full voting record.

## Options Considered

### Option A: Byzantine Consensus 2-of-3 ✅ Chosen
- **Complexity:** Low
- **Cost:** 3× API calls per item
- **Scalability:** Fine for <100 items/day
- **Familiarity:** Medium

**Pros:**
- Tolerates 1 Byzantine fault
- Formal agreement proof (logged)
- Prevents single bad source pollution
- Immutable consensus record

**Cons:**
- Higher latency (3 validators)
- 3× processing cost

### Option B: Simple Majority (2 of 2)
**Rejected:** No Byzantine tolerance.

### Option C: Single Validator (Claude only)
**Rejected:** Single point of failure.

## Trade-off Analysis
BFT adds latency (wait for 3 validators) but guarantees correctness. For research queue (async, latency-tolerant), acceptable. Formal record satisfies governance requirement.

## Consequences
- **Easier:** Prove governance, catch bad data early, dispute resolution (log shows votes)
- **Harder:** Slower queue (3 validators), requires coordinating sources
- **Revisit:** If any validator offline >5min, switch to 2-of-2 emergency mode

## Implementation

### Voting Protocol
```json
{
  "item_id": 42,
  "title": "Solar Panel Maintenance for RVs",
  "votes": [
    {"voter": "web_fetch", "result": "valid", "priority": 2, "timestamp": "..."},
    {"voter": "human_team", "result": "valid", "priority": 2, "timestamp": "..."},
    {"voter": "claude_api", "result": "valid", "priority": 2, "timestamp": "..."}
  ],
  "consensus": {"passed": true, "quorum": 2, "priority": 2},
  "action": "item_queued"
}
```

### Validation Rules
- **Valid Quorum:** ≥2 matching {result, priority}
- **Byzantine:** 1 voter disagrees, majority wins
- **Timeout:** If any validator unreachable >5min, proceed with 2 votes

## Action Items
- [x] Voting logic implemented in research-queue-claude-auto.py
- [x] Consensus decision logged to JSONL
- [ ] Consensus audit report (voting pattern analysis)
- [ ] Byzantine fault detection (auto-fallback to 2-of-2)

---
**Evidence:** LANTERN-DAY-ONE-DEMO.py shows 3 voting scenarios with consensus log
