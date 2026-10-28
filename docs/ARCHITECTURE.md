# Cyberkill.ai Architecture & Design Specification

## Overview
Cyberkill.ai is a state-of-the-art multi-agent cybersecurity platform and Model Context Protocol (MCP) server engineered by Harsh Vardhan.

```
                    ┌────────────────────────────────────────┐
                    │    AI Clients (Claude, Cursor, Copilot)│
                    └───────────────────┬────────────────────┘
                                        │ FastMCP Protocol (JSON-RPC)
                                        ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                             CYBERKILL.AI CORE                              │
│                                                                            │
│  ┌───────────────────────┐   ┌───────────────────┐   ┌──────────────────┐  │
│  │  FastAPI REST Server  │   │  FastMCP 2.0 Stdio│   │  CLI Controller  │  │
│  └──────────┬────────────┘   └─────────┬─────────┘   └────────┬─────────┘  │
│             └──────────────────────────┼──────────────────────┘            │
│                                        ▼                                   │
│                        ┌───────────────────────────────┐                   │
│                        │    ScopeGuard Auth Engine     │                   │
│                        └───────────────┬───────────────┘                   │
│                                        ▼                                   │
│                        ┌───────────────────────────────┐                   │
│                        │  Kill Chain StateGraph Engine │                   │
│                        └───────────────┬───────────────┘                   │
│                                        ▼                                   │
│       ┌────────────────────────────────────────────────────────┐           │
│       │               Autonomous Multi-Agent Swarm             │           │
│       │  [ReconAgent]  -->  [ExploitAgent]  --> [PurpleDefense] │           │
│       └────────────────────────────────┬───────────────────────┘           │
│                                        ▼                                   │
│       ┌────────────────────────────────────────────────────────┐           │
│       │        Unified Tool Registry (180+ Kali Tools)         │           │
│       │  Nmap, Rustscan, Nuclei, Katana, SQLmap, Prowler, etc. │           │
│       └────────────────────────────────┬───────────────────────┘           │
│                                        ▼                                   │
│                        ┌───────────────────────────────┐                   │
│                        │ Async Process Manager & Cache │                   │
│                        └───────────────────────────────┘                   │
└────────────────────────────────────────────────────────────────────────────┘
```

## Key Innovations over Legacy Frameworks
1. **ScopeGuard Active Boundary Verification**: Guarantees scans never bleed into unapproved targets.
2. **Lockheed Martin Cyber Kill Chain Alignment**: Organizes every tool into formal adversarial phases.
3. **Automated Purple Teaming**: Every exploit finding is paired with Sigma rules and Snort signatures.
4. **FastMCP 2.0 Protocol**: Zero-latency native bridge into LLM reasoning loops.
