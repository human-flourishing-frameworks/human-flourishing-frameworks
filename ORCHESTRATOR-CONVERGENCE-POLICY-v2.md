# Orchestrator Convergence Policy v2

## Purpose
This policy defines mandatory convergence gates for cross-repository work across:
- `C:\Users\alexp\Documents\gm-agent-orchestrator`
- `C:\tmp\human-flourishing-frameworks-scan`

## Core Rules
1. Local-first MCP verification is required before trusting any remote endpoint.
2. No implicit trust of tunnel or internet-exposed tools.
3. No production-ready claim without passing evidence gates.
4. No destructive git operations (`reset --hard`, `clean -fd`, force-push) in convergence flow.

## Deterministic Convergence Checklist
1. Baseline truth captured (branch, remotes, dirty state, top commits) for both repos.
2. Claimed-vs-verified artifact matrix generated.
3. CI guardrail suite passes in target repo.
4. Evidence bundle includes UTC timestamp, command outputs, and commit SHAs.
5. Merge order validated:
   - Core runtime
   - Orchestration/policy
   - QA/tests
   - Docs/reporting
6. Rollback points documented:
   - Last passing SHA per stream
   - Revert strategy (`git revert` only, no history rewrite)

## Production-Ready Gate
A release may be labeled production-ready only when all checklist items pass and the evidence report has no unresolved unknown claims.
