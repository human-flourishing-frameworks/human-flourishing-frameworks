#!/usr/bin/env python3
"""Privacy-bounded iPhone Shortcut telemetry sensor.

This module adapts coarse, operator-approved phone heartbeat payloads into the
existing HFF sensor/measurement model. It intentionally does not add a runtime
endpoint and does not collect private phone data by default.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Mapping, Optional

from sensors import Measurement, Sensor


ALLOWED_PHONE_TELEMETRY_FIELDS = frozenset({
    "device_id",
    "battery_level",
    "battery_state",
    "manual_mode",
    "shortcut_version",
    "operator_note",
    "recorded_at",
})

BLOCKED_PHONE_TELEMETRY_FRAGMENTS = (
    "location",
    "gps",
    "latitude",
    "longitude",
    "coordinate",
    "address",
    "contact",
    "message",
    "call_log",
    "photo",
    "microphone",
    "audio",
    "camera",
    "video",
    "health",
    "biometric",
    "sleep",
    "calendar",
    "browser_history",
    "notification",
)

ALLOWED_BATTERY_STATES = frozenset({"charging", "unplugged", "full", "unknown"})
ALLOWED_MANUAL_MODES = frozenset({"awake", "working", "sleep_soon", "traveling", "unknown"})
MAX_DEVICE_ID_LENGTH = 80
MAX_VERSION_LENGTH = 80
MAX_OPERATOR_NOTE_LENGTH = 160


def _normalise_key(key: Any) -> str:
    """Normalize a JSON key for allowlist/blocklist checks."""
    return str(key).strip().lower().replace("-", "_").replace(" ", "_")


def _bounded_text(value: Any, default: str, max_length: int) -> str:
    """Return a stripped bounded text value."""
    if value is None:
        return default
    text = str(value).strip()
    if not text:
        return default
    return text[:max_length]


def _choice(value: Any, allowed: frozenset[str], default: str) -> str:
    """Normalize a bounded enum-like field."""
    text = _bounded_text(value, default, 64).lower().replace(" ", "_").replace("-", "_")
    return text if text in allowed else default


def _coerce_battery_level(value: Any) -> Optional[int]:
    """Coerce battery level to an integer percentage in [0, 100]."""
    if value is None or value == "":
        return None

    if isinstance(value, str):
        value = value.strip().rstrip("%")

    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None

    if numeric < 0 or numeric > 100:
        return None
    return int(round(numeric))


def blocked_phone_telemetry_fields(payload: Mapping[str, Any]) -> List[str]:
    """Return payload keys that look like disallowed private phone data."""
    blocked: List[str] = []
    for key in payload.keys():
        normalised = _normalise_key(key)
        if any(fragment in normalised for fragment in BLOCKED_PHONE_TELEMETRY_FRAGMENTS):
            blocked.append(str(key))
    return sorted(blocked)


def sanitize_phone_payload(payload: Mapping[str, Any]) -> Dict[str, Any]:
    """Validate and sanitize a coarse iPhone Shortcut telemetry payload.

    The input must be a mapping with only allowlisted keys. Any key that looks
    like location, health, messages, audio/video, contacts, or other private
    phone data is rejected even if the value is blank.
    """
    if not isinstance(payload, Mapping):
        raise ValueError("phone telemetry payload must be a JSON object")

    blocked = blocked_phone_telemetry_fields(payload)
    if blocked:
        raise ValueError("blocked_phone_telemetry_fields: " + ", ".join(blocked))

    normalised_keys = {_normalise_key(key) for key in payload.keys()}
    unsupported = sorted(normalised_keys - ALLOWED_PHONE_TELEMETRY_FIELDS)
    if unsupported:
        raise ValueError("unsupported_phone_telemetry_fields: " + ", ".join(unsupported))

    by_key = {_normalise_key(key): value for key, value in payload.items()}
    battery_level = _coerce_battery_level(by_key.get("battery_level"))

    return {
        "device_id": _bounded_text(
            by_key.get("device_id"),
            "unknown_phone_device",
            MAX_DEVICE_ID_LENGTH,
        ),
        "battery_level": battery_level,
        "battery_state": _choice(
            by_key.get("battery_state"),
            ALLOWED_BATTERY_STATES,
            "unknown",
        ),
        "manual_mode": _choice(
            by_key.get("manual_mode"),
            ALLOWED_MANUAL_MODES,
            "unknown",
        ),
        "shortcut_version": _bounded_text(
            by_key.get("shortcut_version"),
            "unknown",
            MAX_VERSION_LENGTH,
        ),
        "operator_note": _bounded_text(
            by_key.get("operator_note"),
            "",
            MAX_OPERATOR_NOTE_LENGTH,
        ),
        "client_recorded_at": _bounded_text(
            by_key.get("recorded_at"),
            "unknown",
            64,
        ),
    }


class PhoneShortcutSensor(Sensor):
    """A bounded sensor adapter for operator-approved iPhone Shortcut data.

    This sensor observes only the latest explicitly supplied payload or an
    injected payload provider. It does not access the phone directly.
    """

    def __init__(
        self,
        sensor_id: str = "alex-iphone-shortcut",
        scope: str = "operator:alex:iphone",
        payload_provider: Optional[Callable[[], Mapping[str, Any]]] = None,
    ):
        super().__init__(
            sensor_id=sensor_id,
            domain="personal_device_telemetry",
            scope=scope,
        )
        self._payload_provider = payload_provider
        self._latest_payload: Optional[Mapping[str, Any]] = None

    def update_payload(self, payload: Mapping[str, Any]) -> Dict[str, Any]:
        """Store a sanitized latest payload and return the sanitized copy."""
        sanitized = sanitize_phone_payload(payload)
        self._latest_payload = sanitized
        return sanitized

    def observe(self) -> List[Measurement]:
        """Return one Measurement for the current phone payload, if available."""
        try:
            payload = self._payload_provider() if self._payload_provider else self._latest_payload
            if payload is None:
                self._last_error = "no_phone_payload_available"
                return []

            sanitized = sanitize_phone_payload(payload)
            now = datetime.now(timezone.utc)
            measurement = Measurement(
                value=sanitized,
                uncertainty=0.35,
                confidence_interval=(0.0, 1.0),
                sample_size=1,
                confounders=[
                    "operator_controlled_shortcut",
                    "manual_mode_self_reported",
                    "phone_shortcut_may_fail_or_be_stale",
                ],
                missing=[
                    "no_precise_location",
                    "no_health_data",
                    "no_contacts",
                    "no_messages",
                    "no_audio",
                    "no_camera",
                    "no_notification_content",
                ],
                source="iphone_shortcuts",
                methodology="operator_initiated_phone_heartbeat",
                temporal_range=("instant", "instant"),
                scope=self.scope,
                recorded_at=now,
            )
            self._last_observation = now
            self._observation_count += 1
            self._last_error = None
            return [measurement]
        except Exception as exc:
            self._error_count += 1
            self._last_error = str(exc)
            return []
