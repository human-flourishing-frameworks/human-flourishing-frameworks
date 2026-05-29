# Live Polling Readiness

This checklist explains when live polling may move from documentation to a
teaching/research-grade runtime path. PBFT consensus is not required for live polling to start; the first gate is clear operator visibility and honest statusing.

## Enablement

- Set `ENABLE_LIVE_SENSORS=true` only when the operator wants real polling.
- Use `/api/world/status` as the public status surface.
- Preserve `live_observation_status`, `status_reason`, `last_error_count`, and
  `ran_with_updates` in the status payload.

## Operator Status Reason Table

| status | status_reason | Meaning |
|---|---|---|
| not_enabled | operator has not enabled live polling | safe default-closed state |
| registered_not_run | sensor exists but has not executed yet | configuration present, no live evidence yet |
| running | poll currently in flight | transient active state |
| ran_no_measurements | poll completed but returned nothing | network or source gap without fake certainty |
| ran_with_measurements_no_updates | measurements arrived but beliefs were unchanged | evidence seen, no score movement |
| ran_with_updates | measurements arrived and updates were applied | positive live evidence path |
| failed | runtime error or source break occurred | operator review required before trust increases |

## Runtime Expectations

- `failed` must remain visible to the operator.
- `ran_with_updates` should only appear after a real observation pass.
- `status_reason` should explain whether the system is not enabled, registered
  but idle, actively running, or blocked by an error.
- `last_error_count` should increase when a poll fails and remain inspectable.
