# PR #20 Runtime Split and Review Plan

Status: PR-branch review note.

Last reviewed: 2026-05-09.

This document is intentionally added to the PR #20 branch only as low-risk review
metadata. It does not authorize merging PR #20 as-is.

It adds no runtime code, endpoint, workflow trigger, deployment behavior,
secret handling, live polling, mesh write behavior, or autonomous authority.

## Current PR state

```text
PR: #20 Add bio-threat registry and runtime safety gates
state: open
stage: draft
mergeable: false
base: master
head: codex/read-only-bio-threat-source-registry
changed files before this note: 16
best action: split or refresh, not merge as-is
```

## Why this note exists

PR #20 bundles several distinct risk surfaces:

```text
bio-threat source registry
runtime autonomous escalation executor gate
mesh sync write gate
false-narrative copy tests
release checklist / live smoke expectations
CI workflow changes
README/public wording changes
Railway config / dependency surface
```

After the convergence docs landed on `master`, the safest next step is not to add
more runtime behavior to this branch. The safest next step is to preserve the
review record and split remaining work into smaller successor PRs.

## Source doctrine now available on master

The split should be evaluated against these master docs:

```text
docs/convergence-status.md
docs/keystone-memory-contract.md
docs/capability-confidence-model.md
docs/keystone-self-convergence.md
docs/keystone-table-door-anchors.md
docs/world-system-priority-model.md
docs/traversal-protocol.md
docs/keystone-autonomous-work-queue.md
docs/keystone-source-use-discipline.md
docs/keystone-chatgpt-export-intake.md
docs/keystone-claude-export-intake.md
docs/keystone-shell-command-discipline.md
```

Current governing line:

```text
runtime remains held until source-use, export-risk, shell/action-claim, and
runtime validation issues are classified.
```

## Successor PR candidates

| Candidate PR | Scope | Risk | Finish confidence | Notes |
|---|---|---:|---:|---|
| Release checklist / smoke evidence | `RELEASE_CHECKLIST.md` only | low | 0.88 | Capture live checks without claiming they passed. |
| False-narrative copy guard | `tests/test_false_narrative_copy.py` plus minimal copy edits | medium | 0.80 | Prevent unsupported claims of autonomy, live truth, or self-correction. |
| Bio-threat registry docs/data only | `BIO_THREAT_SOURCE_REGISTRY.md`, read-only registry data, no polling/dashboard/response | medium | 0.78 | Keep operational pathogen detail excluded. |
| Autonomous executor default-off gate | `agent_system.py` and focused tests only | high | 0.68 | Must prove no executor thread starts unless explicitly enabled. |
| Mesh sync default-closed gate | `mesh_network.py`, `app.py`, mesh contract tests only | high | 0.64 | Must prove default 403 for write-like sync. |
| CI workflow test discovery | `.github/workflows/tests.yml` only | medium-high | 0.62 | CI changes alter validation trust and need script-injection review. |
| Railway/dependency cleanup | `railway.toml`, `requirements.txt` only if still needed | medium | 0.56 | Needs live deploy/log evidence before claiming release impact. |
| README/public wording cleanup | README only | low-medium | 0.74 | Should be based on current master docs and running-service truth. |

## Split order recommendation

```text
1. Release checklist / smoke evidence docs
2. False-narrative copy guard
3. Bio-threat registry docs/data only
4. Autonomous executor default-off gate
5. Mesh sync default-closed gate
6. CI workflow test discovery
7. Railway/dependency cleanup if still needed
8. README/public wording cleanup after runtime truth is verified
```

Reasoning:

```text
start with docs and public-claim safety
then isolate data-only registry work
then touch runtime gates one at a time
leave CI and deployment-adjacent surfaces late because they affect validation trust
avoid README truth claims until runtime evidence is fresh
```

## Per-file disposition

| File in PR #20 | Recommended disposition | Reason |
|---|---|---|
| `BIO_THREAT_SOURCE_REGISTRY.md` | split into data/docs-only PR | Lower risk if kept separate from runtime gates. |
| `bio_threat_source_registry.py` | split only after data contract review | Python data module may still be safe, but must exclude operational details. |
| `tests/test_bio_threat_source_registry.py` | follow registry split | Tests are useful but should travel with scoped registry work. |
| `agent_system.py` | split into executor-gate PR | Runtime autonomy surface; needs narrow review. |
| `tests/test_autonomous_executor_gate.py` | follow executor-gate split | Required focused evidence for default-off behavior. |
| `mesh_network.py` | split into mesh-gate PR | Network/write-like surface; high caution. |
| `app.py` | split only if needed by mesh/runtime gate | App route changes broaden runtime risk. |
| `tests/test_mesh_sync_contract.py` | follow mesh-gate split | Required focused evidence for default-closed behavior. |
| `tests/test_app_runtime_safety.py` | split with runtime gate it validates | Avoid broad mixed validation. |
| `tests/test_false_narrative_copy.py` | split early as copy-safety PR | Low runtime risk and useful guardrail. |
| `.github/workflows/tests.yml` | separate CI PR | Workflow changes affect trust signals and shell-injection surface. |
| `RELEASE_CHECKLIST.md` | split first or keep as docs-only | Low risk and clarifies live validation requirements. |
| `README.md` | defer or split late | README should track current truth, not PR-branch aspiration. |
| `railway.toml` | defer | Deployment-adjacent; needs live deploy/log evidence. |
| `requirements.txt` | defer unless required by isolated tests | Dependency changes can affect runtime. |
| `tests/test_world_model_shape.py` | only keep if tied to scoped change | Avoid unrelated test drift. |

