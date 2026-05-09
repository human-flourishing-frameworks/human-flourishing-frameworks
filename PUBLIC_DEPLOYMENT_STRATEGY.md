# Public Deployment Strategy

Status: docs/data-contract policy.

This document defines a platform-agnostic public deployment strategy for HFF.
Railway may be used as a current adapter, but HFF should not depend on Railway
as the architecture.

It is intentionally docs-only. It adds no runtime code, deploy hooks, secrets,
credentials, infrastructure automation, endpoints, polling, mesh writes, or
provider-specific configuration.

## Core rule

Railway is a hosting adapter, not the deployment strategy.

The strategy is:

```text
portable container
read-only public surface
closed write/autonomy flags
explicit deployed-SHA validation
post-deploy smoke checks
external monitoring
provider-exit path
```

## Target deployment shape

Preferred public posture:

```text
public web surface: read-only / advisory
public API surface: health, status, read-only model views
write surfaces: disabled unless narrowly approved
autonomy surfaces: disabled unless stage-authorized
operator/control plane: separate from public app
secrets: never exposed to public app logs or UI
```

## Provider roles

| Provider role | Acceptable use | Not acceptable |
|---|---|---|
| Simple PaaS adapter | Host the Docker image and expose health endpoints | Become the source of deployment truth |
| Container platform | Run the same image with explicit env flags | Mutate runtime behavior through hidden defaults |
| Static host/CDN | Serve public read-only artifacts | Host write/control endpoints |
| External monitor | Verify uptime and smoke checks after deploy | Replace release validation |
| CI/CD system | Build, test, publish signed images | Self-authorize production recovery |

## Current Railway posture

Current Railway-specific posture should stay minimal:

```text
railway.toml: Dockerfile builder only
startCommand override: absent unless fresh evidence requires it
healthcheck path: /health when configured in provider settings
PORT: provided by hosting platform and consumed by container command
```

Railway should be easy to replace with any platform that can run the OCI/Docker
image and provide environment variables.

## Why provider-agnostic matters

A public deployment that depends too much on one provider can create avoidable
risk:

```text
provider outage -> total outage
provider-specific config -> portability loss
provider healthcheck semantics -> false release confidence
provider logs/env handling -> accidental secret exposure
provider deploy UI -> unreviewed production mutation
```

The system should treat provider evidence as one signal, not the source of
truth.

## Public-risk-minimized modes

### Mode A: Static public mirror

Lowest public risk.

```text
build static/read-only public pages
publish no write endpoints
publish no secrets
publish no live autonomy
refresh by reviewed deploy only
```

Good for public education, status snapshots, and doctrine pages.

### Mode B: Read-only dynamic service

Acceptable default for HFF public app.

```text
serve /health
serve /api/status
serve read-only model/status endpoints
keep writes disabled
keep mesh sync disabled
keep executor disabled
keep live sensors disabled unless explicitly approved
```

Good for demos and public transparency.

### Mode C: Controlled API service

Higher risk.

```text
requires write tokens
requires scoped credentials
requires rate limits
audit logs required
no public-write demo override in production
```

Good only for controlled deployments.

### Mode D: Runtime/autonomy service

Highest risk.

```text
requires maturity-stage authorization
requires separate control plane
requires audit, rollback, external monitor, kill switch
not a default public deployment mode
```

## Release validation ladder

| Reliance level | Evidence | Public-deploy meaning |
|---:|---|---|
| 1 | A provider says deploy succeeded | Weak signal only |
| 2 | `/health` returns 200 once | App process responded once |
| 3 | `/health` + `/api/status` pass on deployed SHA | Basic smoke validation |
| 4 | Safety endpoints and runtime flags verified | Low-risk public mode acceptable |
| 5 | External monitor + rollback path + operator/governance confirmation | Release validated |

## Required public deploy gates

Before public release validation:

```text
deployed commit SHA recorded
container image/digest recorded when available
/health returns 200
/api/status returns 200
/api/autonomous/status confirms executor disabled by default
/api/mesh/sync returns 403 by default
runtime flags audited
public writes disabled
live sensors disabled unless approved
mesh sync disabled unless approved
secrets not printed or exposed
external monitor configured or manual follow-up scheduled
rollback path identified
```

## Provider exit criteria

A deployment strategy is acceptable only if HFF can move providers without
rewriting the app.

Minimum exit criteria:

```text
Dockerfile remains source of startup truth
app listens on PORT
no required Railway-only runtime code
no provider-specific secret assumptions
release checklist works for at least one non-Railway target
health/status endpoints are platform-neutral
```

## Better-than-Railway target architecture

Longer-term target:

```text
public static/read-only mirror
+ read-only dynamic API container
+ separate private control plane
+ external uptime/smoke monitor
+ signed image or deploy artifact
+ immutable release notes with deployed SHA
+ provider-neutral rollback procedure
```

Railway can host the read-only dynamic API container for now. It should not host
operatorless control authority until the deployment autonomy maturity model has
advanced beyond Stage 1.

## Explicit non-goals

This policy does not authorize:

```text
self-repairing deploys
secret rotation
production rollback automation
autonomous config changes
public write APIs
mesh writes
live sensor polling
autonomous escalation execution
provider-specific lock-in
```

## Default conclusion

The acceptable-risk public strategy is not "make Railway safer." It is:

```text
make HFF portable
make the public surface read-only
make provider evidence non-authoritative
make release validation explicit
make provider replacement easy
```
