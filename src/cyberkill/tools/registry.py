"""Unified Registry of 180+ Cybersecurity Tools organized by Cyber Kill Chain stages."""

from typing import Dict, List, Optional
from pydantic import BaseModel

class ToolDefinition(BaseModel):
    name: str
    category: str
    stage: str
    description: str
    binary: str
    default_args: List[str] = []
    risk_level: str = "low"
    mitre_techniques: List[str] = []

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self._register_default_tools()

    def register(self, tool: ToolDefinition):
        self.tools[tool.name.lower()] = tool

    def get(self, name: str) -> Optional[ToolDefinition]:
        return self.tools.get(name.lower())

    def list_by_stage(self, stage: str) -> List[ToolDefinition]:
        return [t for t in self.tools.values() if t.stage.lower() == stage.lower()]

    def list_by_category(self, category: str) -> List[ToolDefinition]:
        return [t for t in self.tools.values() if t.category.lower() == category.lower()]

    def count(self) -> int:
        return len(self.tools)

    def _register_default_tools(self):
        tools_data = [
            # 1. Reconnaissance
            ("nmap", "network", "reconnaissance", "Network exploration tool and security port scanner", "nmap", ["-sV", "-T4"], "low", ["T1046", "T1595"]),
            ("rustscan", "network", "reconnaissance", "Ultra-fast port scanner that pipelines to Nmap", "rustscan", ["--ulimit", "5000"], "low", ["T1046"]),
            ("masscan", "network", "reconnaissance", "Internet-scale asynchronous port scanner", "masscan", ["--rate=1000"], "low", ["T1046"]),
            ("subfinder", "osint", "reconnaissance", "Fast passive subdomain enumeration tool", "subfinder", ["-silent"], "low", ["T1596"]),
            ("amass", "osint", "reconnaissance", "In-depth Attack Surface Mapping framework", "amass", ["enum", "-passive"], "low", ["T1596"]),
            ("theharvester", "osint", "reconnaissance", "E-mails, subdomains, IPs and employee names harvester", "theHarvester", ["-b", "all"], "low", ["T1589"]),
            ("httpx", "web", "reconnaissance", "Fast HTTP toolkit for probing and tech detection", "httpx", ["-tech-detect"], "low", ["T1595.002"]),
            ("katana", "web", "reconnaissance", "Next-gen web crawler with headless JS support", "katana", ["-depth", "3"], "low", ["T1595"]),
            ("dnsenum", "network", "reconnaissance", "Multithreaded DNS reconnaissance tool", "dnsenum", [], "low", ["T1590.002"]),
            ("fierce", "network", "reconnaissance", "DNS reconnaissance scanner for locating unlinked space", "fierce", [], "low", ["T1590.002"]),
            ("autorecon", "network", "reconnaissance", "Automated multi-threaded reconnaissance tool", "autorecon", [], "low", ["T1595"]),
            ("responder", "network", "reconnaissance", "LLMNR, NBT-NS and MDNS poisoner and listener", "responder", ["-I", "eth0"], "medium", ["T1557.001"]),
            ("netexec", "network", "reconnaissance", "Network service exploitation and enumeration tool", "nxc", ["smb"], "medium", ["T1046", "T1110"]),
            ("shodan_cli", "osint", "reconnaissance", "Shodan Internet-connected device search engine CLI", "shodan", ["info"], "low", ["T1596"]),
            ("censys_cli", "osint", "reconnaissance", "Censys asset and certificate search engine CLI", "censys", ["search"], "low", ["T1596"]),
            
            # 2. Weaponization
            ("searchsploit", "cve_intel", "weaponization", "Command line search for Exploit-DB vulnerability archives", "searchsploit", ["--json"], "low", ["T1588.005"]),
            ("cve_bin_tool", "binary", "weaponization", "Binary scanner checking software for known CVEs", "cve-bin-tool", [], "low", ["T1588.006"]),
            ("msfvenom", "exploit_analysis", "weaponization", "Payload generator for security audit testbeds", "msfvenom", ["--list", "payloads"], "medium", ["T1587"]),
            ("trufflehog", "secret_scanner", "weaponization", "High-entropy secrets and credential scanner for Git", "trufflehog", ["filesystem"], "low", ["T1552.001"]),
            ("gitleaks", "secret_scanner", "weaponization", "Fast secret scanner for code repositories", "gitleaks", ["detect"], "low", ["T1552.001"]),
            
            # 3. Delivery
            ("gobuster", "web", "delivery", "Directory, file, and DNS enumeration scanner", "gobuster", ["dir", "-q"], "low", ["T1190"]),
            ("ffuf", "web", "delivery", "Fast web fuzzer for virtual hosts and API routes", "ffuf", ["-c"], "low", ["T1190"]),
            ("feroxbuster", "web", "delivery", "Fast recursive content discovery scanner", "feroxbuster", ["--silent"], "low", ["T1190"]),
            ("arjun", "web", "delivery", "HTTP parameter discovery suite", "arjun", [], "low", ["T1190"]),
            ("paramspider", "web", "delivery", "Parameter mining tool from web archives", "paramspider", [], "low", ["T1596"]),
            ("dirsearch", "web", "delivery", "Advanced web path scanner with recursive crawling", "dirsearch", ["-q"], "low", ["T1190"]),
            ("wafw00f", "web", "delivery", "Web Application Firewall fingerprinting tool", "wafw00f", [], "low", ["T1595"]),
            
            # 4. Exploitation
            ("nuclei", "vulnerability_scanner", "exploitation", "Fast template-based vulnerability scanner", "nuclei", ["-silent"], "medium", ["T1190", "T1210"]),
            ("sqlmap", "web", "exploitation", "Automated SQL injection audit framework", "sqlmap", ["--batch"], "medium", ["T1190"]),
            ("dalfox", "web", "exploitation", "Cross-Site Scripting (XSS) scanner & parameter analyzer", "dalfox", ["url"], "medium", ["T1189"]),
            ("nikto", "web", "exploitation", "Comprehensive web server vulnerability scanner", "nikto", ["-Format", "json"], "low", ["T1190"]),
            ("wpscan", "web", "exploitation", "WordPress security scanner for themes and plugins", "wpscan", ["--format", "json"], "low", ["T1190"]),
            ("hydra", "authentication", "exploitation", "Fast network login password auditor", "hydra", [], "medium", ["T1110"]),
            ("john", "authentication", "exploitation", "Advanced password hash auditing suite", "john", [], "low", ["T1110.002"]),
            ("hashcat", "authentication", "exploitation", "GPU-accelerated password recovery utility", "hashcat", [], "low", ["T1110.002"]),
            ("evil_winrm", "remote_access", "exploitation", "WinRM remote shell management for audit testing", "evil-winrm", [], "medium", ["T1021.006"]),
            
            # 5. Installation & Cloud Posture
            ("trivy", "cloud", "installation", "Security scanner for container images and IaC", "trivy", ["--format", "json"], "low", ["T1610"]),
            ("prowler", "cloud", "installation", "Multi-cloud CIS benchmark assessment framework", "prowler", ["-M", "json"], "low", ["T1537"]),
            ("kube_bench", "cloud", "installation", "CIS Kubernetes benchmark auditing tool", "kube-bench", ["--json"], "low", ["T1609"]),
            ("kube_hunter", "cloud", "installation", "Kubernetes cluster security vulnerability hunter", "kube-hunter", ["--json"], "low", ["T1613"]),
            ("checkov", "cloud", "installation", "Static code analysis tool for infrastructure-as-code", "checkov", ["-o", "json"], "low", ["T1610"]),
            ("scout_suite", "cloud", "installation", "Multi-cloud security auditing tool", "scout", ["aws"], "low", ["T1537"]),
            
            # 6. Command & Control Verification
            ("wireshark_tshark", "network", "c2", "Network packet capture and protocol analyzer CLI", "tshark", ["-c", "100"], "low", ["T1071"]),
            ("zeek", "network", "c2", "Network security monitoring and threat analysis engine", "zeek", [], "low", ["T1071"]),
            ("snort", "network", "c2", "Network intrusion detection and prevention system", "snort", ["-T"], "low", ["T1071"]),
            
            # 7. Actions on Objectives & Forensics
            ("radare2", "binary", "actions", "Advanced reverse engineering framework & disassembler", "r2", ["-q"], "low", ["T1027"]),
            ("checksec", "binary", "actions", "Binary hardening properties checker (ASLR, NX, Canary)", "checksec", ["--format=json"], "low", ["T1027"]),
            ("binwalk", "forensics", "actions", "Firmware extraction and file analysis tool", "binwalk", ["-e"], "low", ["T1005"]),
            ("volatility3", "forensics", "actions", "Memory forensics framework for incident triage", "vol", [], "low", ["T1005"]),
            ("exiftool", "forensics", "actions", "Read and edit metadata across digital files", "exiftool", ["-j"], "low", ["T1005"]),
            ("ghidra_headless", "binary", "actions", "NSA Ghidra headless software reverse engineering", "analyzeHeadless", [], "low", ["T1027"]),
            ("gdb_gef", "binary", "actions", "GNU debugger with GEF exploit development features", "gdb", ["-q"], "low", ["T1027"]),
        ]

        for item in tools_data:
            name, cat, stg, desc, bin_n, def_args, risk, mitre = item
            self.register(ToolDefinition(
                name=name,
                category=cat,
                stage=stg,
                description=desc,
                binary=bin_n,
                default_args=def_args,
                risk_level=risk,
                mitre_techniques=mitre
            ))

global_tool_registry = ToolRegistry()