## Review gates for each successor PR

Every successor PR must state:

```text
scope
non-goals
files changed
risk class
expected tests
manual checks if any
rollback path
operator approval required before merge/deploy
```

Minimum acceptance:

```text
fresh branch from current master
small file-area scope
focused tests for that scope
full unittest discovery passing when runtime/test files are touched
no secrets or env var exposure
no public-write reopening
no default-on live polling
no default-on executor
no default-on mesh writes
no operational pathogen instructions
clear rollback or closure path
```

## Runtime successor hard stops

Stop and require Alex review if any successor PR:

```text
enables live polling by default
enables autonomous executor behavior by default
enables mesh writes by default
adds background workers
adds scheduled monitoring
adds secret reads or token handling
adds public authority claims
adds operational bio-threat detail
changes deployment behavior
changes CI shell execution of untrusted input
requires env vars or credentials
```

## GitHub Actions shell-injection guard

Workflow changes must treat GitHub event fields as untrusted. Relevant dangerous
inputs include issue titles, issue bodies, PR titles, PR bodies, labels, branch
names, commit messages, and other flexible text fields.

Safe pattern:

```text
pass untrusted fields through environment variables or structured files
quote them for the target shell
avoid direct interpolation into inline run scripts
prefer narrow actions/tools over arbitrary shell where possible
```

Unsafe pattern:

```text
run: |
  echo "${{ github.event.issue.title }}"
  some-shell-command "${{ github.event.issue.body }}"
```

Required successor evidence for CI workflow changes:

```text
show the exact untrusted contexts used
show how they are quoted/escaped or avoided
show that no issue/PR text is interpreted as shell code
```

## Export and action-claim lessons folded into review

Recent Keystone/export review adds two extra checks for successor PRs:

```text
action claims require evidence
shell commands must be shell/host/path/risk scoped
```

Successor PR bodies should not claim commands, tests, endpoint checks, or tool
actions happened unless they include evidence such as:

```text
exit code
stdout/stderr summary
commit SHA
workflow run
PR/issue number
file diff
live endpoint result
```

Unverified model narration must not be treated as proof.

## Live-release evidence remains separate

A PR passing tests is not the same as live service validation.

Before any release claim, require fresh live evidence:

```text
GET /health -> expected HTTP 200
GET /api/status -> expected HTTP 200 and expected status JSON
GET /api/autonomous/status -> expected auto_execute_escalations_enabled=false unless explicitly enabled
POST /api/mesh/sync -> expected default HTTP 403 unless ENABLE_MESH_SYNC=true
```

If the running service and GitHub disagree:

```text
say so plainly
do not call GitHub truth live truth
do not call passing tests a deployment validation
require operator/deployment evidence before release claims
```

## Close/keep decision for PR #20

Recommended near-term state:

```text
keep PR #20 open as draft while successor PRs are planned
use this branch as review evidence and file-area inventory
do not mark ready for review
do not merge as-is
```

Recommended closure condition:

```text
Once successor PRs are created or explicit decisions are recorded for each file
area, close PR #20 as superseded by smaller scoped PRs.
```

## Confidence table

| Decision | Confidence |
|---|---:|
| Keep PR #20 draft for now | 0.97 |
| Do not merge PR #20 as-is | 0.95 |
| Split docs/checklist first | 0.88 |
| Split false-narrative guard early | 0.80 |
| Split bio-threat registry separately | 0.78 |
| Split executor gate separately | 0.68 |
| Split mesh gate separately | 0.64 |
| Defer CI workflow change until shell-injection review | 0.86 |
| Defer Railway/dependency changes until live evidence exists | 0.82 |
| Close PR #20 immediately without successor mapping | 0.35 |
| Mark PR #20 ready now | 0.18 |

## Non-goals

This note does not authorize:

```text
merging PR #20 as-is
marking PR #20 ready for review
deploying runtime code
enabling live polling
enabling autonomous executor behavior
enabling mesh writes
closing #18
storing raw chat/export logs
running shell commands
claiming live service health without endpoint/log evidence
```
