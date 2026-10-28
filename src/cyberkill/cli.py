"""Command Line Interface (CLI) for Cyberkill.ai."""

import asyncio
import click
import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cyberkill.__version__ import __version__, __author__
from cyberkill.config import settings
from cyberkill.core.orchestrator import global_orchestrator
from cyberkill.core.scope_guard import default_scope_guard
from cyberkill.reporting.generator import ReportGenerator
from cyberkill.tools.registry import global_tool_registry

console = Console()

BANNER = f"""
[bold red]  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗  ██╗██╗██╗     ██╗     [/bold red]
[bold red] ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██║██║     ██║     [/bold red]
[bold white] ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝█████╔╝ ██║██║     ██║     [/bold white]
[bold white] ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔═██╗ ██║██║     ██║     [/bold white]
[bold red] ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║  ██╗██║███████╗███████╗[/bold red]
[bold red]  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝[/bold red]
[bold yellow]   Autonomous Cybersecurity & MCP Platform v{__version__} | By {__author__}[/bold yellow]
"""

@click.group()
def main():
    """Cyberkill.ai - Next-Gen Multi-Agent Cybersecurity Platform."""
    pass

@main.command()
@click.option("--host", default="0.0.0.0", help="Binding host address.")
@click.option("--port", default=8888, type=int, help="Port to run server on.")
def server(host, port):
    """Launch the Cyberkill.ai REST & WebSocket API Server."""
    console.print(BANNER)
    console.print(f"[green]Starting Cyberkill.ai server on http://{host}:{port}[/green]")
    uvicorn.run("cyberkill.server:app", host=host, port=port, reload=False)

@main.command()
def mcp():
    """Launch Cyberkill.ai FastMCP server via Stdio (for Claude/Cursor)."""
    from cyberkill.mcp_server import CyberkillMCPServer
    server_inst = CyberkillMCPServer()
    asyncio.run(server_inst.run_stdio())

@main.command()
@click.argument("target")
@click.option("--mode", default="standard", type=click.Choice(["quick", "standard", "aggressive"]))
@click.option("--report", is_flag=True, help="Print full executive Markdown report.")
def scan(target, mode, report):
    """Run an autonomous assessment against a target."""
    console.print(BANNER)
    console.print(f"[bold cyan]Validating scope for target:[/bold cyan] {target}")
    allowed, reason = default_scope_guard.validate_target(target)
    if not allowed:
        console.print(f"[bold red]SCOPE VIOLATION:[/bold red] {reason}")
        return

    console.print(f"[green]Authorization verified:[/green] {reason}")
    console.print(f"[bold yellow]Executing Cyber Kill Chain assessment ({mode} mode)...[/bold yellow]")

    result = asyncio.run(global_orchestrator.execute_full_chain(target, mode))
    vulns = result["stages"]["exploitation"].get("vulnerabilities", [])

    table = Table(title="Assessment Results", border_style="red")
    table.add_column("Finding ID", style="cyan")
    table.add_column("Title", style="bold white")
    table.add_column("Severity", style="bold red")
    table.add_column("CVSS", style="yellow")
    table.add_column("MITRE ATT&CK", style="magenta")

    for v in vulns:
        table.add_row(v["id"], v["title"], v["severity"].upper(), str(v["cvss"]), v["mitre"])

    console.print(table)

    if report:
        rep_md = ReportGenerator.generate_markdown(result, author=__author__)
        console.print(Panel(rep_md, title="Executive Assessment Report", border_style="green"))

@main.command()
def tools():
    """Display registered security tools categorized by Kill Chain stage."""
    console.print(BANNER)
    stages = ["reconnaissance", "weaponization", "delivery", "exploitation", "installation", "actions"]
    for s in stages:
        stage_tools = global_tool_registry.list_by_stage(s)
        table = Table(title=f"Kill Chain Stage: {s.upper()} ({len(stage_tools)} tools)", border_style="blue")
        table.add_column("Tool", style="bold cyan")
        table.add_column("Category", style="green")
        table.add_column("Description", style="white")
        table.add_column("MITRE", style="yellow")
        for t in stage_tools:
            table.add_row(t.name, t.category, t.description, ", ".join(t.mitre_techniques))
        console.print(table)

if __name__ == "__main__":
    main()
