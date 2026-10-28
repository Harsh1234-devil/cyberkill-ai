"""Audit trails, real-time metrics, and telemetry tracker."""

import time
from typing import Dict, Any

class TelemetryTracker:
    def __init__(self):
        self.start_time = time.time()
        self.total_scans_requested = 0
        self.total_tools_executed = 0
        self.total_vulnerabilities_found = 0
        self.severities = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}

    def record_scan(self):
        self.total_scans_requested += 1

    def record_tool_run(self):
        self.total_tools_executed += 1

    def record_vulnerability(self, severity: str = "info"):
        sev = severity.lower()
        if sev in self.severities:
            self.severities[sev] += 1
        self.total_vulnerabilities_found += 1

    def get_metrics(self) -> Dict[str, Any]:
        uptime = round(time.time() - self.start_time, 2)
        return {
            "uptime_seconds": uptime,
            "total_scans_requested": self.total_scans_requested,
            "total_tools_executed": self.total_tools_executed,
            "total_vulnerabilities_found": self.total_vulnerabilities_found,
            "severity_breakdown": self.severities
        }

global_telemetry = TelemetryTracker()
