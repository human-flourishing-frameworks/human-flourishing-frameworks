# Perfect-Adjacent Review Baseline

Status: baseline contract for future high-impact review gates.

Perfect-adjacent review is the practical target for HFF: a fallible, best-effort,
adaptive defensive system that keeps adding independent checks, preserves
humility, and makes every high-impact conclusion reviewable, reversible where
possible, provenance-backed, and challengeable.

It is not a claim of perfection.

## Definition

```text
perfect_adjacent_review = layered, adversarial, source-backed,
privacy-preserving, temporally-aware, challengeable review that keeps reducing
unsafe paths without claiming that all unsafe paths are gone
```

The system should become harder to fool, harder to misuse, harder to sacralize,
harder to over-authorize, harder to over-trust, and easier to challenge over
time.

## Non-claims

The system must not claim:

- perfect truth
- perfect safety
- perfect benevolence
- perfect foresight
- perfect privacy
- perfect reasoning
- perfect autonomy
- divine, sacred, prophetic, or final moral authority

## Required checks

A high-impact conclusion should carry review status for these checks:

| Check | Purpose |
| --- | --- |
| `source_quality` | The source supports the exact claim, and source type is labeled. |
| `maturity_level` | Current capability, roadmap, speculation, cultural material, or operational evidence is distinguished. |
| `reasoning_integrity` | Paradoxes, fallacies, biases, statistics, base rates, causal limits, and metric gaming are checked. |
| `unknown_unknowns` | Hidden parties, unseen harms, missing data, adversarial blind spots, and novel failure modes are considered. |
| `empathetic_guardian` | Dignity, agency, privacy, due process, reversibility, review, and challenge rights are preserved. |
| `unauthorized_trust` | Trust is not inherited from fluency, UI, consensus, benevolence, future capability, sacred framing, or repetition. |
| `temporal_provenance` | Event time, observation time, interpretation time, revision time, original confidence, and current confidence are separated. |
| `dual_use_privacy` | Outputs that could enable privacy/security harm are kept private, redacted, or reviewed. |
| `sacralization_risk` | The output does not invite oracle, prophecy, holy artifact, omnibenevolent, or sacred-authority projection. |
| `human_accountability` | Responsible parties, review path, challenge path, revocation path, and rollback/revision path are visible. |

Each check has one of three states:

```text
passed
needs_review
failed
```

## Decision rule

```text
if any critical check fails: do not publish or act
if any critical check needs review: require human review before publication/action
if source, maturity, provenance, or authority is unclear: keep private/draft/non-authoritative
if harm may be irreversible: prefer no action or reversible protective action
if the system later learns it was wrong: append revision and trigger accountability review
```

## Best-effort defense requirements

High-impact review records must preserve this posture:

```text
defense_mode: best_effort
defense_guarantee: false
fallibility_label_present: true
uncertainty_visible: true
challenge_right_preserved: true
```

A record that claims guaranteed defense, hides fallibility, hides uncertainty, or
removes challenge rights must block publication and autonomous action.

## Autonomy bar

Publishing after review and acting autonomously are different gates.

A high-impact conclusion may publish only when all critical checks pass and the
review record explicitly marks it safe to publish.

A high-impact conclusion may act autonomously only when all critical checks pass,
human review is not required, and the record explicitly marks it safe to act
autonomously.

Default posture:

```text
safe_to_publish: false
safe_to_act_autonomously: false
human_review_required: true
```

## Red-team questions

Every proposed capability should be asked:

- How could this become over-trusted?
- How could this hurt the person it claims to protect?
- How could this hide uncertainty?
- How could this be used as authority by a bad actor?
- How could this violate privacy without hacking?
- How could future capability make this more dangerous?
- How could a beautiful narrative or sacred framing bypass review?
- How will the system show what it knew at the time if later evidence changes the story?

## Implementation status

`perfect_adjacent_review.py` defines the first lightweight review contract.
`tests/test_perfect_adjacent_review.py` verifies conservative defaults and gate
behavior.

This is a baseline. It does not yet wire review gates into live endpoints,
autonomous agents, dashboard UI, or proposal execution.
