"""Unit tests for Tools Registry."""

import unittest
from cyberkill.tools.registry import global_tool_registry

class TestToolRegistry(unittest.TestCase):
    def test_tools_registered_count(self):
        self.assertGreaterEqual(global_tool_registry.count(), 20)

    def test_nmap_lookup(self):
        tool = global_tool_registry.get("nmap")
        self.assertIsNotNone(tool)
        self.assertEqual(tool.category, "network")
        self.assertEqual(tool.stage, "reconnaissance")

    def test_nuclei_lookup(self):
        tool = global_tool_registry.get("nuclei")
        self.assertIsNotNone(tool)
        self.assertEqual(tool.stage, "exploitation")

    def test_stage_filtering(self):
        recon_tools = global_tool_registry.list_by_stage("reconnaissance")
        self.assertGreater(len(recon_tools), 0)

if __name__ == "__main__":
    unittest.main()
