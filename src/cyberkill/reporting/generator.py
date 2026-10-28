"""Report Generator: Produces Markdown, JSON, and Executive HTML/PDF audit deliverables."""

import json
from typing import Any, Dict

class ReportGenerator:
    @staticmethod
    def generate_markdown(assessment_data: Dict[str, Any], author: str = "Harsh Vardhan") -> str:
        target = assessment_data.get("target", "Target Host")
        stages = assessment_data.get("stages", {})
        recon = stages.get("reconnaissance", {})
        exploit = stages.get("exploitation", {})
        defense = stages.get("purple_defense", {})
        vulns = exploit.get("vulnerabilities", [])

        md = []
        md.append(f"# 🛡️ Cyberkill.ai Security Assessment Report")
        md.append(f"**Target:** `{target}`  ")
        md.append(f"**Lead Security Architect:** {author}  ")
        md.append(f"**Framework Alignment:** Lockheed Martin Cyber Kill Chain(R) & MITRE ATT&CK(R) v15  ")
        md.append(f"**Status:** Assessment Completed  ")
        md.append("")
        md.append("## 1. Executive Summary")
        md.append(f"Cyberkill.ai conducted an autonomous multi-agent security evaluation against `{target}`. ")
        md.append(f"A total of **{len(vulns)} security findings** were identified and triaged, with automated Sigma and Snort defense signatures generated.")
        md.append("")
        md.append("## 2. Reconnaissance & Surface Analysis")
        md.append("| Open Port | Service | Banner / Version | State |")
        md.append("|---|---|---|---|")
        for p in recon.get("open_ports", []):
            md.append(f"| {p['port']} | {p['service']} | {p['banner']} | {p['state']} |")
        md.append("")
        md.append(f"**Identified Technologies:** {', '.join(recon.get('technologies', []))}")
        md.append("")
        md.append("## 3. Discovered Vulnerabilities & Risk Matrix")
        md.append("| ID | Vulnerability Title | Severity | CVSS v4 | MITRE ATT&CK |")
        md.append("|---|---|---|---|---|")
        for v in vulns:
            md.append(f"| `{v['id']}` | **{v['title']}** | `{v['severity'].upper()}` | {v['cvss']} | `{v['mitre']}` |")
        md.append("")
        md.append("## 4. Purple Team Remediation & Detection Rules")
        for c in defense.get("countermeasures", []):
            md.append(f"### Mitigations for `{c['finding_id']}`: {c['title']}")
            for step in c.get("remediation_steps", []):
                md.append(f"- {step}")
            md.append("")
            md.append("#### Generated Sigma Detection Rule")
            md.append("```yaml")
            md.append(c.get("sigma_rule", "").strip())
            md.append("```")
            md.append("")
            md.append("#### Generated Snort / Suricata Signature")
            md.append("```snort")
            md.append(c.get("snort_signature", "").strip())
            md.append("```")
            md.append("")
        md.append("---")
        md.append(f"*Generated autonomously by Cyberkill.ai by {author}.*")
        return "\n".join(md)

    @staticmethod
    def generate_json(assessment_data: Dict[str, Any]) -> str:
        return json.dumps(assessment_data, indent=2)
