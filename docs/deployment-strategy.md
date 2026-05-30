# Deployment Strategy

Canonical production start command:

`gunicorn safe_app:app --bind 0.0.0.0:$PORT --log-file -`

For local container parity, the Docker/TOML equivalent is:

`gunicorn safe_app:app --bind 0.0.0.0:${PORT:-5000} --log-file -`

## Health

Use `/healthz` as the deployment healthcheck route.

## Blocked Stale Commands

`python /app/dashboard_app.py` is not the canonical production target. Keep it
out of Railway, Render, and Docker production start commands.

## Release Check

Platform deployment references the expected Git commit before promoting any
release.

## Lantern AWS URL Bridge

Lantern Cloud OS AWS migration is tracked separately from this HFF deployment
surface. Do not treat HFF Render status as Lantern cloud truth.

Use [`docs/lantern-aws-url-bridge.md`](./lantern-aws-url-bridge.md) for the
current Lantern AWS links, local validation URLs, retired Render URLs, and the
held AWS public URL gate.
