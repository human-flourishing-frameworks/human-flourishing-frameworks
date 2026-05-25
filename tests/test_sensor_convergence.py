"""Regression tests for HFF sensor convergence boundaries.

These tests keep sensor terminology aligned with the public-surface policy:
sensor definitions are not live observation, and live observation is not personal
monitoring or device enrollment.
"""

import unittest

import app as hff_app
import live_sensors


class SensorConvergenceTests(unittest.TestCase):
    def test_live_sensors_default_disabled(self):
        self.assertFalse(hff_app.ENABLE_LIVE_SENSORS)
        self.assertFalse(hff_app.ENABLE_MESH_SYNC)
        self.assertFalse(hff_app.ALLOW_PUBLIC_WRITES)

    def test_current_sensor_definitions_are_public_aggregate_only(self):
        sensors = live_sensors.create_live_sensors()
        sensor_ids = {sensor.sensor_id for sensor in sensors}
        self.assertEqual(
            sensor_ids,
            {
                "wb-life-expectancy",
                "wb-infant-mortality",
                "wb-maternal-mortality",
                "wb-gdp-per-capita",
                "wb-gini-index",
                "wb-adult-literacy",
                "wb-co2-per-capita",
                "wb-forest-area",
                "wb-protected-areas",
            },
        )
        self.assertTrue(all(sensor.sensor_id.startswith("wb-") for sensor in sensors))

    def test_runtime_defaults_block_sensitive_sensor_paths(self):
        self.assertFalse(hff_app.ENABLE_LIVE_SENSORS)
        self.assertFalse(hff_app.ENABLE_MESH_SYNC)
        self.assertFalse(hff_app.ALLOW_PUBLIC_WRITES)
        self.assertEqual(len(live_sensors.create_live_sensors()), 9)


if __name__ == "__main__":
    unittest.main()
