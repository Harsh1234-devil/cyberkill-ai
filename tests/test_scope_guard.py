"""Unit tests for ScopeGuard authorization engine."""

import unittest
from cyberkill.core.scope_guard import ScopeGuard

class TestScopeGuard(unittest.TestCase):
    def setUp(self):
        self.guard = ScopeGuard(
            allowed_domains=["target.corp", "*.lab.internal", "localhost"],
            allowed_cidrs=["192.168.1.0/24", "127.0.0.1/32"],
            disallowed_domains=["*.gov", "*.mil", "google.com"]
        )

    def test_authorized_domain(self):
        allowed, msg = self.guard.validate_target("target.corp")
        self.assertTrue(allowed)
        self.assertIn("authorized", msg)

    def test_wildcard_subdomain(self):
        allowed, msg = self.guard.validate_target("app.lab.internal")
        self.assertTrue(allowed)

    def test_disallowed_gov_domain(self):
        allowed, msg = self.guard.validate_target("fbi.gov")
        self.assertFalse(allowed)
        self.assertIn("forbidden", msg)

    def test_authorized_cidr_ip(self):
        allowed, msg = self.guard.validate_target("192.168.1.50")
        self.assertTrue(allowed)

    def test_unauthorized_ip(self):
        allowed, msg = self.guard.validate_target("8.8.8.8")
        self.assertFalse(allowed)

if __name__ == "__main__":
    unittest.main()
