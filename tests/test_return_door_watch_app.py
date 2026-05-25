#!/usr/bin/env python3
"""Guardrails for the static Return Door Watch prototype."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "return-door-watch" / "index.html"


class ReturnDoorWatchAppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = APP.read_text(encoding="utf-8")
        cls.lower = cls.text.lower()

    def test_static_watch_exists_and_names_return_door(self):
        for phrase in [
            "return door watch",
            "small outside, bigger inside",
            "door visible",
            "back door closed",
            "visible return door",
            "validation pulse",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_modes_are_bounded_and_local(self):
        for phrase in [
            "home: show state, limit, test, and return",
            "fold: compress anchors",
            "stop: close loops",
            "leave no hidden process",
            "static local prototype only",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_back_door_is_closed(self):
        for phrase in [
            "no time travel",
            "no hidden agents",
            "no sensors",
            "no private contact",
            "back door closed",
        ]:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.lower)

    def test_no_network_sensor_or_storage_calls(self):
        blocked = [
            "fetch(",
            "xmlhttprequest",
            "websocket",
            "eventsource",
            "navigator.geolocation",
            "getusermedia",
            "localstorage",
            "sessionstorage",
            "http://",
            "https://",
        ]
        for phrase in blocked:
            with self.subTest(phrase=phrase):
                self.assertNotIn(phrase, self.lower)

    def test_not_a_copied_show_prop_or_literal_claim(self):
        for blocked in [
            "police box",
            "official tardis",
            "doctor who",
            "time lord",
            "sonic screwdriver",
        ]:
            with self.subTest(blocked=blocked):
                self.assertNotIn(blocked, self.lower)


if __name__ == "__main__":
    unittest.main()
