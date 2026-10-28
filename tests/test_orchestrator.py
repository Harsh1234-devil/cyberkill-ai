"""Unit tests for Orchestrator and Reporting."""

import asyncio
import unittest
from cyberkill.core.orchestrator import global_orchestrator
from cyberkill.reporting.generator import ReportGenerator

class TestOrchestrator(unittest.TestCase):
    def test_full_chain_execution(self):
        result = asyncio.run(global_orchestrator.execute_full_chain("localhost", "quick"))
        self.assertEqual(result["status"], "COMPLETED")
        self.assertIn("reconnaissance", result["stages"])
        self.assertIn("exploitation", result["stages"])
        self.assertIn("purple_defense", result["stages"])

    def test_report_generation(self):
        result = asyncio.run(global_orchestrator.execute_full_chain("localhost", "quick"))
        report_md = ReportGenerator.generate_markdown(result, author="Harsh Vardhan")
        self.assertIn("Cyberkill.ai Security Assessment Report", report_md)
        self.assertIn("Harsh Vardhan", report_md)
        self.assertIn("Purple Team", report_md)

if __name__ == "__main__":
    unittest.main()
