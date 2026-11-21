# TCP/UDP Port Security Analysis Using Nmap

[![Nmap](https://img.shields.io/badge/Scanner-Nmap%207.94SVN-blue.svg)](https://nmap.org)
[![Platform](https://img.shields.io/badge/Environment-Kali%20Linux%20%7C%20Metasploitable%202-red.svg)](https://www.kali.org)
[![Language](https://img.shields.io/badge/Scripts-Bash%20%7C%20Python%203-green.svg)](https://www.python.org)
[![Security Audit](https://img.shields.io/badge/Audit-Passed%20%26%20Documented-brightgreen.svg)]()
[![Report](https://img.shields.io/badge/Report-Word%20(.docx)%20Included-orange.svg)]()

> **Mini Project:** Controlled TCP and UDP port security assessment, service fingerprinting, and vulnerability analysis using Nmap against a controlled lab target.  
> **Prepared for:** Trionix Tech Mini Project Evaluation  
> **Author / Intern:** Cybersecurity Engineering Intern  

---

## Table of Contents
- [Project Overview](#project-overview)
- [Lab Environment Architecture](#lab-environment-architecture)
- [Methodology & Port State Classification](#methodology--port-state-classification)
- [Nmap Commands Used](#nmap-commands-used)
- [Scan Results & Vulnerability Matrix](#scan-results--vulnerability-matrix)
- [Key Security Findings](#key-security-findings)
- [Remediation & Hardening Plan](#remediation--hardening-plan)
- [Repository File Structure](#repository-file-structure)
- [How to Reproduce the Audit](#how-to-reproduce-the-audit)
- [Trionix Tech Submission & Collaboration](#trionix-tech-submission--collaboration)

---

## Project Overview

Port scanning is an indispensable phase in network reconnaissance and security assessments. By identifying listening ports and running services, security analysts can uncover attack surfaces, legacy protocols, unpatched vulnerabilities, and misconfigurations.

This project delivers a complete port security analysis conducted in an isolated virtual lab environment. All TCP and UDP scans were executed using **Nmap**, followed by automated NSE vulnerability audits, resulting in a comprehensive Word Report (`.docx`) and technical documentation.

---

## Lab Environment Architecture

The project was executed in a strictly controlled, isolated virtual network:

```
               CONTROLLED LAB TOPOLOGY
 +-----------------------+        +--------------------------+
 |   KALI LINUX (VM)     |        |   METASPLOITABLE 2 (VM)  |
 |  IP: 192.168.56.102   |  <-->  |    IP: 192.168.56.101    |
 |  Attacker / Auditor   |        |    Target / Audit Node   |
 +-----------------------+        +--------------------------+
             |                                 |
             +--------[ Host-Only Net ]--------+
                     (192.168.56.0/24)
```

| Component | Virtual Machine | Operating System | IP Address | Network Adapter |
| :--- | :--- | :--- | :--- | :--- |
| **Auditor Node** | Kali Linux | Kali Rolling (Debian 64-bit) | `192.168.56.102` | VirtualBox Host-Only (`vboxnet0`) |
| **Target Node** | Metasploitable 2 | Ubuntu 8.04 LTS (Kernel 2.6.x) | `192.168.56.101` | VirtualBox Host-Only (`vboxnet0`) |

---

## Methodology & Port State Classification

The audit adopted a systematic four-phase security reconnaissance methodology:

```
[Phase 1: Host Discovery] ──> [Phase 2: TCP Scanning] ──> [Phase 3: UDP Scanning] ──> [Phase 4: NSE Vuln Audit]
```

### Port State Classification Summary

| Port State | TCP Packet Mechanism | UDP Packet Mechanism | Meaning |
| :--- | :--- | :--- | :--- |
| **`open`** | Target replies with `SYN/ACK` | Target replies with UDP payload | Application is actively listening and accepting traffic. |
| **`closed`** | Target replies with `RST` | Target replies with ICMP port unreachable | Host is up, but no application is bound to the port. |
| **`filtered`** | No response (dropped) or ICMP error | No response (dropped) or ICMP unreachable | A firewall or packet filter is blocking probe packets. |
| **`open|filtered`**| Rare in TCP | No response received to UDP probe | Port is either open or packet dropped by packet filter. |

---

## Nmap Commands Used

### 1. Network Host Discovery (ARP/Ping Sweep)
```bash
sudo nmap -sn -PR 192.168.56.0/24 -oN scans/01_network_host_discovery.nmap
```

### 2. Fast TCP SYN Stealth Scan (Top 1000 Ports)
```bash
sudo nmap -sS -v -T4 192.168.56.101 -oN scans/02_tcp_syn_stealth_scan.nmap
```

### 3. Full 65,535 TCP Port Enumeration
```bash
sudo nmap -sS -p- -T4 192.168.56.101 -oN scans/03_tcp_full_port_scan.nmap
```

### 4. Deep Service Version & OS Fingerprinting
```bash
sudo nmap -sS -sV -O -A -p 21,22,23,25,53,80,111,139,445,1524,3306,3632,5432,5900,6667,8180 192.168.56.101 -oN scans/04_tcp_service_os_detection.nmap
```

### 5. UDP Port & Version Scanning
```bash
sudo nmap -sU --top-ports 50 -v -T4 192.168.56.101 -oN scans/05_udp_top_ports_scan.nmap
sudo nmap -sU -sV -p 53,69,111,137,161,2049 192.168.56.101 -oN scans/06_udp_service_version_scan.nmap
```

### 6. Nmap Scripting Engine (NSE) Vulnerability Audit
```bash
sudo nmap --script vuln -p 21,22,23,25,80,139,445,1524,3632,6667 192.168.56.101 -oN scans/07_nse_vulnerability_audit.nmap
```

---

## Scan Results & Vulnerability Matrix

| Port/Protocol | Service | Version Detected | State | Risk Level | Notable CVE / Threat |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **21/tcp** | FTP | vsftpd 2.3.4 | `open` | **CRITICAL** | [CVE-2011-2523](https://nvd.nist.gov/vuln/detail/CVE-2011-2523) Backdoor root shell |
| **22/tcp** | SSH | OpenSSH 4.7p1 (Debian) | `open` | **MEDIUM** | Weak ciphers, brute force exposure |
| **23/tcp** | Telnet | Linux telnetd | `open` | **HIGH** | Cleartext credential transmission |
| **25/tcp** | SMTP | Postfix smtpd | `open` | **MEDIUM** | User enumeration via VRFY & EXPN |
| **53/tcp, udp**| DNS | BIND 9.4.2 | `open` | **HIGH** | DNS cache poisoning, zone transfer |
| **80/tcp** | HTTP | Apache 2.2.8 (Ubuntu) | `open` | **HIGH** | Slowloris DoS, DVWA, phpMyAdmin |
| **111/tcp, udp**| RPCbind | SunRPC 2 | `open` | **MEDIUM** | Mapped services enumeration |
| **139, 445/tcp**| SMB | Samba smbd 3.X-4.X | `open` | **CRITICAL** | [CVE-2007-2447](https://nvd.nist.gov/vuln/detail/CVE-2007-2447) username map script RCE |
| **512-514/tcp**| R-Services | rexec, rlogin, rsh | `open` | **HIGH** | Insecure .rhosts trust authentication |
| **1099/tcp**| Java RMI | GNU Classpath rmiregistry | `open` | **HIGH** | Unauthenticated remote object invocation |
| **1524/tcp**| Bindshell | Metasploitable root shell | `open` | **CRITICAL** | Direct unauthenticated root shell |
| **2049/tcp, udp**| NFS | NFS Version 2-4 | `open` | **HIGH** | Insecure exports, no root squash |
| **3306/tcp**| MySQL | MySQL 5.0.51a | `open` | **HIGH** | Remote root access with empty password |
| **3632/tcp**| DistCC | distccd v1 | `open` | **CRITICAL** | [CVE-2004-2687](https://nvd.nist.gov/vuln/detail/CVE-2004-2687) Compiler RCE |
| **5432/tcp**| PostgreSQL| PostgreSQL 8.3.0-8.3.7 | `open` | **HIGH** | Database listener exposed, weak auth |
| **5900/tcp**| VNC | VNC Protocol 3.3 | `open` | **HIGH** | Weak authentication (password: `password`) |
| **6667/tcp**| IRC | UnrealIRCd 3.2.8.1 | `open` | **CRITICAL** | [CVE-2010-2075](https://nvd.nist.gov/vuln/detail/CVE-2010-2075) Trojaned backdoor RCE |
| **8180/tcp**| Tomcat | Apache Tomcat/5.5 | `open` | **HIGH** | Default manager credentials (`tomcat:tomcat`) |
| **69/udp** | TFTP | Linux TFTP | `open` | **HIGH** | Unauthenticated file read/write |
| **161/udp** | SNMP | net-snmp SNMPv1 | `open` | **HIGH** | Default community string `public` |

---

## Key Security Findings

1. **Direct Remote Code Execution (RCE):** Backdoor triggers in `vsftpd 2.3.4` (CVE-2011-2523) and `UnrealIRCd 3.2.8.1` (CVE-2010-2075), along with the `username map script` vulnerability in Samba (CVE-2007-2447), allow instantaneous remote code execution under `root` privileges.
2. **Unauthenticated Shell Port 1524:** Connecting to port 1524 via `nc 192.168.56.101 1524` yields an interactive root shell immediately without any authentication challenge.
3. **Insecure Cleartext Protocols:** Telnet (port 23) and R-services (ports 512-514) allow attackers to intercept passwords via network sniffing.
4. **Exposed Administrative & Database Portals:** MySQL (3306), PostgreSQL (5432), and Tomcat Manager (8180) are bound to all network interfaces and configured with default or blank credentials.
5. **UDP Information Leaks:** SNMPv1 on port 161/udp exposes full host parameters, process lists, and network routing tables using the default community string `public`.

---

## Remediation & Hardening Plan

1. **Firewall Ingress Controls:** Deploy `iptables` or `ufw` to enforce a default-deny ingress rule. Permit only necessary inbound traffic (e.g. port 22 for SSH or port 443 for HTTPS).
2. **Decommission Vulnerable Daemons:** Uninstall `vsftpd 2.3.4`, `telnetd`, `rsh`, `rlogin`, and kill the port 1524 bindshell.
3. **Service Localhost Binding:** Reconfigure MySQL (`bind-address = 127.0.0.1`) and PostgreSQL to bind only to the local loopback interface.
4. **Cryptographic Upgrades:** Enforce SSH key-based authentication (disable password logins). Upgrade SNMPv1/v2 to SNMPv3 with `authPriv` (SHA authentication + AES encryption).
5. **Continuous Port Auditing:** Integrate recurring Nmap scans into CI/CD pipelines and cron jobs to promptly detect configuration drift.

---

## Repository File Structure

```
.
├── TCP_UDP_Port_Security_Analysis_Report.docx  # Primary Word Report deliverable
├── README.md                                  # Complete repository documentation
├── .gitignore                                 # Git ignore file
├── docs/
│   ├── Project_Report.md                      # Complete Markdown project report
│   └── TCP_UDP_Port_Security_Analysis_Report.docx # Backup copy of Word Report
├── scans/
│   ├── 01_network_host_discovery.nmap         # Phase 1: Host discovery scan
│   ├── 02_tcp_syn_stealth_scan.nmap          # Phase 2: Top 1000 TCP ports scan
│   ├── 03_tcp_full_port_scan.nmap            # Phase 3: All 65,535 TCP ports scan
│   ├── 04_tcp_service_os_detection.nmap      # Phase 4: Service versions & OS detection
│   ├── 05_udp_top_ports_scan.nmap            # Phase 5: Top UDP ports scan
│   ├── 06_udp_service_version_scan.nmap      # Phase 6: UDP service fingerprinting
│   ├── 07_nse_vulnerability_audit.nmap       # Phase 7: NSE vulnerability audit
│   └── full_lab_audit.xml                     # Machine-readable Nmap XML output
└── scripts/
    ├── run_port_security_audit.sh             # Bash automation script for Kali Linux
    ├── parse_scan_results.py                  # Python scan parser & summary generator
    └── generate_docx_report.py                # Python generator for the Word report
```
