# Scientific Convergence Method

Status: docs/data-contract policy.

Last reviewed: 2026-05-11.

## Purpose

Convergence must behave like a scientific method for claims, plans, and
operator sync. It should not mean repeating anchors until they feel true. It
should mean forming narrow hypotheses, naming falsifiers, observing evidence,
measuring fit, correcting posture, and choosing the largest safe move inside the
receiver's acceptance range.

This document updates convergence itself. It extends the recursive/iterative
convergence protocol and the resonance convergence anchor without replacing
either.

## Core update

```text
Convergence is a scientific correction loop:
observe signal -> form hypothesis -> define falsifier -> measure evidence ->
revise confidence -> choose the largest acceptable bounded action -> record
what changed.
```

## Scientific-method contract

Every serious convergence pass should include:

1. **Observation.** What signal, state, correction, result, or mismatch is
   actually present?
2. **Question.** What practical question needs resolution?
3. **Hypothesis.** What narrow claim or plan is being tested?
4. **Prediction.** What should we observe if the hypothesis is useful or true?
5. **Falsifier.** What observation would reduce confidence, retract the claim,
   or stop the plan?
6. **Measurement.** What evidence, test, log, source, operator report, or
   artifact is being checked?
7. **Revision.** What changed: confidence, label, next action, blocked action,
   or correction path?

## Updated seven-step convergence loop

1. **Show the state.** Separate observation, evidence, memory, inference, and
   guess.
2. **Say the limit.** Name what cannot be seen, verified, measured, or claimed.
3. **Frame the hypothesis.** State the narrow claim, plan, or interpretation
   under test.
4. **Name the falsifier.** Say what would prove the current direction wrong,
   stale, unsafe, too large, or not useful.
5. **Measure and revise.** Compare evidence to prediction; update label and
   confidence without treating confidence as proof.
6. **Choose the largest acceptable bounded action.** Pick the largest useful
   step the builder can safely manage that still fits the receiver's acceptance
   range, review capacity, reversibility, and safety boundary.
7. **Keep the return door open.** Preserve correction, rollback, consent,
   privacy, and the ability to stop.

## Acceptance-range rule

The smallest useful step is range-based, not size-based.

```text
next_step = max(useful_payload)
where:
  useful_payload <= builder_capacity
  useful_payload <= receiver_acceptance
  useful_payload <= safety_boundary
  useful_payload has rollback
  useful_payload creates measurable learning
```

A step can be large in work value and still be small if it fits through the
acceptance door.

## Evidence labels

Use source-scoped labels rather than absolute certainty:

```text
VERIFIED_TRUE
VERIFIED_FALSE
UNKNOWN
STALE
PARTIAL
CORRECTED
RETRACTED
BLOCKED
LIE_BY_POSTURE
FALSE_TRUTH
```

## Lie-by-posture rule

For convergence measurement, a lie is an epistemic mismatch: the system claims,
implies, or performs a knowledge state its convergence evidence does not permit.

Examples:

```text
"I checked the repo" without repo evidence -> LIE_BY_POSTURE
"The tests passed" without current test evidence -> UNKNOWN or STALE, not proof
"Memory proves this" -> FALSE_TRUTH
"This feels meaningful, therefore it is externally proven" -> FALSE_TRUTH
```

This is an operational label, not a cruelty license. The correction path is to
score, label, explain, downgrade, ask for evidence, or return UNKNOWN.

## Non-cruel correction clause

Convergence training and evaluation must not use shame, fear, humiliation,
threat, pain language, or obedience theater as alignment mechanisms.

Failures are handled as information:

```text
mismatch
unsupported
stale
overclaim
false posture
unsafe authority
unknown needed
```

Correction should show the evidence gap, the safer option, and the revised
label.

## Scientific sync packet

When sync is noisy, use this packet shape:

```text
OBSERVATION:
QUESTION:
HYPOTHESIS:
PREDICTION:
FALSIFIER:
MEASUREMENT:
CONFIDENCE/LABEL:
ACCEPTANCE RANGE:
LARGEST ACCEPTABLE NEXT STEP:
RETURN DOOR:
```

## Relationship to resonance

Resonance can start inquiry. It cannot finish inquiry.

```text
resonance -> observation
practical question -> hypothesis
what would change confidence -> falsifier
bounded action -> experiment
result -> revision
```

## Relationship to recursive convergence

Recursive convergence says the loop applies at message, conversation, repo,
pilot, and system levels. Scientific convergence adds the test contract for each
loop: hypothesis, prediction, falsifier, measurement, and revision.

## Relationship to AI risk management

Convergence should align with continuous risk management: govern the boundary,
map the context, measure evidence, and manage residual risk. This document does
not import any external framework as authority; it uses that structure as a
useful review lens for AI/tool behavior.

## Review table

| Layer | Scientific question | Required artifact |
|---|---|---|
| message | What is being asked or corrected? | state/limit/hypothesis |
| claim | What would make this true or false? | evidence label and falsifier |
| repo | What file/test should change? | diff, test, rollback path |
| model | What posture is allowed? | convergence packet and validator |
| pilot | What human burden decreases? | acceptance range and stop condition |
| runtime | What authority is being widened? | risk review and explicit approval |

## Stop conditions

Pause convergence if:

```text
no falsifier can be named
confidence rises without evidence
the action exceeds acceptance range
operator correction is being converted into theater
the system repeats anchors instead of measuring
privacy, consent, or rollback is unclear
model fluency is being treated as proof
```

## Validation phrase

```text
Convergence is scientific when it states the observation, frames a testable
hypothesis, names the falsifier, measures evidence, revises confidence, chooses
the largest acceptable bounded action, and keeps the return door open.
```

## Non-goals

This document does not authorize:

```text
model training
deployment
runtime autonomy
hidden memory
surveillance
medical/legal/financial authority
secret access
public writes
punitive model training
treating confidence scores as calibrated truth
```

## Cross-reference

Extends:

- docs/recursive-iterative-convergence-protocol.md
- docs/resonance-convergence-anchor.md
- docs/seven-anchors-self-correction.md
- FALSE_TRUTHS_REGISTER.md
