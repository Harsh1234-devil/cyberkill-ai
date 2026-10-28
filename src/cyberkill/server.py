"""FastAPI REST & WebSocket Server for Cyberkill.ai."""

import asyncio
from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

from cyberkill.config import settings
from cyberkill.core.cache import global_cache
from cyberkill.core.orchestrator import global_orchestrator
from cyberkill.core.process_manager import global_process_manager
from cyberkill.core.scope_guard import default_scope_guard
from cyberkill.core.telemetry import global_telemetry
from cyberkill.reporting.generator import ReportGenerator
from cyberkill.tools.registry import global_tool_registry

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Next-Generation Autonomous Multi-Agent Cybersecurity Platform & MCP Server by Harsh Vardhan"
)

class ScanRequest(BaseModel):
    target: str = Field(..., description="Target domain, IP, or URL")
    mode: str = Field("standard", description="Scan profile: quick, standard, aggressive")

class ScopeCheckRequest(BaseModel):
    target: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.version,
        "author": settings.author,
        "tools_registered": global_tool_registry.count(),
        "active_processes": len(global_process_manager.active_processes),
        "telemetry": global_telemetry.get_metrics()
    }

@app.get("/api/v1/tools")
async def list_tools(stage: Optional[str] = None, category: Optional[str] = None):
    if stage:
        tools = global_tool_registry.list_by_stage(stage)
    elif category:
        tools = global_tool_registry.list_by_category(category)
    else:
        tools = list(global_tool_registry.tools.values())
    return {
        "total": len(tools),
        "tools": [t.dict() for t in tools]
    }

@app.post("/api/v1/scope/validate")
async def validate_scope(req: ScopeCheckRequest):
    allowed, reason = default_scope_guard.validate_target(req.target)
    return {
        "target": req.target,
        "authorized": allowed,
        "reason": reason
    }

@app.post("/api/v1/scan")
async def start_scan(req: ScanRequest):
    allowed, reason = default_scope_guard.validate_target(req.target)
    if not allowed:
        raise HTTPException(status_code=403, detail=f"Target unauthorized: {reason}")

    cache_key = f"scan:{req.target}:{req.mode}"
    cached = global_cache.get(cache_key)
    if cached:
        return {"cached": True, "data": cached}

    result = await global_orchestrator.execute_full_chain(req.target, req.mode)
    global_cache.set(cache_key, result)
    return {"cached": False, "data": result}

@app.post("/api/v1/reports/generate")
async def generate_report(req: ScanRequest):
    scan_res = await global_orchestrator.execute_full_chain(req.target, req.mode)
    report_md = ReportGenerator.generate_markdown(scan_res, author=settings.author)
    return {
        "target": req.target,
        "markdown_report": report_md
    }

@app.get("/api/v1/telemetry")
async def get_telemetry():
    return {
        "telemetry": global_telemetry.get_metrics(),
        "cache": global_cache.stats()
    }
