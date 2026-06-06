# Innovator Evidence Method

Lantern OS uses the operator's Innovator method for release decisions. The old
Seven smoke check is deprecated and must not be treated as a release gate.

The method now includes a scientific-rigor overlay for claim packets, claims-related work, and whitepapers. The canonical support document is `docs/CLAIM-PACKET-SCIENTIFIC-RIGOR.md`.

## Method

1. Name the artifact or surface.
2. State the exact claim it makes.
3. Classify the claim: descriptive, operational, measurement, comparative, causal, intervention, forecast, normative, myth/cultural, or unknown.
4. Tie the claim to source evidence.
5. Classify the capability being asserted.
6. Classify the boundary, consent rule, and authority limit.
7. Classify the rollback or correction path.
8. Add operational definitions for measured constructs.
9. Add uncertainty, denominator, bias/confounding, limitations, and external-validity notes.
10. Add falsification criteria and revision triggers.
11. Retire or quarantine legacy surfaces that conflict with the claim.
12. Record validation evidence.
13. Promote, hold, revise, downgrade, or reject.
14. Re-run the convergence loop before expanding scope.

## Evidence Classes

- `artifact_verified`: verified against local files, tests, commits, runtime outputs, or git state.
- `source_verified`: verified against source registry or cited external source.
- `empirical_pilot`: measured local/pilot evidence with methods and denominator stated.
- `replicated_internal`: reproduced by a second internal run or reviewer.
- `replicated_external`: reproduced by an independent party or external dataset.
- `systematic_review`: evidence synthesized through an explicit search and inclusion method.
- `model_based`: forecast, simulation, or theory with assumptions stated.
- `expert_judgment`: reviewer judgment, separated from measured evidence.
- `operator_asserted`: operator-provided and not independently verified yet.
- `llm_interpretation`: model interpretation only; cannot support a factual claim by itself.
- `inferred`: reasonable inference from evidence, marked as inference.
- `blocked`: missing evidence, contradiction, unsafe action, or inappropriate authority language.

## Certainty Classes

- `high`: direct, repeated, low-bias evidence; limitations do not materially change the claim.
- `moderate`: direct evidence with known limitations; claim is likely but bounded.
- `low`: pilot, indirect, noisy, single-run, or single-reviewer evidence; use cautious wording.
- `very_low`: hypothesis, analogy, or early signal; use roadmap/research language only.
- `blocked`: unsupported, contradicted, unsafe, or missing required review fields.

Downgrade certainty for risk of bias, imprecision, inconsistency, indirectness, selection/publication bias, unresolved counterevidence, missing denominator, stale generated artifacts, or missing replication status.

## Claim Packet Required Fields

Each promoted claim packet should record:

- packet ID, title, reviewer, review date, and intended use;
- source path and target path;
- artifact type;
- primary claim and claim kind;
- safe public wording;
- evidence class and certainty class;
- evidence bundle IDs and source references;
- validation command or check;
- validation result;
- claim scope and unit of analysis;
- operational definition;
- denominator, sample size, or observation count;
- effect size, margin, or practical significance statement when change is claimed;
- uncertainty statement;
- bias/confounding notes;
- limitations and external-validity boundary;
- counterevidence, minority report, or alternative explanations;
- replication status;
- known blockers;
- falsification criteria and revision triggers;
- rollback/removal/public-correction path;
- operator approval status.

## Whitepaper Requirements

Claims-related whitepapers must include a method box before conclusions:

```text
Methods summary:
- Claim type:
- Evidence search/source method:
- Inclusion/exclusion rule:
- Measurement or review protocol:
- Unit of analysis:
- Denominator/sample/observation count:
- Comparator or baseline:
- Analysis method:
- Uncertainty method:
- Bias/confounding review:
- Replication status:
- Limitations:
- Falsification criteria:
```

Whitepapers must separate observed, inferred, projected, and normative language. Forecasts must stay scenario-labeled. Causal and intervention claims require comparator/counterfactual language and confounder review; otherwise they must be rewritten as association, hypothesis, or roadmap claims.

## Required Release Fields

Each promoted artifact should record:

- source path;
- target path;
- artifact type;
- primary claim;
- evidence class;
- certainty class;
- validation command or check;
- validation result;
- known blockers;
- rollback/removal path;
- operator approval status.

## Deprecated Legacy Path

The old Seven audit can remain as historical context in source repos, but
Lantern OS readiness must use `docs/CONVERGENCE-LOOP.md` and the claim packet rigor standard.

## Hard Stops

- No bootloader, partition, or firmware mutation by an agent.
- No medical, legal, financial, governance, safety, privacy, or human-outcome authority claims without explicit boundary language, evidence class, uncertainty, and human review.
- No production-ready claim without validation evidence.
- No scientific, causal, intervention, or forecast claim in public copy without operational definitions, limitations, counterevidence/alternatives, and falsification criteria.
- No LLM-only evidence bundle may support a factual claim.
