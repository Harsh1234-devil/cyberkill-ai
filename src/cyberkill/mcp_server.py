"""FastMCP 2.0 Server for Cyberkill.ai."""

import asyncio
import json
import sys
from typing import Any, Dict

from cyberkill.config import settings
from cyberkill.core.orchestrator import global_orchestrator
from cyberkill.core.scope_guard import default_scope_guard
from cyberkill.reporting.generator import ReportGenerator
from cyberkill.tools.registry import global_tool_registry

class CyberkillMCPServer:
    def __init__(self):
        self.tools = {
            "cyberkill_scan": {
                "name": "cyberkill_scan",
                "description": "Execute autonomous multi-agent security evaluation across the Cyber Kill Chain.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target": {"type": "string", "description": "Target hostname, IP, or URL"},
                        "mode": {"type": "string", "enum": ["quick", "standard", "aggressive"], "default": "standard"}
                    },
                    "required": ["target"]
                }
            },
            "cyberkill_validate_scope": {
                "name": "cyberkill_validate_scope",
                "description": "Verify whether a target host or IP is within legally authorized scope.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target": {"type": "string", "description": "Target hostname or IP"}
                    },
                    "required": ["target"]
                }
            },
            "cyberkill_list_tools": {
                "name": "cyberkill_list_tools",
                "description": "List all registered cybersecurity tools categorized by Kill Chain stage.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "stage": {"type": "string", "description": "Optional stage filter (e.g. reconnaissance, exploitation)"}
                    }
                }
            },
            "cyberkill_generate_report": {
                "name": "cyberkill_generate_report",
                "description": "Generate comprehensive executive security assessment report in Markdown.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "target": {"type": "string", "description": "Target evaluated"}
                    },
                    "required": ["target"]
                }
            }
        }

    async def handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> Any:
        if name == "cyberkill_validate_scope":
            target = arguments.get("target", "")
            allowed, reason = default_scope_guard.validate_target(target)
            return {"target": target, "authorized": allowed, "reason": reason}

        elif name == "cyberkill_scan":
            target = arguments.get("target", "")
            mode = arguments.get("mode", "standard")
            allowed, reason = default_scope_guard.validate_target(target)
            if not allowed:
                return {"error": f"Target outside authorized scope: {reason}"}
            result = await global_orchestrator.execute_full_chain(target, mode)
            return result

        elif name == "cyberkill_list_tools":
            stage = arguments.get("stage")
            if stage:
                tools = global_tool_registry.list_by_stage(stage)
            else:
                tools = list(global_tool_registry.tools.values())
            return {"count": len(tools), "tools": [t.dict() for t in tools]}

        elif name == "cyberkill_generate_report":
            target = arguments.get("target", "")
            scan_res = await global_orchestrator.execute_full_chain(target, "standard")
            report = ReportGenerator.generate_markdown(scan_res, author=settings.author)
            return {"markdown": report}

        else:
            return {"error": f"Unknown tool: {name}"}

    async def run_stdio(self):
        loop = asyncio.get_event_loop()
        reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        while True:
            line = await reader.readline()
            if not line:
                break
            try:
                req = json.loads(line.decode("utf-8").strip())
                req_id = req.get("id")
                method = req.get("method")

                if method == "tools/list":
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"tools": list(self.tools.values())}
                    }
                elif method == "tools/call":
                    params = req.get("params", {})
                    tool_name = params.get("name")
                    args = params.get("arguments", {})
                    result = await self.handle_tool_call(tool_name, args)
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                        }
                    }
                else:
                    resp = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {}
                    }

                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
            except Exception as e:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32603, "message": str(e)}
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()

if __name__ == "__main__":
    server = CyberkillMCPServer()
    asyncio.run(server.run_stdio())
