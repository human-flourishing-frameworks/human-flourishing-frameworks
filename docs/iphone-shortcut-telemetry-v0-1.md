# iPhone Shortcut Telemetry V0.1

Status: implemented as operator Shortcut recipe using the existing adoption heartbeat surface.

Last reviewed: 2026-05-09.

## Purpose

Add a small amount of useful iPhone telemetry without adding a new runtime endpoint or collecting private phone data.

V0.1 builds on the already-working iPhone adoption heartbeat:

```text
POST /api/adoption/register
platform: iphone_shortcuts
node_name: Alex iPhone
```

## Telemetry allowed in V0.1

Allowed coarse telemetry:

```text
battery_level_percent
battery_state: charging | unplugged | full | unknown
manual_mode: awake | working | sleep_soon | traveling | unknown
shortcut_version
```

Do not collect or transmit by default:

```text
precise GPS location
contacts
messages
call logs
photos
microphone/audio
camera/video
health data
biometrics
sleep data
calendar contents
browser history
raw notification content
```

## Why this version uses existing fields

The current adoption schema already stores visible node metadata:

```text
version
region
operator_type
deployment_type
```

Until HFF adds a dedicated phone telemetry endpoint/table, the iPhone Shortcut can encode coarse telemetry into those existing metadata fields.

This avoids a runtime migration while still proving that the phone can report more than bare liveness.

## Recommended Shortcut actions

In the existing `HFF Heartbeat` Shortcut, add these actions before `Get Contents of URL`:

```text
Get Battery Level
Set Variable: BatteryLevel

Get Battery State
Set Variable: BatteryState

Text: awake
Set Variable: ManualMode
```

For manual mode, Alex can duplicate the shortcut or edit the `Text` value before running:

```text
awake
working
sleep_soon
traveling
unknown
```

## Updated JSON body

Use the same URL and token as the working heartbeat.

Update the JSON body to:

```json
{
  "node_id": "alex-iphone-001",
  "node_name": "Alex iPhone",
  "platform": "iphone_shortcuts",
  "version": "phone-heartbeat-v0.1 battery=${BatteryLevel}",
  "region": "coarse_only",
  "operator_type": "owner_operator mode=${ManualMode}",
  "deployment_type": "personal_phone_sensor battery_state=${BatteryState}",
  "node_public_key": ""
}
```

In Shortcuts, insert the variables using the variable picker rather than typing `${BatteryLevel}` literally.

## Expected visible result

After running the shortcut, check:

```text
GET /api/adoption/nodes
```

Expected node entry should still show:

```text
name: Alex iPhone
platform: iphone_shortcuts
```

and should now expose coarse telemetry inside visible metadata fields, for example:

```text
version: phone-heartbeat-v0.1 battery=83
operator_type: owner_operator mode=working
deployment_type: personal_phone_sensor battery_state=charging
region: coarse_only
```

## Limits

This is not a real phone telemetry table yet. It is a low-friction V0.1 bridge using existing adoption metadata.

A later V1 can add:

```text
POST /api/operator/phone/heartbeat
GET /api/operator/phone/latest
phone-specific token
bounded schema validation
separate retention policy
explicit privacy review
```

## Safety boundary

Do not use this telemetry to infer private health, sleep, location, or emotional state as fact.

Treat it as:

```text
operator-controlled coarse phone heartbeat metadata
```

not as:

```text
surveillance
medical data
verified sleep data
precise location
private personal-state proof
```

## Validation checklist

```text
1. Run HFF Heartbeat from iPhone.
2. Confirm Shortcut returns success.
3. Open /api/adoption/nodes.
4. Confirm Alex iPhone appears.
5. Confirm battery and mode metadata are visible.
6. Confirm no token, location, health, contact, message, audio, camera, or notification data appears.
```
