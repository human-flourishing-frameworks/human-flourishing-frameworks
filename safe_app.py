"""Safe public WSGI entrypoint for Human Flourishing Frameworks.

This module imports the existing Flask app and sanitizes known misleading or
incomplete public dashboard markup before the app is served. It does not change
endpoints, auth, agents, sensors, mesh sync, secrets, databases, or deployment
settings beyond the deployment choosing this entrypoint.

The underlying app.py template should still be corrected directly in follow-up
work. This file is a public-copy and presentation guard for the live service.
"""

from __future__ import annotations

import app as _app_module


_ADVISORY_BANNER = (
    "<strong>EXPERIMENTAL ADVISORY AGENTS</strong> &mdash; Research/demo agents\n"
    "                expose advisory workflow status and audit records. They are not a\n"
    "                human board, regulator, court, enforcement system, or autonomous authority.\n"
    "                Escalations are review records only unless explicitly authorized by an operator."
)

_SKIP_LINK_CSS = """
        .skip-link {
            position: absolute;
            left: 12px;
            top: -48px;
            background: #ffffff;
            color: #111111;
            padding: 10px 14px;
            border-radius: 6px;
            z-index: 1000;
        }
        .skip-link:focus { top: 12px; }
"""

_HEALTHZ_SENSOR_STATUS_JS = """
        // Public runtime sensor state comes from /healthz, not from the
        // world-model registry count. This keeps sensor definitions separate
        // from live observation.
        fetch('/healthz')
            .then(r => r.json())
            .then(data => {
                const el = document.getElementById('wm-live-sensors-header');
                if (!el) return;
                el.textContent = data.live_sensors_enabled ? 'enabled' : 'disabled';
            })
            .catch(() => {
                const el = document.getElementById('wm-live-sensors-header');
                if (el) el.textContent = 'check /healthz';
            });
"""

_PUBLIC_COPY_REPLACEMENTS = (
    (
        "<!-- AUTONOMOUS GOVERNANCE (collapsed by default) -->",
        "<!-- ADVISORY AGENT STATUS (collapsed by default) -->",
    ),
    ("Autonomous Governance", "Advisory Agent Status"),
    (
        "<strong>ALGORITHMIC GOVERNANCE</strong> &mdash; 7 autonomous agents\n"
        "                coordinate through PBFT consensus. No human board. Escalations are\n"
        "                irreversible after a 24-hour lock.",
        _ADVISORY_BANNER,
    ),
    ("<strong>ALGORITHMIC GOVERNANCE</strong>", "<strong>EXPERIMENTAL ADVISORY AGENTS</strong>"),
    ("No human board.", "Operator review required."),
    (
        "Escalations are irreversible after a 24-hour lock.",
        "Escalations are review records only unless explicitly authorized by an operator.",
    ),
    (
        "irreversible after a 24-hour lock.",
        "not executable unless explicitly authorized by an operator.",
    ),
    (
        '&mdash; <span id="wm-sensor-count-header">0</span> registered sensors',
        '&mdash; live sensors: <span id="wm-live-sensors-header">checking</span>',
    ),
    (
        "document.getElementById('wm-sensor-count-header').textContent = data.sensor_count || 0;",
        "// Live sensor header is populated from /healthz below.",
    ),
    ('<div class="stat-label">Registered Sensors</div>', '<div class="stat-label">Runtime Sensor Sources</div>'),
    (
        "sensors registered. Waiting for first observation cycle...",
        "sensor definitions available. Live observation remains disabled unless explicitly enabled.",
    ),
)


def _rewrite_public_html(template: str) -> str:
    """Apply public-copy convergence to a rendered or template HTML string."""
    for old, new in _PUBLIC_COPY_REPLACEMENTS:
        template = template.replace(old, new)

    template = template.replace("<html>", '<html lang="en" dir="ltr">', 1)

    if ".skip-link" not in template:
        template = template.replace("    </style>", _SKIP_LINK_CSS + "    </style>", 1)

    if 'href="#main-content"' not in template:
        template = template.replace(
            '<body>\n    <div class="container">',
            '<body>\n    <a class="skip-link" href="#main-content">Skip to main content</a>\n    <main id="main-content" class="container">',
            1,
        )
        template = template.replace(
            "        </footer>\n    </div>\n\n    <script>",
            "        </footer>\n    </main>\n\n    <script>",
            1,
        )

    if (
        "wm-live-sensors-header" in template
        and "/healthz" in template
        and "Public runtime sensor state comes from /healthz" not in template
    ):
        template = template.replace(
            "        // ---- WORLD MODEL STATUS ----",
            _HEALTHZ_SENSOR_STATUS_JS + "\n        // ---- WORLD MODEL STATUS ----",
            1,
        )

    return template


def _sanitize_public_template() -> None:
    """Replace misleading public copy in the module-level template."""
    template = getattr(_app_module, "HTML_TEMPLATE", "")
    if isinstance(template, str):
        _app_module.HTML_TEMPLATE = _rewrite_public_html(template)


def _apply_public_ui_baseline() -> None:
    """Kept for compatibility with older tests/imports; handled by rewrite."""
    _sanitize_public_template()


def _clarify_public_sensor_status() -> None:
    """Kept for compatibility with older tests/imports; handled by rewrite."""
    _sanitize_public_template()


_sanitize_public_template()

app = _app_module.app


@app.after_request
def _enforce_safe_public_response(response):
    """Prevent stale public dashboard copy from surviving template drift or cache.

    This response-level guard is intentionally presentation-only. It does not add
    routes, writes, sensors, mesh sync, agents, secrets, databases, or deployment
    authority. It gives the public HTML the same claim/guard language even if the
    imported template changes before app.py is corrected directly.
    """
    response.headers["Cache-Control"] = "no-store, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    content_type = response.headers.get("Content-Type", "")
    if response.direct_passthrough or "text/html" not in content_type.lower():
        return response

    try:
        html = response.get_data(as_text=True)
        rewritten = _rewrite_public_html(html)
        if rewritten != html:
            response.set_data(rewritten)
            response.headers["Content-Length"] = str(len(response.get_data()))
    except Exception:
        return response

    return response


if __name__ == "__main__":
    app.run()
