# HFF Convergence Status

Status: docs/data-contract policy.

Last reviewed: 2026-05-09.

This document is the current convergence anchor for Human Flourishing Frameworks.
It explains what is currently agreed, what remains blocked, and which action is
safest next.

It is intentionally docs-only. It adds no runtime code, endpoints, polling,
autonomous behavior, deployment hooks, secrets access, credentials, or mesh
writes.

## Current convergence line

```text
hold runtime
anchor doctrine in docs
then re-evaluate runtime PRs
```

The active operating decision is:

```text
ConvergenceHoldAndDocsAnchorFirst
```

This means HFF should not increase runtime authority, merge broad runtime safety
branches, or add memory/autonomy machinery until the current Keystone memory and
capability-confidence contracts are durable in the repository.

## Why this is the safest next action

The repo has converged on a doctrine, but that doctrine is still distributed
across issues, pull request bodies, docs, and chat-derived summaries.

That creates a continuity risk:

```text
future agent reads only code -> misses doctrine
future agent reads only PR -> misses memory boundary
future agent reads only chat -> treats memory as proof
future agent reads only deployment state -> overclaims runtime health
```

The next safe move is to create one repo-readable anchor that future agents,
operators, and reviewers can inspect before changing runtime behavior.

## Current doctrine spine

```text
Truth requires provenance.
Capability is not authority.
Memory is not proof.
Sensors are best-effort unless verified.
Live deployment health requires live endpoint or deployment-log evidence.
Autonomy is closed unless explicitly enabled and stage-authorized.
Alex is the human operator/project owner.
Keystone is the HFF continuity role.
```

## Current issue alignment

| Issue | Status | Convergence meaning |
|---|---:|---|
| #36 Keystone memory contract | Open | Must become durable docs before Keystone memory is treated as repo state. |
| #37 Capability confidence model | Open | Must become durable docs before using actor/system confidence records. |
| #18 Dual-use engine risk | Open | Ongoing governance/security boundary; do not collapse into this PR. |
| #22 Live polling observability | Closed/completed | Live polling/status observability comes before consensus hardening. |
| #13 Live sensor diagnosis | Historical | Registered sensors are not proof of fresh or verified measurements. |
| #12 Deployment split-brain | Historical | Deployment truth must be checked against the selected live surface. |

## Current PR alignment

| Pull request | Status | Convergence meaning |
|---|---:|---|
| #20 Runtime safety gates | Open draft | Keep held. Re-evaluate after convergence docs land. |
| Recent docs/safety PRs | Merged | The doctrine is moving toward default-closed advisory behavior. |

## External alignment

The current convergence posture is consistent with public governance and platform
sources:

- NIST AI RMF frames AI work as risk management for individuals,
  organizations, and society, and as a way to incorporate trustworthiness into
  design, development, use, and evaluation.
- NIST describes the AI RMF core around govern, map, measure, and manage.
- OECD AI Principles promote human-centric, trustworthy AI that respects human
  rights and democratic values.
- Railway healthchecks gate deployment activation but are not continuous live
  monitoring after deployment.
- GitHub Actions job reruns use the original event SHA/ref; a rerun is not the
  same as a fresh workflow dispatch on a new target.

References:

```text
https://www.nist.gov/itl/ai-risk-management-framework
https://www.nist.gov/news-events/news/2023/01/nist-risk-management-framework-aims-improve-trustworthiness-artificial
https://www.oecd.org/en/topics/ai-principles.html
https://docs.railway.com/reference/healthchecks
https://docs.github.com/en/actions/how-tos/manage-workflow-runs/re-run-workflows-and-jobs
```

## Current validation evidence

Latest available GitHub Actions rerun evidence from 2026-05-09:

```text
workflow: tests
run id: 25597347535
rerun job id: 75152786980
context: PR #35 merge-test ref, not a new master workflow dispatch
compile key modules and tests: passed
focused unittest discovery: passed
result: Ran 92 tests in 0.127s — OK
```

Important limitation:

```text
The workflow has pull_request and push-to-master triggers only.
It does not currently expose workflow_dispatch.
The rerun validated the original PR/run context, not a fresh manual master run.
```

## Current blockers

Do not mark runtime work ready until these are satisfied:

```text
Keystone memory contract committed
capability confidence model committed
convergence status committed
human review complete
live public health checked against selected deployment
runtime flags audited
write/autonomy/mesh surfaces verified default-closed
```

## Next best action

The current highest-confidence action is this docs-only convergence PR:

```text
docs/convergence-status.md
docs/keystone-memory-contract.md
docs/capability-confidence-model.md
```

Expected issue effect:

```text
satisfies #36
satisfies #37
references #18 as ongoing boundary
references #20 as held runtime PR
```

## Explicit non-goals

This convergence anchor does not authorize:

```text
runtime memory engine
raw chat transcript storage
autonomous deployment
autonomous recovery
mesh writes
bio-threat polling or dashboarding
operational pathogen detail
secret access
public scoring of people
moral authority claims
consensus hardening before live telemetry evidence
```

## Re-evaluation rule

After this docs anchor lands:

```text
review #20 again
prefer splitting broad runtime changes into small successor PRs
keep default-closed behavior as the baseline
require live endpoint/deployment-log evidence before release validation
```
