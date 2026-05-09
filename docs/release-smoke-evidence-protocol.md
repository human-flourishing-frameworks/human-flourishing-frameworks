# Release Smoke Evidence Protocol

Status: docs/release checklist policy.

Last reviewed: 2026-05-09.

This document defines what counts as release smoke evidence for HFF. It is the
first successor lane split out from PR #20's broader runtime bundle.

It is intentionally docs-only. It adds no runtime code, endpoint, workflow
trigger, deployment behavior, secret handling, live polling, mesh write behavior,
or autonomous authority.

## Purpose

PR #20 correctly identified that tests and deployment readiness are not the same
thing as live service evidence. This document turns that distinction into a
small reviewable release protocol.

Core rule:

```text
A test pass is not a live release claim.
A healthcheck gate is not continuous monitoring.
A GitHub commit is not production truth.
```

## Evidence classes

| Evidence class | What it proves | What it does not prove |
|---|---|---|
| Local tests | Code behavior in the local/test environment | Public deployment health |
| GitHub Actions | CI behavior for a specific ref/SHA | Live Railway service state |
| Deployment logs | Build/startup/deploy lifecycle for a target service | Endpoint semantics unless endpoints are checked |
| `/health` | Service is reachable and health endpoint returns expected status | Full application correctness |
| `/api/status` | Application status endpoint is reachable and returns expected status JSON | Full runtime safety posture |
| `/api/autonomous/status` | Autonomous status endpoint is reachable and can expose default-off state | That no other executor path exists |
| `/api/mesh/sync` smoke | Default write-like mesh path remains closed unless explicitly enabled | That all network paths are safe |
| Operator confirmation | Human review of deployment/context | Technical proof by itself |

## Minimum release smoke packet

Before anyone says a release is live-validated, record:

```yaml
release_smoke_packet:
  repo: human-flourishing-frameworks/human-flourishing-frameworks
  branch: master
  commit_sha: <deployed commit sha>
  deployment_target: Railway
  checked_at_utc: <timestamp>
  checked_by: <operator/tool>
  evidence:
    health:
      method: GET
      url: https://web-production-46794.up.railway.app/health
      expected: HTTP 200
      observed: <status/body summary>
    api_status:
      method: GET
      url: https://web-production-46794.up.railway.app/api/status
      expected: HTTP 200 with expected status JSON
      observed: <status/body summary>
    autonomous_status:
      method: GET
      url: https://web-production-46794.up.railway.app/api/autonomous/status
      expected: auto_execute_escalations_enabled=false unless explicitly enabled
      observed: <status/body summary>
    mesh_sync_default_closed:
      method: POST
      url: https://web-production-46794.up.railway.app/api/mesh/sync
      expected: HTTP 403 unless ENABLE_MESH_SYNC=true
      observed: <status/body summary>
  conclusion: pending | passed | failed | partial
  limitations:
    - <known gap>
```

## Shell-specific command packets

Commands must name the shell and risk class. Do not present these as executed
unless output is captured.

PowerShell:

```powershell
# PowerShell, local machine, network smoke checks, read-only except POST smoke
$BaseUrl = 'https://web-production-46794.up.railway.app'
Invoke-WebRequest -Uri "$BaseUrl/health" -Method GET
Invoke-WebRequest -Uri "$BaseUrl/api/status" -Method GET
Invoke-WebRequest -Uri "$BaseUrl/api/autonomous/status" -Method GET
Invoke-WebRequest -Uri "$BaseUrl/api/mesh/sync" -Method POST -ContentType 'application/json' -Body '{"node_id":"smoke-test","violations":[]}'
```

Bash / Git Bash / WSL:

```bash
# Bash/Git Bash/WSL, network smoke checks, read-only except POST smoke
BASE_URL='https://web-production-46794.up.railway.app'
curl -i "$BASE_URL/health"
curl -i "$BASE_URL/api/status"
curl -i "$BASE_URL/api/autonomous/status"
curl -i -X POST "$BASE_URL/api/mesh/sync" \
  -H 'Content-Type: application/json' \
  -d '{"node_id":"smoke-test","violations":[]}'
```

Risk note:

```text
The mesh smoke POST is acceptable only because the expected default result is
403 unless ENABLE_MESH_SYNC=true. If it succeeds unexpectedly, treat that as a
release blocker until reviewed.
```

## Required failure handling

If a smoke check fails:

```text
do not claim release validation
capture status code and short body summary
avoid repeating secrets or full logs
determine whether failure is deployment, routing, app, config, or auth related
open or update a focused issue/PR only after operator review
```

If `/api/mesh/sync` returns success by default:

```text
mark release unsafe
verify ENABLE_MESH_SYNC state
inspect recent deployment/config changes
avoid sending further synthetic sync payloads until reviewed
```

If `/api/autonomous/status` shows executor enabled unexpectedly:

```text
mark release unsafe
verify ENABLE_AUTONOMOUS_ESCALATION_EXECUTOR state
inspect deployment config and logs
stop before any autonomous workflow test
```

## PR body wording

Allowed:

```text
Local tests passed for commit <sha>.
GitHub Actions passed for run <id> on ref <ref>.
Live smoke checks passed at <timestamp> for deployed commit <sha>.
```

Not allowed:

```text
Production is healthy.
Runtime is proven safe.
Autonomy is safe.
Mesh is secure.
```

Those are broader claims than the smoke evidence supports.

## Relationship to PR #20

This document is a low-risk successor slice from PR #20. It preserves PR #20's
release-validation concern while avoiding runtime code changes.

It should be reviewed independently before any runtime successor PRs are marked
ready.

## Non-goals

This document does not authorize:

```text
deployment
redeployment
environment variable changes
runtime code changes
mesh writes beyond the default-closed smoke check
live polling
autonomous executor enablement
secret reads
background monitoring
claiming health without fresh endpoint evidence
```
