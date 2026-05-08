# Corrections Record

This file documents claims made by this project that were inaccurate, and what was done to correct them. A project about accountability should hold itself to the same standard.

---

## 2026-05-08 — Fabricated data and false status claims

### What was wrong

The application served fabricated data presented as real.

**Hardcoded violations in `app.py` (lines 113–144, original):**
- Hospital XYZ — Diagnostic Bias — 2,400 affected — $12M harm
- Federal Sentencing — Sentencing Bias — 15,000 affected — $45M harm
- ICE Facial Recognition — Recognition Error — 8,500 affected — $28M harm

These were Python dicts, not records from any real source. No institution was audited. No affected persons were tracked.

**`/api/status` returned fabricated aggregate figures:**
```json
{
  "violations": 7,
  "affected_persons": 48250,
  "governance": "12-member board active",
  "mode": "production"
}
```
None of these numbers reflected real data. There was no 12-member board. The system was not in production.

**README made the following claims without basis:**
- "13 nodes deployed globally" — there were at most a few free-tier cloud instances run by one person
- "Real Data Currently Tracked" — the data was hardcoded
- "Cryptographic proof (court-admissible)" — HMAC-SHA256 over SQLite rows is not court-admissible; this was a legal claim, not a technical description
- "Byzantine consensus voting — automatic, no human approval needed" — consensus ran over a single node, guaranteeing 100% approval of every proposal
- "48,250+ affected persons | $1.163M+ quantified harm" — fabricated totals

**Byzantine consensus DB** contained pre-seeded "approved" proposals:
- `system-improvement-1` — Performance Optimization
- `system-improvement-2` — Add WebAssembly Support
- `system-improvement-3` — Implement Sharding

These were not AI bias violations. They were seeded to make the consensus system appear active.

**Adoption DB** contained 15–16 node registrations accumulated from local test runs, presented to the `/api/adoption/stats` endpoint as real global nodes.

### What was corrected

- Removed all hardcoded violation data from `app.py`
- Created `violations_db.py`: real SQLite-backed intake with HMAC-SHA256 signing at submission time
- `POST /api/violations` now validates, persists, and signs each submission
- `/api/status` now queries real DB counts — starts at 0 and reflects actual submissions
- `mode` changed from `"production"` to `"open"`
- `governance` claim removed from status response
- `/api/mesh/peers` was 404 — endpoint added, returns real peer list
- `/mesh/sync` endpoint added — mesh sync thread now has somewhere to POST
- Auto-updater (`auto_updater.py`, which ran `git pull origin master` hourly) disabled by default; requires `AUTO_UPDATE=true`
- Pre-seeded Byzantine consensus proposals deleted
- Test-run ghost nodes deleted from adoption DB
- Test-run peer entries deleted from resilience DB
- Dashboard stats load from API at runtime — no hardcoded numbers in HTML

### What remains to be done

- README still contains false claims (Phase 4, pending)
- Governance board is described in software but no board members exist — README should clarify this honestly
- "Court-admissible" language should be removed or replaced with an accurate technical description
- Single-node Byzantine consensus auto-approves every proposal — correct behavior technically, but requires multi-node deployment to be meaningful; this should be documented clearly

---

*This record will be updated as further corrections are made.*
