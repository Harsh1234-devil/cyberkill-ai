"""StateGraph Orchestrator: Chains multi-agent workflows across the Cyber Kill Chain."""

import asyncio
from typing import Any, Dict
from cyberkill.agents.recon import ReconAgent
from cyberkill.agents.exploitation import ExploitationAgent
from cyberkill.agents.purple_defense import PurpleDefenseAgent
from cyberkill.core.telemetry import global_telemetry

class KillChainOrchestrator:
    def __init__(self):
        self.recon_agent = ReconAgent()
        self.exploit_agent = ExploitationAgent()
        self.defense_agent = PurpleDefenseAgent()

    async def execute_full_chain(self, target: str, scan_mode: str = "standard") -> Dict[str, Any]:
        global_telemetry.record_scan()

        recon_data = await self.recon_agent.run(target, {"mode": scan_mode})
        exploit_data = await self.exploit_agent.run(target)
        defense_data = await self.defense_agent.run(target, {"findings": exploit_data.get("vulnerabilities", [])})

        return {
            "target": target,
            "scan_mode": scan_mode,
            "stages": {
                "reconnaissance": recon_data,
                "exploitation": exploit_data,
                "purple_defense": defense_data
            },
            "status": "COMPLETED",
            "executive_summary": f"Autonomous assessment completed for {target}. Discovered {len(exploit_data.get('vulnerabilities', []))} findings with automated detection rules generated."
        }

global_orchestrator = KillChainOrchestrator()
