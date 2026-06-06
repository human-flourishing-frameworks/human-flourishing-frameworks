# Claim Packet Scientific Rigor Standard

Status: canonical support document for claim packets, claim-safety reviews, whitepapers, release notes, and public-facing claims.

Scope: this standard applies to any material claim about capability, measurement, causality, forecast, risk reduction, user outcome, adoption, safety, privacy, accessibility, operational readiness, or scientific novelty.

This is not a claim of formal compliance with GRADE, PRISMA, CONSORT, NIST, or any regulatory standard. It is an internal rigor layer that borrows their discipline: explicit evidence grading, transparent reporting, uncertainty disclosure, and risk-based review.

## Method references

Use these as method anchors when a claim packet needs external methodological grounding:

- NIST AI Risk Management Framework: risk framing for AI systems, including governance, measurement, management, and trustworthiness considerations.
- GRADE: certainty-of-evidence discipline, especially risk of bias, imprecision, inconsistency, indirectness, publication bias, effect magnitude, dose-response, and plausible residual bias.
- PRISMA 2020: transparent search, screening, inclusion, and evidence-synthesis reporting for systematic review-like claims.
- CONSORT and related trial-reporting guidance: required discipline when a whitepaper makes intervention or human-outcome claims that would need controlled evaluation.

Do not cite these frameworks as endorsements. Cite them only as methodological comparators or reporting references.

## Claim strength ladder

Every claim must be assigned the lowest strength class that honestly fits the evidence.

| Class | Allowed wording | Minimum support |
|---|---|---|
| `descriptive` | "This file/service/report exists." | File path, commit, runtime output, or other direct artifact evidence. |
| `operational` | "This workflow passes listed checks in this environment." | Timestamped command output, environment notes, and failure boundary. |
| `measurement` | "This observed metric changed under these conditions." | Operational definition, denominator, measurement method, uncertainty, and raw/source reference. |
| `comparative` | "A was higher/lower/faster than B in this test." | Comparator, protocol, repeated measurement or stated single-run limitation, and confounder notes. |
| `causal` | "A caused B." | Pre-specified causal model, plausible counterfactual, confounder strategy, and limitations. |
| `intervention` | "This improves outcomes for users/patients/operators." | Human-subject or field evaluation protocol, harms/burdens, comparator, and ethics/consent boundary where applicable. |
| `forecast` | "This is plausible by a horizon." | Time horizon, base rate or model rationale, assumptions, competing forecasts, confidence range, and falsification criteria. |
| `normative` | "This should be done." | Values statement, decision context, affected parties, trade-offs, and non-authority disclaimer. |

If the evidence does not meet the minimum support for the desired class, downgrade the claim rather than inflate the language.

## Minimum claim packet fields

A release-facing claim packet must contain:

1. Packet ID, title, reviewer, review date, and intended use.
2. Primary claim, claim kind, risk class, and safe public wording.
3. Claim scope: population/system, environment, time window, and boundary conditions.
4. Unit of analysis: file, claim row, user, session, device, node, incident, run, or other explicit unit.
5. Operational definition for every measured construct.
6. Evidence bundle IDs and source references.
7. Evidence class and certainty class.
8. Method summary and analysis/protocol reference.
9. Sample size, observation count, denominator, or explicit statement that the claim is non-statistical.
10. Effect size, margin, or practical significance statement where a change is claimed.
11. Uncertainty statement: confidence interval, credible interval, sensitivity range, or qualitative uncertainty if quantitative uncertainty is not possible.
12. Bias/confounding notes and mitigation strategy.
13. Limitations and external-validity boundary.
14. Counterevidence, minority report, or alternative explanations.
15. Replication status: not replicated, internally replicated, externally replicated, or not applicable.
16. Falsification criteria and revision triggers.
17. Rollback, correction, or public amendment path.

A packet with missing methods, missing uncertainty, missing limitations, or missing falsification criteria is not ready for whitepaper, release, fundraising, medical, legal, financial, governance, or safety language.

## Evidence classes

Use the most conservative evidence class that fits:

