# Release Checklist

This checklist tracks the release-preparation gates for the read-only
bio-threat registry and runtime safety hardening work.

## Release Blockers

1. Public Railway health must be restored.
   - `GET /health` must return 200.
   - `GET /api/status` must return 200.
   - Current validation found Railway 502 responses before this PR was
     deployed.

2. Validate the exact deployed commit.
   - Record the deployed commit SHA.
   - Confirm it includes the corrected Railway start command.
   - Confirm it includes default-off runtime safety gates.

3. Keep the PR draft until live validation passes.
   - CI passing is necessary but not sufficient for release.
   - Public service health must be verified after deploy.

## Required Checks

Run before marking the PR ready:

```bash
python -m unittest discover -s tests
```

Confirm GitHub Actions `unittest` is green on the PR head.

## Runtime Safety Gates

Confirm defaults before release:

- `ENABLE_LIVE_SENSORS` is unset/false unless live polling is explicitly approved.
- `ENABLE_MESH_SYNC` is unset/false unless peer mesh writes are explicitly approved.
- `ENABLE_AUTONOMOUS_ESCALATION_EXECUTOR` is unset/false unless autonomous execution is explicitly approved.
- `HFF_ALLOW_PUBLIC_WRITES` is unset/false on public services.

## Endpoint Smoke Checks

After deploy, verify:

```bash
curl -i https://web-production-46794.up.railway.app/health
curl -i https://web-production-46794.up.railway.app/api/status
curl -i https://web-production-46794.up.railway.app/api/autonomous/status
curl -i -X POST https://web-production-46794.up.railway.app/api/mesh/sync \
  -H "Content-Type: application/json" \
  -d "{\"node_id\":\"smoke-test\",\"violations\":[]}"
```

Expected `/api/mesh/sync` default result is 403 unless `ENABLE_MESH_SYNC=true`
was explicitly approved.

## Open Decisions

- Decide whether PR #20 should remain bundled or be split into smaller PRs.
- Select a public reuse license only when the operator is ready to grant one.
