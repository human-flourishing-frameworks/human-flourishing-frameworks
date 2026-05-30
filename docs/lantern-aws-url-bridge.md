# Lantern AWS URL Bridge

Status: link bridge only; AWS public URL is not verified yet.

This HFF repo should not use Render status as Lantern Cloud OS truth. Lantern
runtime and AWS migration work lives in the Lantern OS repo, while this file
keeps the HFF side linked to the current contract and validation URLs.

## Source Links

| Surface | Link |
|---|---|
| Lantern repo | https://github.com/alex-place/lantern-os |
| Runtime CI/CD contract | https://github.com/alex-place/lantern-os/blob/master/docs/LANTERN-RUNTIME-CICD.md |
| Baseline model v1 | https://github.com/alex-place/lantern-os/blob/master/manifests/LANTERN-BASELINE-MODEL-v1.md |
| Cloud mirrors manifest | https://github.com/alex-place/lantern-os/blob/master/manifests/cloud-mirrors.json |
| AWS Dockerfile | https://github.com/alex-place/lantern-os/blob/master/apps/lantern-garage/Dockerfile |
| AWS cloud server | https://github.com/alex-place/lantern-os/blob/master/apps/lantern-garage/cloud-server.js |

## URL Truth

| Kind | URL | Status |
|---|---|---|
| Local primary dashboard | `http://127.0.0.1:4177/` | Verified locally when the operator app is running. |
| Local health | `http://127.0.0.1:4177/api/health` | Must return HTTP 200 before local claims. |
| Local cloud mirror state | `http://127.0.0.1:4177/api/cloud-mirrors` | Must show AWS mirror truth before promotion. |
| Local MCP catalog | `http://127.0.0.1:4177/api/mcp-catalog` | Local-only runtime evidence. |
| AWS service root | pending operator deploy | Not verified; do not publish as fixed yet. |
| AWS service health | pending operator deploy plus `/api/health` | Required before public cloud claim. |
| AWS mirror API | pending operator deploy plus `/api/cloud-mirrors` | Required before public cloud claim. |

## Current Fix Contract

- `npm start` stays local and runs `server.js`.
- `npm run start:cloud` is the cloud-safe runtime and runs `cloud-server.js`.
- AWS target is ECS Fargate or a compatible AWS container service exposing port
  `8080`.
- Cloud mode must stay read-only for local controls, worktrees, queues, secrets,
  Windows actions, and MCP dispatch.
- Render URLs are retired from Lantern cloud truth until an operator explicitly
  re-promotes them with fresh evidence.

## Retired Lantern Mirror URLs

These URLs may exist, but they must not be treated as Lantern Cloud OS proof:

- `https://lantern-os.onrender.com`
- `https://human-flourishing-frameworks.onrender.com` as a Lantern mirror

HFF may still have its own public deployment lifecycle. That lifecycle is
separate from Lantern Cloud OS AWS promotion.

