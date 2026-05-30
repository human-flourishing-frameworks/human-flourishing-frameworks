"""Guard the public Lantern AWS URL bridge.

This repo should link the Lantern AWS migration without claiming that a public
AWS service URL is already verified.
"""

import unittest

import safe_app


class LanternAwsBridgeTests(unittest.TestCase):
    def setUp(self):
        self.client = safe_app.app.test_client()

    def test_lantern_aws_bridge_api_is_truth_bounded(self):
        response = self.client.get("/api/lantern/aws-bridge")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "aws_public_url_pending_operator_deploy")
        self.assertEqual(data["localPrimary"], "http://127.0.0.1:4177/")
        self.assertEqual(data["localHealth"], "http://127.0.0.1:4177/api/health")
        self.assertIn("LANTERN-RUNTIME-CICD.md", data["runtimeContract"])
        self.assertIn("pending operator deploy", data["awsServiceRoot"])
        self.assertIn("https://lantern-os.onrender.com", data["retiredLanternMirrors"])

    def test_lantern_aws_bridge_page_links_sources_and_validation_urls(self):
        response = self.client.get("/lantern/aws")
        self.assertEqual(response.status_code, 200)
        text = response.get_data(as_text=True)
        self.assertIn("Lantern AWS URL Bridge", text)
        self.assertIn("http://127.0.0.1:4177/api/cloud-mirrors", text)
        self.assertIn("https://github.com/alex-place/lantern-os/blob/master/apps/lantern-garage/Dockerfile", text)
        self.assertIn("pending operator deploy", text)
        self.assertIn("not Lantern Cloud OS proof", text)


if __name__ == "__main__":
    unittest.main()
