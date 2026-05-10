# Safe Background Mode

Status: opt-in runtime boundary.

## Purpose

Background mode proves the service can run a bounded worker without changing the public model or deployment authority.

## Default

```text
HFF_BACKGROUND_MODE=false
```

When disabled, no background worker starts.

## Enabled behavior

When explicitly enabled with:

```text
HFF_BACKGROUND_MODE=true
```

HFF may start one in-process heartbeat-only worker.

Allowed behavior:

```text
in-memory heartbeat tick
visible /background/status state
visible /healthz background state
safe shutdown on process exit
```

Not included in this mode:

```text
external calls
sensor polling
mesh activity
write endpoints
profile collection
device enrollment
location logic
analytics
SDK/APK behavior
actuator behavior
queue execution
agent autonomy
```

## Public proof

```text
GET /background/status
GET /healthz
```

Pass condition:

```text
background_mode.enabled is explicit
background_mode.side_effects.network=false
background_mode.side_effects.live_sensors=false
background_mode.side_effects.mesh_sync=false
background_mode.side_effects.public_writes=false
background_mode.side_effects.personal_data=false
background_mode.side_effects.device_or_actuator_control=false
```

## Expansion rule

Any expansion beyond heartbeat-only requires a separate reviewed PR with a specific purpose, bounded input, bounded output, stop path, idempotency story, least-privilege story, observability story, and tests.
