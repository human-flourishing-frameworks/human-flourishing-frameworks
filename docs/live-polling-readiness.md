# Live Polling Readiness

Status: teaching/research-grade
Last reviewed: 2026-06-01

## Enabling live sensors

Set `ENABLE_LIVE_SENSORS=true` to activate live observation polling.

The runtime health endpoint is `/api/world/status`.

## Sensor status fields

The `live_observation_status` response includes:

| Field | Meaning |
|-------|---------|
| `status_reason` | Why the sensor is in its current state |
| `last_error_count` | Errors since last successful poll |
| `ran_with_updates` | Whether the latest run produced belief updates |
| `failed` | Whether the sensor is in a failed state |

## Status reason values

| Value | Meaning |
|-------|---------|
| `not_enabled` | `ENABLE_LIVE_SENSORS` is not set |
| `registered_not_run` | Sensor registered but hasn't polled yet |
| `running` | Sensor is currently polling |
| `ran_no_measurements` | Poll completed, no data returned |
| `ran_with_measurements_no_updates` | Data returned but no belief updates |
| `ran_with_updates` | Data returned and beliefs updated |
| `failed` | Poll threw an error |

## Consensus note

PBFT consensus is not required for live polling to start. Each node polls independently.
