# Release Manifest - HFF Convergence V0.1

Status: release-hardening artifact.

## Purpose

This manifest defines the minimum files and validation evidence required before
publishing `hff-convergence-v0.1` as a tag, release bundle, or pre-release.

## Release candidate

```text
name: hff-convergence-v0.1
status: not yet tagged
release_type: pre-release candidate until restore drill passes
```

## Required release files

The release bundle must include these files:

```text
RELEASE_MANIFEST.md
RECOVERY_README.md
MIRROR_ARCHIVE_PLAN.md
KEYSTONE_BOOTSTRAP.md
RESTORE_DRILL_CHECKLIST.md
FALSE_TRUTHS_REGISTER.md
CHECKSUMS.sha256
data/theorem-register.v0.1.json
schemas/theorem-register.v0.1.schema.json
tests/test_theorem_register.py
tests/test_schema_source_lore.py
tests/test_recovery_artifacts.py
tests/test_ci_workflow.py
```

## Required doctrine anchors

The release should include these doctrine/context files when available:

```text
HUMAN_TRANSPORTATION_BOUNDARY.md
docs/three-way-convergence-plan-2026-05-09.md
docs/three-way-durability-threat-model-2026-05-09.md
docs/safety-preserving-data-collection-consent-2026-05-09.md
docs/operator-chat-history-convergence-2026-05-09.md
docs/release-preparation-plan-convergence-v0.1-2026-05-09.md
docs/negative-outcomes-future-possibilities-convergence-2026-05-09.md
docs/imaginative-lore-100-negative-outcomes-convergence-2026-05-09.md
docs/imaginative-lore-100b-convergence-2026-05-09.md
```

## Validation commands

Run from repo root before release:

```powershell
python -m unittest discover -s tests -p "test_theorem_register.py" -t .
python -m unittest discover -s tests -p "test_schema_source_lore.py" -t .
python -m unittest discover -s tests -p "test_recovery_artifacts.py" -t .
python -m unittest discover -s tests -p "test_ci_workflow.py" -t .
python -m unittest discover -s tests -p "test_release_artifacts.py" -t .
```

## Required release gates

Do not tag or publish until:

```text
1. All validation commands pass.
2. CI workflow is merged and running on PRs/pushes to master.
3. Release bundle can be created from a clean checkout.
4. CHECKSUMS.sha256 includes required release files.
5. Restore drill checklist can be completed from a non-primary copy.
6. False truths register is reviewed before tag.
7. Mirror/archive plan has at least two non-primary destination candidates.
```

## Evidence to record in release notes

```text
commit SHA
branch or tag
validation command output
CI run identifier if available
release bundle filename
checksum file hash
source copy used for restore drill
known limitations
next review date
```

## Known limitations

```text
A release bundle preserves artifacts, not human subject-continuity.
A tag improves recoverability, not metaphysical truth.
CI validates encoded assumptions, not all possible failures.
A restore drill is still required before declaring full operational durability.
```

## Non-goals

This manifest does not authorize runtime autonomy, secret access, deployments,
medical procedures, mission booking, human traversal, copy-transfer claims,
immortality claims, AI impersonation, repo-consciousness claims, or fictional
world truth claims.
