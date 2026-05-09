# Production Release Readiness Plan

Status: release-gating strategy artifact.

## Purpose

This plan optimizes HFF for a safer public production release using the seven-step
method. It converts current doubts into release blockers, acceptance criteria, and
small implementation slices.

## Release claim

HFF may be released publicly only as experimental advisory research software with
visible uncertainty, source limitations, and public-surface boundaries.

It must not be released as:

- production governance infrastructure;
- emergency response authority;
- legal, medical, financial, or geopolitical authority;
- surveillance infrastructure;
- an autonomous control system;
- a verified live sensor network;
- or a scientifically complete flourishing oracle.

## Seven-step production method

| Step | Release application | Pass condition |
|---:|---|---|
| 1. Say the claim | State exactly what public release means and does not mean. | README/dashboard/release notes use experimental advisory framing. |
| 2. Set the guard | Block unsafe expansions: public writes, hidden sensors, mesh sync, SDK/APK release, actuator control, authority claims. | Public-surface policy and CI assertions remain green. |
| 3. Add tiny checks | Add route tests, dashboard transparency tests, source/freshness assertions, and release smoke checklist. | CI covers public-readiness and dashboard health guardrails. |
| 4. Try safely | Use local Flask tests, CI, restore drill, and read-only public smoke checks. | No secret, credential, private-log, or write/action test is required. |
| 5. Look at reality | Compare deployed public UI/API responses against docs and dashboard copy. | Captured smoke evidence matches public claims. |
| 6. Fix mismatches | Correct labels, docs, tests, or routes when public output overclaims. | Mismatches are fixed by the smallest reviewed patch. |
| 7. Repeat later | Re-smoke after deploys and whenever public copy/model routes change. | Release checklist remains reusable and current. |

## Current release blockers

| Blocker | Severity | Why it blocks release confidence | Required fix |
|---|---:|---|---|
| Dashboard sensor wording says `live sensors` while observations may not be flowing. | High | Public may confuse registered sensors with active live evidence. | Distinguish registered, enabled, and observed sensors. |
| Dashboard source traceability is too thin for some entries. | High | `github.com` or short labels are not enough for public audit. | Add source-class/detail links or soften traceability copy. |
| Dashboard freshness wording is ambiguous. | High | `updated 5/9/2026` can look like source freshness instead of model-record freshness. | Rename to `model record updated`. |
| `active` advisory agents can imply operational authority. | High | Public may infer autonomous governance/control. | Rename to `loaded advisory workflow` or `demo status`. |
| `/healthz` not yet verified/implemented. | Medium-high | Deployment readiness checks need a lightweight endpoint. | Add route and tests. |
| Degraded-state UI is incomplete. | Medium-high | API failures may look blank/stale. | Add visible fallback. |
| Universe scope is hard to interpret. | Medium | `50% ±71%` needs experimental-context warning. | Label as experimental or collapse by default. |
| Accessibility implementation is not verified. | Medium | Public usability is policy-level only. | Add basic accessibility checks. |
| Live deployment smoke evidence missing. | High | Repo state is not production proof. | Capture public read-only smoke results after deploy. |
| License remains unresolved. | Medium | Public reuse rights are unclear. | Choose license or keep explicit no-license posture. |

## Minimum production release gate

A public production release candidate passes only if:

| Gate | Required evidence |
|---|---|
| CI | All tests and convergence-validation pass on `master`. |
| Restore drill | Release bundle and restore drill pass. |
| Public routes | `/`, `/health`, `/healthz`, and `/api/status` pass local route tests. |
| Dashboard truthfulness | Sensor, source, freshness, agent, and experimental-scope labels are unambiguous. |
| Public surface policy | Public read/write/private/disabled/not-allowed classifications are current. |
| No unsafe runtime flags | `ENABLE_LIVE_SENSORS`, `ENABLE_MESH_SYNC`, and `HFF_ALLOW_PUBLIC_WRITES` are off unless explicitly reviewed. |
| Smoke evidence | Public deployed routes are checked read-only after deploy. |
| Secrets | No secrets/tokens in repo, logs, dashboard, screenshots, or release docs. |
| Authority boundary | Dashboard and README do not claim governance, legal, medical, financial, geopolitical, or emergency authority. |
| Correction path | Public docs explain uncertainty and correction/review paths. |

## Near-term implementation slices

| Slice | Change | Validation |
|---:|---|---|
| 1 | Add `/healthz` route and route tests. | `test_dashboard_health.py` passes. |
| 2 | Add dashboard transparency wording tests. | Tests fail on `live sensors`, bare `updated`, or `active` authority drift. |
| 3 | Patch dashboard labels. | Tests pass and UI is easier to interpret. |
| 4 | Add CI step for dashboard health/transparency tests. | convergence-validation includes dashboard tests. |
| 5 | Add release smoke checklist artifact. | Checklist names public routes and expected safe responses. |
| 6 | Capture live smoke evidence after deploy. | Release notes include timestamps/status without secrets. |
| 7 | Re-score release readiness. | Confidence table updated from evidence. |

## Production confidence table

| Area | Current confidence | Target before release |
|---|---:|---:|
| Docs/policy guardrails | 94 | 95 |
| CI enforcement | 93 | 95 |
| Dashboard transparency | 61 | 90 |
| Dashboard route health | 58 | 90 |
| Live deployment truthfulness | 45 | 85 |
| Source traceability | 65 | 90 |
| Accessibility posture | 70 | 85 |
| Unsafe capability blocking | 92 | 97 |
| Release readiness overall | 68 | 88 |

## Not in scope for production v0

- public write enablement;
- live sensor enablement without review;
- mesh sync enablement without review;
- SDK or APK release;
- vehicle/device control;
- autonomous governance/enforcement;
- private data intake;
- national-security or geopolitical operational claims;
- claims of complete scientific validity.

## Boundary

Production release should mean: stable public experimental advisory surface with
honest labels, health checks, source limitations, CI guardrails, and smoke
evidence. It should not mean stronger authority, hidden capabilities, or proof
that the model is objectively complete.