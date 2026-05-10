"""Tests for the safe public UI baseline.

These checks keep the public dashboard readable and assistive-technology
friendly without adding new runtime capability.
"""

import unittest

import safe_app


class PublicUiBaselineTests(unittest.TestCase):
    def setUp(self):
        self.client = safe_app.app.test_client()

    def test_public_html_declares_current_language_and_direction(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('<html lang="en" dir="ltr">', text)

    def test_public_html_has_skip_link_and_main_landmark(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('href="#main-content"', text)
        self.assertIn('id="main-content"', text)
        self.assertIn('<main ', text)
        self.assertIn('</main>', text)

    def test_public_html_preserves_advisory_boundary(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn("Research Software", text)
        self.assertIn(
            "not a human board, regulator, court, enforcement system, or autonomous authority",
            text,
        )
        self.assertNotIn("ALGORITHMIC GOVERNANCE", text)
        self.assertNotIn("irreversible after a 24-hour lock", text)

    def test_public_sensor_copy_separates_live_state_from_definitions(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn('live sensors: <span id="wm-live-sensors-header">checking</span>', text)
        self.assertIn("Public runtime sensor state comes from /healthz", text)
        self.assertIn("Runtime Sensor Sources", text)
        self.assertIn(
            "sensor definitions available. Live observation remains disabled unless explicitly enabled.",
            text,
        )
        self.assertNotIn('id="wm-sensor-count-header"', text)
        self.assertNotIn("sensors registered. Waiting for first observation cycle", text)

    def test_public_dashboard_is_not_cached(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("no-store", response.headers.get("Cache-Control", ""))
        self.assertEqual(response.headers.get("Pragma"), "no-cache")
        self.assertEqual(response.headers.get("Expires"), "0")


if __name__ == "__main__":
    unittest.main()
