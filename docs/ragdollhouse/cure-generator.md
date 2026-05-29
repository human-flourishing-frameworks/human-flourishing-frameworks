# `!cure-generator` (Speculative, WebMD-like)

This repo includes a local-first speculative packet generator meant for **care coordination** and **question lists**.

It is intentionally *non-diagnostic*:
- not a cure finder,
- not a treatment recommender,
- not a patent/novelty engine,
- not a substitute for clinician judgment.

## Input schema

See `../../schemas/cure-generator-input.v0.1.json`.

## Generate a packet

The generator consumes JSON and outputs Markdown:

```powershell
python tools/cure_generator.py --in .\input.json --out .\packet.md
```

## Safe defaults

- Keep `patient_label` minimal (avoid DOB/address/insurance IDs in version-controlled files).
- Use `speculative_buckets` for “plausible buckets to discuss” (not claims).
- Use `questions_for_team` for the actual value: faster clarification, less drift, safer escalation.

