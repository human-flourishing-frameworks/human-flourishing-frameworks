# Claim Packet Template

Use this template for claim packets, whitepaper claims, release notes, investor/stakeholder packets, public-copy claims, and internal claims that may later become public.

Canonical rigor standard: `docs/CLAIM-PACKET-SCIENTIFIC-RIGOR.md`.

## 1. Packet metadata

| Field | Value |
|---|---|
| Packet ID |  |
| Title |  |
| Reviewer |  |
| Review date |  |
| Intended use | internal / whitepaper / release / public copy / investor / other |
| Decision context |  |
| Related artifact path(s) |  |
| Related issue/PR/commit |  |

## 2. Primary claim

| Field | Value |
|---|---|
| Claim ID |  |
| Exact claim text |  |
| Safe public wording |  |
| Claim kind | descriptive / operational / measurement / comparative / causal / intervention / forecast / normative / myth / scenario / unknown |
| Risk class | normal / high_impact / catastrophic / autonomy / security / privacy / p_doom |
| Claim scope | population/system, environment, time window, boundary conditions |
| Unit of analysis | file / row / user / session / device / node / incident / run / other |
| Operational definition |  |

## 3. Evidence bundle

| Field | Value |
|---|---|
| Evidence bundle ID(s) |  |
| Source references | file paths, commits, tests, runtime logs, external sources |
| Evidence class | artifact_verified / source_verified / empirical_pilot / replicated_internal / replicated_external / systematic_review / model_based / expert_judgment / operator_asserted / llm_interpretation / blocked |
| Certainty class | high / moderate / low / very_low / blocked |
| Provenance reference(s) |  |
| Validation command/check |  |
| Validation result |  |
| Denominator/sample/observation count |  |
| Effect size/margin/practical significance |  |
| Uncertainty statement | confidence interval / credible interval / sensitivity range / qualitative uncertainty |

## 4. Method box

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

## 5. Scientific method mapping

| Step | Packet entry |
|---|---|
| Observation/problem |  |
| Research/source review |  |
| Hypothesis or claim |  |
| Prediction or expected observation |  |
| Test/measurement plan |  |
| Analysis rule |  |
| Conclusion boundary |  |
| Revision/falsification trigger |  |

## 6. Bias, limitations, and alternatives

| Field | Value |
|---|---|
| Bias/confounding notes |  |
| Mitigation strategy |  |
| Limitations |  |
| External-validity boundary |  |
| Counterevidence |  |
| Minority report |  |
| Alternative explanations |  |
| Replication status | not replicated / internally replicated / externally replicated / not applicable |

## 7. Forecast fields, if applicable

| Field | Value |
|---|---|
| Time horizon |  |
| Event definition |  |
| Base rate/reference class |  |
| Assumptions |  |
| Confidence range |  |
| Competing forecasts/scenarios |  |
| Leading indicators |  |
| Falsification conditions |  |
| Allowed actions |  |
| Disallowed actions |  |

## 8. Causal or intervention fields, if applicable

| Field | Value |
|---|---|
| Causal mechanism |  |
| Comparator/counterfactual |  |
| Time-ordering evidence |  |
| Confounder inventory |  |
| Sensitivity analysis/caveat |  |
| Harms and unintended effects |  |
| Ethics/consent boundary |  |

If these fields cannot be completed, rewrite the claim as association, compatibility, hypothesis, pilot signal, or roadmap language.

## 9. Decision

| Field | Value |
|---|---|
| Classification | accepted_candidate / unsupported / overclaim / impossible_claim / forecast_quarantine / cultural_context / needs_review |
| Verdict | supports / refutes / not_enough_info |
| Required action | promote / hold / revise / downgrade / reject / public correction |
| Human review required | yes / no |
| Reviewer note |  |
| Rollback/removal/public-correction path |  |
| Revision triggers |  |

## 10. Safe-language rewrite

Original wording:

> 

Safe replacement:

> 

Rationale for rewrite:

> 

## 11. Release checklist

- [ ] Evidence bundle has non-LLM support.
- [ ] Source classifications are present.
- [ ] Provenance is present.
- [ ] Disagreements have minority report or counterevidence handling.
- [ ] Operational definition is present.
- [ ] Denominator/sample/observation count is present or explicitly not applicable.
- [ ] Uncertainty is stated.
- [ ] Limitations are stated.
- [ ] External-validity boundary is stated.
- [ ] Falsification criteria are stated.
- [ ] Safe public wording is present.
- [ ] High-impact claims received human review.
- [ ] Forecasts remain scenario-labeled unless separately approved for planning.
- [ ] Causal/intervention claims have comparator or counterfactual support.
- [ ] Unsupported claims are downgraded or blocked.
