# 🛡️ Cyberkill.ai

<div align="center">

```
  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗  ██╗██╗██╗     ██╗     
 ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║ ██╔╝██║██║     ██║     
 ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝█████╔╝ ██║██║     ██║     
 ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔═██╗ ██║██║     ██║     
 ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║  ██╗██║███████╗███████╗
  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝
```

### Next-Generation Autonomous Multi-Agent Cybersecurity Platform & FastMCP Server

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![MCP](https://img.shields.io/badge/MCP-Protocol_2.0-8A2BE2)](https://modelcontextprotocol.io)
[![MITRE ATT&CK](https://img.shields.io/badge/MITRE-ATT%26CK_v15-red)](https://attack.mitre.org)
[![Architecture](https://img.shields.io/badge/Kill_Chain-Lockheed_Martin-green)](https://www.lockheedmartin.com/en-us/capabilities/cyber/cyber-kill-chain.html)
[![Author](https://img.shields.io/badge/Architect-Harsh_Vardhan-orange)](#author)

</div>

---

## ⚡ Executive Summary

**Cyberkill.ai** is an enterprise-grade autonomous cybersecurity automation platform and Model Context Protocol (MCP) server engineered by **Harsh Vardhan**. 

Designed as a superior evolution beyond legacy tool wrappers (such as HexStrike), Cyberkill.ai organizes **180+ professional security tools** into an autonomous, state-driven multi-agent framework strictly aligned with the **Lockheed Martin Cyber Kill Chain®** and **MITRE ATT&CK® v15**.

Crucially, Cyberkill.ai bridges the gap between offensive auditing and defensive resilience through **Automated Purple Teaming**: for every attack vector or vulnerability uncovered, the platform synthesizes production-ready **Sigma detection rules**, **Snort / Suricata signatures**, and **remediation patch snippets**.

---

## 🚀 Key Advantages Over HexStrike.ai

| Feature Category | HexStrike AI (Legacy) | Cyberkill.ai (Next-Gen) |
|---|---|---|
| **Architectural Model** | Monolithic script wrappers | Modular async Python package (`src/cyberkill`) |
| **Framework Alignment** | Ad-hoc tool execution | Structured **Lockheed Martin Cyber Kill Chain® (7 Stages)** |
| **Purple Teaming** | Offensive-only | Automated **Blue Team Defenses, Sigma & Snort Signatures** |
| **Legal Scope Enforcement** | None (Risk of out-of-scope probes) | **ScopeGuard Engine**: CIDR & domain regex authorization |
| **Process Management** | Synchronous blocking calls | **Asyncio ProcessManager** with live stream capture & kill switches |
| **Caching Engine** | Basic dictionary storage | **LRU Cache with TTL** and hit-ratio telemetry |
| **Protocol Support** | Basic FastMCP stdio | **FastMCP 2.0** with typed Pydantic V2 schemas & SSE transport |
| **Reporting Suite** | Raw terminal output | Executive **Markdown, JSON, & CVSS v4 Scored Audit Deliverables** |
| **Deployment** | Manual script execution | **Docker, Docker-Compose, & GitHub Actions CI/CD** |

---

## 🏗️ Architecture & Cyber Kill Chain Alignment

Cyberkill.ai coordinates specialized AI agents across all 7 stages of the Cyber Kill Chain:

```
[Target] ──► [ScopeGuard Validation]
                    │
                    ▼
Stage 1: Reconnaissance ──────► Nmap, Rustscan, Amass, Subfinder, HTTPx, Katana
                    │
Stage 2: Weaponization ───────► Searchsploit, CVE-Bin-Tool, MSFVenom, TruffleHog
                    │
Stage 3: Delivery ────────────► Gobuster, FFuf, Feroxbuster, Arjun, ParamSpider
                    │
Stage 4: Exploitation ────────► Nuclei, SQLMap, Dalfox, Nikto, WPScan, Hydra
                    │
Stage 5: Installation ────────► Trivy, Prowler, Kube-bench, Checkov, ScoutSuite
                    │
Stage 6: Command & Control ───► TShark, Zeek, Snort Inspection
                    │
Stage 7: Actions on Objectives► Radare2, Checksec, Binwalk, Volatility3, ExifTool
                    │
                    ▼
Purple Team Defense Engine ───► Sigma Rules, Snort Signatures, Remediation Guides
                    │
                    ▼
Executive Audit Deliverable ──► Markdown, JSON & Executive Reports
```

---

## 📦 Quick Start Installation

### Prerequisites
- Linux (Kali Linux, Ubuntu, Debian recommended) or macOS
- Python 3.9+
- Docker (optional)

### 1. Clone Repository & Setup
```bash
git clone https://github.com/harshvardhan/cyberkill-ai.git
cd cyberkill-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### 2. Verify Installation
```bash
# Check registered tools
cyberkill tools

# Test ScopeGuard validation
cyberkill scan localhost --mode quick --report
```

---

## 🤖 MCP Integration (Claude Desktop & Cursor)

Cyberkill.ai integrates directly into Claude Desktop, Cursor, and Copilot as an MCP tool provider.

### Claude Desktop Configuration
Add the configuration to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "cyberkill-ai": {
      "command": "python3",
      "args": [
        "-m",
        "cyberkill.mcp_server"
      ],
      "env": {
        "PYTHONPATH": "/path/to/cyberkill-ai/src"
      },
      "description": "Cyberkill.ai v1.0.0 by Harsh Vardhan",
      "timeout": 300,
      "disabled": false
    }
  }
}
```

Now you can prompt Claude:
> *"Run an autonomous Cyber Kill Chain assessment against my test lab at target.corp and generate Sigma detection rules for discovered vulnerabilities."*

---

## 🐳 Docker Deployment

Run Cyberkill.ai in a fully isolated container environment:
```bash
cd docker
docker compose up -d

# Verify server health
curl http://localhost:8888/health
```

---

## 🛠️ CLI Reference

```bash
# Start FastAPI REST & WebSocket server
cyberkill server --port 8888

# Launch Stdio MCP server
cyberkill mcp

# Execute an autonomous scan
cyberkill scan target.lab --mode standard --report

# List 180+ tools categorized by Kill Chain stage
cyberkill tools
```

---

## 👤 Author

**Harsh Vardhan**  
- Cybersecurity Architect & Ethical Hacker (CEH & CISSP Preparation Track)  
- Artificial Intelligence & Prompt Engineer  
- Founder / Lead Developer of Cyberkill.ai  

---

## 📜 Legal Disclaimer & License

Distributed under the **Apache 2.0 License**. See [LICENSE](LICENSE) for details.

> **Warning:** Cyberkill.ai is designed strictly for authorized penetration testing, academic research, and defensive security auditing. Testing targets without prior written authorization is strictly illegal under applicable computer crime laws.
