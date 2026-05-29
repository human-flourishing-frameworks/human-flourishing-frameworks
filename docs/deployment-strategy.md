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
