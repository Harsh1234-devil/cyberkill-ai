# Lockheed Martin Cyber Kill Chain(R) Mapping

Cyberkill.ai maps all operations to the 7 stages of the Cyber Kill Chain:

| Stage | Name | Description | Key Cyberkill Tools |
|---|---|---|---|
| 1 | **Reconnaissance** | Harvesting email addresses, subdomains, open ports, banners | Nmap, Rustscan, Amass, Subfinder, TheHarvester, HTTPx |
| 2 | **Weaponization** | Pairing exploits with payloads and analyzing CVE databases | Searchsploit, CVE-Bin-Tool, MSFVenom, Trufflehog |
| 3 | **Delivery** | Probing transmission paths, entry points, and web routes | Gobuster, FFuf, Feroxbuster, Arjun, ParamSpider |
| 4 | **Exploitation** | Triggering vulnerabilities on target applications safely | Nuclei, SQLMap, Dalfox, Nikto, WPScan, Hydra |
| 5 | **Installation** | Auditing persistence vectors and cloud infrastructure | Trivy, Prowler, Kube-bench, Kube-hunter, Checkov |
| 6 | **Command & Control** | Network protocol analysis and egress filtering checks | TShark, Zeek, Snort |
| 7 | **Actions on Objectives**| Binary reverse engineering and forensics analysis | Radare2, Checksec, Binwalk, Volatility3, Exiftool |
| + | **Purple Team Defense**| Automated mitigation, patch generation, and Sigma rules | Cyberkill PurpleDefense Engine |
