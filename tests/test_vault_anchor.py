#!/usr/bin/env python3
"""Tests for vault key hardening + external time-anchoring (lantern-os#1740)."""
import json
import os
import tempfile
import unittest
from pathlib import Path

import cryptographic_proof as cp
import vault_anchor as va


class KeyEncryptionAtRestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.priv = os.path.join(self.tmp.name, "node.key")
        self.pub = os.path.join(self.tmp.name, "node.pub")
        os.environ.pop(cp._KEY_PASSPHRASE_ENV, None)

    def tearDown(self):
        os.environ.pop(cp._KEY_PASSPHRASE_ENV, None)
        self.tmp.cleanup()

    def test_passphrase_arg_roundtrip(self):
        priv, pub = cp.generate_keypair()
        cp.save_keypair(priv, pub, self.priv, self.pub, passphrase="s3cr3t")
        # encrypted on disk → cannot load without the passphrase
        with self.assertRaises((ValueError, TypeError)):
            cp.load_keypair(self.priv, self.pub)
        with self.assertRaises((ValueError, TypeError)):
            cp.load_keypair(self.priv, self.pub, passphrase="wrong")
        # correct passphrase round-trips and still signs/verifies
        lpriv, lpub = cp.load_keypair(self.priv, self.pub, passphrase="s3cr3t")
        signed = cp.sign_record({"x": 1}, lpriv)
        self.assertTrue(cp.verify_record(signed, lpub))

    def test_env_passphrase_used_when_no_arg(self):
        os.environ[cp._KEY_PASSPHRASE_ENV] = "envpass"
        priv, pub = cp.generate_keypair()
        cp.save_keypair(priv, pub, self.priv, self.pub)  # no arg → env encrypts
        os.environ.pop(cp._KEY_PASSPHRASE_ENV, None)
        with self.assertRaises((ValueError, TypeError)):
            cp.load_keypair(self.priv, self.pub)  # env cleared → can't decrypt
        os.environ[cp._KEY_PASSPHRASE_ENV] = "envpass"
        lpriv, lpub = cp.load_keypair(self.priv, self.pub)
        self.assertTrue(cp.verify_record(cp.sign_record({"y": 2}, lpriv), lpub))

    def test_unencrypted_backward_compat(self):
        priv, pub = cp.generate_keypair()
        cp.save_keypair(priv, pub, self.priv, self.pub)  # no passphrase, no env
        lpriv, lpub = cp.load_keypair(self.priv, self.pub)  # loads without password
        self.assertTrue(cp.verify_record(cp.sign_record({"z": 3}, lpriv), lpub))
        # the on-disk key is genuinely unencrypted (the documented default)
        self.assertIn("PRIVATE KEY", Path(self.priv).read_text())


class TransparencyLogTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log_path = os.path.join(self.tmp.name, "tlog.jsonl")

    def tearDown(self):
        self.tmp.cleanup()

    def test_append_and_verify_chain(self):
        log = va.TransparencyLog(self.log_path)
        log.append("a" * 64, 3, ts="2026-06-30T00:00:00+00:00")
        log.append("b" * 64, 5, ts="2026-06-30T01:00:00+00:00")
        ok, n = log.verify_chain()
        self.assertTrue(ok)
        self.assertEqual(n, 2)

    def test_tamper_is_detected(self):
        log = va.TransparencyLog(self.log_path)
        log.append("a" * 64, 3, ts="2026-06-30T00:00:00+00:00")
        log.append("b" * 64, 5, ts="2026-06-30T01:00:00+00:00")
        # edit the second entry's count after the fact
        lines = Path(self.log_path).read_text().splitlines()
        e = json.loads(lines[1])
        e["count"] = 999
        lines[1] = json.dumps(e)
        Path(self.log_path).write_text("\n".join(lines) + "\n")
        ok, idx = log.verify_chain()
        self.assertFalse(ok)
        self.assertEqual(idx, 1)


class AnchorExistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = va.TransparencyLog(os.path.join(self.tmp.name, "tlog.jsonl"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_anchor_then_prove_inclusion_and_existence(self):
        recs = [{"event": "memory", "i": i} for i in range(5)]
        anchor = va.anchor_records(recs, log=self.log, ts="2026-06-30T00:00:00+00:00")
        self.assertEqual(anchor.count, 5)
        ok, _ = self.log.verify_chain()
        self.assertTrue(ok)
        res = va.verify_existence(recs[2], recs, self.log)
        self.assertTrue(res["included"])
        self.assertTrue(res["published"])
        self.assertEqual(res["existed_by"], "2026-06-30T00:00:00+00:00")
        self.assertEqual(res["root"], anchor.root)

    def test_foreign_record_not_included(self):
        recs = [{"event": "memory", "i": i} for i in range(5)]
        va.anchor_records(recs, log=self.log, ts="2026-06-30T00:00:00+00:00")
        res = va.verify_existence({"event": "memory", "i": 99}, recs, self.log)
        self.assertFalse(res["included"])

    def test_rfc3161_skips_without_tsa_or_lib(self):
        # no TSA configured → skipped, never raises
        r1 = va.rfc3161_timestamp("ab" * 32)
        self.assertEqual(r1["status"], "skipped")
        # TSA set but rfc3161ng absent in this env → skipped with install hint
        r2 = va.rfc3161_timestamp("ab" * 32, tsa_url="http://tsa.example/tsr")
        self.assertEqual(r2["status"], "skipped")


if __name__ == "__main__":
    unittest.main()
