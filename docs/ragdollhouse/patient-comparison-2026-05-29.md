# Patient Comparison — 2026-05-29

Goal: reduce drift by comparing the active patient artifacts indexed in `docs/ragdollhouse/index.md`.

## Comparison table (high-level)

| Patient | Primary artifact | Primary domain | Current acuity signal | Best next action | Biggest unknowns |
|---|---|---|---|---|---|
| Patient A | `PATIENT-A-500Y-HARDENING-PLAN.md` | Long-horizon safety + continuity doctrine | Not an acute episode (plan document) | Keep as governance/safety baseline | What “current episode” is (if any); what needs refresh |
| Patient C (Courtney B.) | `COMET-LEAP-PATIENT-C-CARE-PACKET.md` (2026-05-26) | Care coordination packet (mood/sleep/pain/OB-GYN) | Moderate (high pain + bleeding + mental health load) | PCP + OB-GYN + behavioral health intake sequencing | Lab results; appointment outcomes; symptom tracker week 1 |
| Tonda Cleaver | `tonda-cleaver-care-convergence-2026-05-29.md` (2026-05-29) | Post-op hospitalization coordination | Potentially high (hospitalized + “pretty sick”) | Clarify current inpatient diagnosis + rule-out major complications | Exact surgery + indication; infection/leak status; nutrition + glucose plan |

## Cross-patient convergence patterns (what repeats)

- “Single entrypoint” reduces chaos: a PCP/surgeon/hospitalist point-person plus a short question list.
- A written 7-day plan is useful only when the diagnosis/complication bucket is known.
- In all packets: keep red-flag escalation logic explicit and short.

## Next update trigger

Update these packets when any of the following happens:
- a diagnosis is named (e.g., leak/fistula, infection, obstruction, diabetes),
- a new test result arrives (labs/imaging),
- a follow-up appointment is scheduled/completed,
- meds or diet plan changes materially.