- `artifact_verified`: direct file, commit, test, or runtime artifact evidence.
- `source_verified`: external cited source with provenance and date accessed.
- `empirical_pilot`: measured evidence from a small or local pilot, not yet replicated.
- `replicated_internal`: reproduced by a second internal run or reviewer.
- `replicated_external`: reproduced by an independent party or external dataset.
- `systematic_review`: evidence synthesized through an explicit search/inclusion method.
- `model_based`: forecast, simulation, or theoretical model with assumptions stated.
- `expert_judgment`: reviewer judgment, clearly separated from measured evidence.
- `operator_asserted`: operator-provided and not independently verified.
- `llm_interpretation`: model interpretation only; cannot support a factual claim by itself.
- `blocked`: missing evidence, unresolved contradiction, unsafe claim, or inappropriate authority language.

## Certainty classes

Use these labels in whitepapers and release packets:

- `high`: direct, repeated, low-bias evidence; limitations do not materially change the claim.
- `moderate`: direct evidence with known limitations; claim is likely but bounded.
- `low`: pilot, indirect, noisy, or single-reviewer evidence; use cautious wording.
- `very_low`: hypothesis, analogy, or early signal; use roadmap/research language only.
- `blocked`: claim is unsupported, contradicted, or unsafe to publish.

Downgrade certainty for risk of bias, imprecision, inconsistency, indirectness, publication/selection bias, unresolved counterevidence, single-reviewer dependence, stale generated artifacts, or missing denominator.

Upgrade only with clear rationale: large effect, repeated measurement, independent replication, strong mechanistic support, dose-response pattern, or conservative bias that would reduce rather than inflate the claim.

## Whitepaper methods section requirements

Every claims-related whitepaper must include a compact methods section before conclusions:

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

A whitepaper may be strategic, but any empirical-sounding claim must still be separated into observed, inferred, projected, and normative language.

## Observed/inferred/projected table

Use this table for stakeholder-facing claims:

| Claim | Status | Evidence | Certainty | Boundary | Safe wording |
|---|---|---|---|---|---|
| Directly observed fact | observed | file/test/runtime/source ref | moderate/high | exact environment | "Observed in this run." |
| Reasoned interpretation | inferred | observed facts plus rationale | low/moderate | assumptions listed | "Suggests" / "is consistent with." |
| Future state | projected | forecast model or roadmap | very_low/low | horizon and assumptions | "Scenario" / "target" / "planned." |
| Recommendation | normative | values/trade-off statement | separate from evidence certainty | decision context | "We recommend because..." |

## Causal and intervention claims

Do not make causal or intervention claims from anecdotes, single examples, model output, or before/after observations alone. A causal claim needs, at minimum:

- a pre-specified causal graph or mechanism;
- comparator or counterfactual;
- time ordering;
- confounder inventory;
- sensitivity analysis or explicit caveat;
- falsification test;
- harms and unintended-effects review.

If these are absent, rewrite causal language as association, compatibility, or hypothesis language.

## Forecast claims

Forecasts stay quarantined as scenarios unless an operator approves their use for planning. A forecast packet must state:

- horizon and event definition;
- base rate or reference class;
- assumptions;
- confidence range;
- competing forecasts or alternative scenarios;
- leading indicators;
- falsification conditions;
- what actions are allowed and disallowed because of the forecast.

Forecasts must not be rewritten as facts. A forecast may trigger review; it may not update accepted belief by default.

## Safe public language

Allowed:

- "Pilot evidence suggests..."
- "In this repository snapshot..."
- "This claim is supported by the listed evidence and limited to the stated scope."
- "The result is consistent with..."
- "The forecast is a scenario, not an operational fact."

Disallowed unless separately proven:

- "proven"
- "guaranteed"
- "clinically validated"
- "scientifically proven"
- "statistically significant" without test, denominator, and method
- "production ready" without release gates
- "safe" without risk class, threat model, and residual-risk statement
- "causes" without causal design
- "predicts the future" or equivalent authority language

## Release decision rule

A claim packet may move into a whitepaper or public release only when:

1. `ClaimSafetyClassification.can_be_accepted_candidate()` is true for normal factual claims.
2. `ClaimSafetyClassification.can_be_scientific_claim_candidate()` is true for scientific, measurement, causal, intervention, or forecast claims that are presented as evidence-backed.
3. `EvidenceBundle.can_support_scientific_claim()` is true for every scientific evidence bundle.
4. `ClaimPacket.can_release()` is true for the release-facing packet.
5. High-impact, medical, legal, financial, governance, autonomy, privacy, security, or catastrophic-risk claims have explicit human review and safe public wording.

If any condition fails, the claim remains internal, is downgraded to roadmap/hypothesis language, or is blocked.
