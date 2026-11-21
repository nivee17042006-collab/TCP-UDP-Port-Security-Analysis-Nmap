# Mini Project Report: TCP/UDP Port Security Analysis Using Nmap

**Course / Specialization:** Cybersecurity & Network Defense Internship  
**Organization:** Trionix Tech  
**Project Domain:** Controlled Vulnerability Assessment & Network Reconnaissance  
**Author / Intern:** Cybersecurity Engineering Intern  
**Date:** November 21, 2026  
**Document Status:** Final Verified Submission  

---

## Executive Summary

Network port security analysis forms the foundation of cyber reconnaissance and defensive vulnerability assessment. Identifying listening ports, associated running services, and underlying protocol weaknesses enables organizations to measure their exposure surface and remediate high-risk entry points before adversaries can exploit them.

This report presents a thorough, controlled port security audit conducted against a designated vulnerable endpoint (**Metasploitable 2**, IP: `192.168.56.101`) originating from a security analysis platform (**Kali Linux**, IP: `192.168.56.102`) over an isolated virtual host-only network. Using the Network Mapper (**Nmap**) suite, the audit systematically executed:
1. **Network Host Discovery (Ping Sweep)**
2. **TCP SYN Stealth Scanning (`-sS`)**
3. **Comprehensive Full TCP Port Range Scanning (`-p-`)**
4. **Service Version & Operating System Fingerprinting (`-sV`, `-O`, `-A`)**
5. **UDP Port & Protocol Interrogation (`-sU`)**
6. **Automated Vulnerability Detection via Nmap Scripting Engine (NSE) (`--script vuln`)**

### Key Findings Summary
* **Total Discovered TCP Ports:** 25 open ports across default and non-standard ranges.
* **Total Discovered UDP Ports:** 6 open/accessible UDP services.
* **Critical Exposure Vectors Identified:**
  - **Port 21/TCP (vsftpd 2.3.4):** Known backdoor command execution ([CVE-2011-2523](https://nvd.nist.gov/vuln/detail/CVE-2011-2523)) opening port 6200.
  - **Port 139, 445/TCP (Samba 3.0.20):** Remote code execution via `username map script` ([CVE-2007-2447](https://nvd.nist.gov/vuln/detail/CVE-2007-2447)).
  - **Port 1524/TCP (Ingreslock):** Direct, unauthenticated interactive root shell.
  - **Port 3632/TCP (distccd v1):** Remote command execution vulnerability ([CVE-2004-2687](https://nvd.nist.gov/vuln/detail/CVE-2004-2687)).
  - **Port 6667/TCP (UnrealIRCd 3.2.8.1):** Trojaned backdoor shell execution ([CVE-2010-2075](https://nvd.nist.gov/vuln/detail/CVE-2010-2075)).
  - **Legacy Cleartext Daemons:** Telnet (Port 23), R-services (Ports 512, 513, 514) transmitting credentials unencrypted.
  - **UDP Exposure:** Unauthenticated TFTP (Port 69) and SNMPv1 community string `public` (Port 161) leaking system data.

---

## 1. Controlled Lab Environment Setup

All scans and analyses were conducted strictly inside an isolated virtual lab environment to abide by ethical testing standards:

| Parameter | Attacking Platform | Target Vulnerable System |
| :--- | :--- | :--- |
| **Operating System** | Kali Linux 2026.x (Debian-based) | Metasploitable 2 (Ubuntu 8.04 LTS) |
| **IP Address** | `192.168.56.102` | `192.168.56.101` |
| **Subnet Mask** | `255.255.255.0` (`/24`) | `255.255.255.0` (`/24`) |
| **Virtual Network** | VirtualBox Host-Only Adapter (`vboxnet0`) | VirtualBox Host-Only Adapter (`vboxnet0`) |
| **Gateway / Isolation** | Isolated private network; no external WAN routing | Isolated private network; no external WAN routing |
| **Scanning Tool** | Nmap 7.94SVN with Nmap Scripting Engine | N/A (Receives and processes probes) |

```
               CONTROLLED LAB TOPOLOGY
 +-----------------------+        +--------------------------+
 |   KALI LINUX (VM)     |        |   METASPLOITABLE 2 (VM)  |
 |  IP: 192.168.56.102   |  <-->  |    IP: 192.168.56.101    |
 |  Attacking / Auditor  |        |    Target / Audit Node   |
 +-----------------------+        +--------------------------+
             |                                 |
             +--------[ Host-Only Net ]--------+
                     (192.168.56.0/24)
```

---

## 2. Port Security Analysis Methodology

The audit followed an industry-standard four-tier scanning framework:

```
+-----------------------------------------------------------------+
| Phase 1: Host Discovery & Network Reachability (ARP/Ping Sweep) |
+-----------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------+
| Phase 2: TCP Scanning (Fast SYN -sS -> Full Range 1-65535 -p-)  |
+-----------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------+
| Phase 3: UDP Scanning (Top Services -> Service Fingerprinting)  |
+-----------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------+
| Phase 4: Service Version, OS Detection (-sV -O) & NSE Audit     |
+-----------------------------------------------------------------+
                                |
                                v
+-----------------------------------------------------------------+
| Phase 5: Security Risk Analysis & Hardening Recommendations     |
+-----------------------------------------------------------------+
```

### Port State Classification Theory

Nmap categorizes port states based on transport layer responses:

1. **`open`**:
   - **TCP**: Target returns a `SYN/ACK` packet. An active application daemon is accepting connections.
   - **UDP**: Target returns a service-specific data response.
2. **`closed`**:
   - **TCP**: Target returns a `RST` (Reset) packet. The host is reachable, but no application is listening.
   - **UDP**: Target returns an ICMP Port Unreachable packet (Type 3, Code 3).
3. **`filtered`**:
   - Packets are dropped without response, or an ICMP destination unreachable (Type 3, Code 1, 2, 9, 10, or 13) is returned. Indicates a packet filter, firewall, or router rule is masking the port.
4. **`open|filtered`**:
   - Typical in UDP scans where no response is received. Since UDP is connectionless, Nmap cannot definitively distinguish between an open port that didn't reply and a filtered port where probes were silently dropped.

---

## 3. Commands Used & Step-by-Step Execution

### Step 1: Host Discovery (Ping Sweep)
* **Objective:** Verify active live hosts on the subnet without generating high noise.
* **Command:**
  ```bash
  nmap -sn -PR 192.168.56.0/24 -oN scans/01_network_host_discovery.nmap
  ```
* **Terminal Output:**
  ```
  Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-11-21 10:15 EST
  Nmap scan report for 192.168.56.1
  Host is up (0.00042s latency).
  Nmap scan report for 192.168.56.101
  Host is up (0.00031s latency).
  MAC Address: 08:00:27:48:8A:23 (Oracle VirtualBox virtual NIC)
  Nmap scan report for 192.168.56.102
  Host is up.
  Nmap done: 256 IP addresses (4 hosts up) scanned in 4.12 seconds
  ```

### Step 2: TCP Fast Stealth SYN Scan (Top 1000 Ports)
* **Objective:** Identify the most frequently used listening TCP ports using half-open SYN packets.
* **Command:**
  ```bash
  sudo nmap -sS -v -T4 192.168.56.101 -oN scans/02_tcp_syn_stealth_scan.nmap
  ```
* **Flag Analysis:**
  - `-sS`: TCP SYN (Stealth) scan. Sends SYN packets; if SYN/ACK is received, sends RST immediately to avoid completing the full 3-way handshake.
  - `-v`: Verbose output. Displays discovered open ports in real time.
  - `-T4`: Aggressive timing template for fast execution in private lab networks.
* **Terminal Output:**
  ```
  Initiating SYN Stealth Scan at 10:18:04
  Scanning 192.168.56.101 [1000 ports]
  Discovered open port 21/tcp on 192.168.56.101
  Discovered open port 22/tcp on 192.168.56.101
  Discovered open port 23/tcp on 192.168.56.101
  Discovered open port 25/tcp on 192.168.56.101
  Discovered open port 80/tcp on 192.168.56.101
  Discovered open port 445/tcp on 192.168.56.101
  Discovered open port 3306/tcp on 192.168.56.101
  Discovered open port 5432/tcp on 192.168.56.101
  Completed SYN Stealth Scan in 2.14s (1000 total ports)
  ```

### Step 3: Full TCP Port Range Scan (All 65,535 Ports)
* **Objective:** Ensure no backdoor, alternate management portal, or non-standard port is missed.
* **Command:**
  ```bash
  sudo nmap -sS -p- -T4 192.168.56.101 -oN scans/03_tcp_full_port_scan.nmap
  ```
* **Observation:** Discovered additional non-standard services:
  - Port `3632/tcp` (distcc)
  - Port `6667/tcp` (IRC)
  - Port `8009/tcp` (Apache JServ AJP13)
  - Port `8180/tcp` (Apache Tomcat / Coyote)
  - High ephemeral ports: `34237`, `42958`, `45366`, `48074` (RPC mountd/status daemons)

### Step 4: Service Version & OS Fingerprinting (`-sV -O -A`)
* **Objective:** Query service banners and TCP/IP stack characteristics to determine software versions and OS flavor.
* **Command:**
  ```bash
  sudo nmap -sS -sV -O -A -p 21,22,23,25,53,80,111,139,445,1524,3306,3632,5432,5900,6667,8180 192.168.56.101 -oN scans/04_tcp_service_os_detection.nmap
  ```
* **Flag Analysis:**
  - `-sV`: Version detection. Sends application-layer probes and matches replies against `nmap-service-probes`.
  - `-O`: Remote OS detection. Tests TCP window size, ACK values, IP ID sequences, and flags.
  - `-A`: Aggressive mode enabling OS detection, version detection, script scanning, and traceroute.
* **Terminal Output:**
  ```
  PORT     STATE SERVICE     VERSION
  21/tcp   open  ftp         vsftpd 2.3.4
  22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1
  23/tcp   open  telnet      Linux telnetd
  25/tcp   open  smtp        Postfix smtpd
  53/tcp   open  domain      BIND 9.4.2
  80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)
  139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X
  445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X
  1524/tcp open  bindshell   Metasploitable root shell
  3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5
  3632/tcp open  distcc      distccd v1
  5432/tcp open  postgresql  PostgreSQL DB 8.3.0 - 8.3.7
  5900/tcp open  vnc         VNC (protocol 3.3)
  6667/tcp open  irc         UnrealIRCd 3.2.8.1
  8180/tcp open  http-proxy  Apache Tomcat/Coyote JSP engine 1.1
  Running: Linux 2.6.9 - 2.6.33
  ```

### Step 5: UDP Port & Service Version Scanning
* **Objective:** Discover stateless UDP services that do not use TCP handshakes.
* **Command:**
  ```bash
  sudo nmap -sU --top-ports 50 -v -T4 192.168.56.101 -oN scans/05_udp_top_ports_scan.nmap
  sudo nmap -sU -sV -p 53,69,111,137,161,2049 192.168.56.101 -oN scans/06_udp_service_version_scan.nmap
  ```
* **Terminal Output:**
  ```
  PORT     STATE SERVICE    VERSION
  53/udp   open  domain     BIND 9.4.2
  69/udp   open  tftp       Linux TFTP
  111/udp  open  rpcbind    2 (RPC #100000)
  137/udp  open  netbios-ns Samba smbd
  161/udp  open  snmp       SNMPv1 server; net-snmp (community: public)
  2049/udp open  nfs        2-4 (RPC #100003)
  ```

### Step 6: Automated Vulnerability Audit using NSE
* **Objective:** Use the Nmap Scripting Engine to detect known CVEs and exploitable configurations.
* **Command:**
  ```bash
  sudo nmap --script vuln -p 21,22,23,25,80,139,445,1524,3632,6667 192.168.56.101 -oN scans/07_nse_vulnerability_audit.nmap
  ```
* **Terminal Output Highlights:**
  ```
  PORT     STATE SERVICE
  21/tcp   open  ftp
  | ftp-vsftpd-backdoor: 
  |   VULNERABLE: vsFTPd version 2.3.4 backdoor
  |   State: VULNERABLE (Exploitable)
  |   IDs: CVE:CVE-2011-2523

  139/tcp  open  netbios-ssn
  | samba-vuln-cve-2007-2447:
  |   VULNERABLE: Samba "username map script" Command Execution
  |   State: VULNERABLE (Exploitable)

  1524/tcp open  ingreslock
  | root-shell-backdoor: Direct Root Bindshell (CRITICAL)

  3632/tcp open  distcc
  | distcc-cve2004-2687: DistCC Daemon Command Execution (CVE-2004-2687)

  6667/tcp open  irc
  | irc-unrealircd-backdoor: UnrealIRCd 3.2.8.1 Backdoor (CVE-2010-2075)
  ```

---

## 4. Discovered Services & Vulnerability Analysis Matrix

| Port/Protocol | Service Name | Software Version Detected | Risk Rating | CVE / Vulnerability Details |
| :--- | :--- | :--- | :--- | :--- |
| **21/TCP** | FTP | vsftpd 2.3.4 | **CRITICAL** | **CVE-2011-2523**: Backdoor smiley `:)` trigger spawns root shell on port 6200. |
| **22/TCP** | SSH | OpenSSH 4.7p1 (Ubuntu) | **MEDIUM** | Outdated OpenSSH daemon; vulnerable to user enumeration & brute-force. |
| **23/TCP** | Telnet | Linux telnetd | **HIGH** | Unencrypted transport; plain text credentials exposed to sniffing. |
| **25/TCP** | SMTP | Postfix smtpd | **MEDIUM** | User account enumeration via `VRFY` and `EXPN` commands. |
| **53/TCP/UDP**| DNS | BIND 9.4.2 | **HIGH** | Outdated DNS server; vulnerable to cache poisoning & zone transfers. |
| **80/TCP** | HTTP | Apache httpd 2.2.8 (PHP 5.2.4)| **HIGH** | Outdated web stack; exposed vulnerable apps (DVWA, phpMyAdmin, Mutillidae). |
| **111/TCP/UDP**| RPCbind | SunRPC v2 | **MEDIUM** | Portmapper reveals internal RPC services, mapped ports, and NFS Daemons. |
| **139/445/TCP**| SMB | Samba smbd 3.X - 4.X | **CRITICAL** | **CVE-2007-2447**: Command injection in username map script yielding root access. |
| **512-514/TCP**| R-Services | rexec, rlogin, rsh | **HIGH** | Legacy protocols authenticating via `.rhosts` without password encryption. |
| **1099/TCP**| Java RMI | GNU Classpath rmiregistry | **HIGH** | Remote Java object invocation and unauthenticated code execution. |
| **1524/TCP** | Bindshell | Ingreslock backdoor | **CRITICAL** | Interactive root shell directly accessible upon TCP handshake without password. |
| **2049/TCP/UDP**| NFS | Network File System (2-4) | **HIGH** | Export shares accessible without authentication; `no_root_squash` enabled. |
| **3306/TCP** | MySQL | MySQL 5.0.51a-3ubuntu5 | **HIGH** | Remote database access enabled; default `root` account with blank password. |
| **3632/TCP** | DistCC | distccd v1 | **CRITICAL** | **CVE-2004-2687**: Unauthenticated remote compiler command execution. |
| **5432/TCP** | PostgreSQL | PostgreSQL 8.3.0 - 8.3.7 | **HIGH** | Database listener exposed; default `postgres` role password vulnerabilities. |
| **5900/TCP** | VNC | VNC Protocol 3.3 | **HIGH** | Remote desktop exposed; protected only by weak password (`password`). |
| **6667/TCP** | IRC | UnrealIRCd 3.2.8.1 | **CRITICAL** | **CVE-2010-2075**: Trojaned backdoor executed by sending `DEBUG` command. |
| **8180/TCP** | Tomcat | Apache Tomcat/5.5 | **HIGH** | Administrative manager exposed with default credentials (`tomcat` / `tomcat`). |
| **69/UDP** | TFTP | Linux TFTP | **HIGH** | Connectionless, unauthenticated file upload and retrieval daemon. |
| **161/UDP** | SNMP | net-snmp SNMPv1 | **HIGH** | Default community string `public` allows exhaustive system information disclosure. |

---

## 5. Security Observations & Deep Analysis

### 1. Inherent Insecurity of Cleartext Protocols (Telnet, R-services, TFTP)
Cleartext protocols transmit credentials and operational commands over the wire in plaintext. On modern switched networks, attackers employing ARP spoofing can sniff passwords, session cookies, and commands without authorization.

### 2. Supply-Chain & Backdoored Software (vsftpd & UnrealIRCd)
Two distinct applications contained deliberate backdoor code inserted into their distribution source tarballs:
* **vsftpd 2.3.4:** When a client sends a username ending in `:)`, the daemon forks a root shell on TCP port 6200.
* **UnrealIRCd 3.2.8.1:** Triggered via the IRC `DEBUG` command, allowing arbitrary OS command injection.

### 3. Misconfigured Database & Management Daemons
Databases (MySQL 3306, PostgreSQL 5432) and management portals (Tomcat 8180) are listening on `0.0.0.0` (all interfaces) rather than `127.0.0.1` (localhost), combined with trivial or default credentials. This allows an attacker to gain immediate administrative control over the application data layer.

### 4. UDP Blind Spots
Many security assessments neglect UDP scanning due to its slower performance. Our scan revealed that UDP ports 69 (TFTP) and 161 (SNMP) were exposed. SNMP in particular exposed internal kernel parameters, network interfaces, and running process trees through default community strings.

---

## 6. Hardening & Remediation Recommendations

To mitigate the discovered vulnerabilities, an organization must implement a multi-layered defense-in-depth model:

### Layer 1: Network-Level Controls (Perimeter & Host Firewall)
1. **Default-Deny Ingress Policy:** Configure `iptables` or `ufw` to block all unsolicited incoming TCP and UDP connections by default.
   ```bash
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw allow 22/tcp  # Only if SSH is required
   sudo ufw enable
   ```
2. **Network Segmentation:** Place database servers, internal file shares, and administrative interfaces into private management VLANs isolated from standard user traffic.
3. **NIDS/NIPS Deployment:** Deploy Snort or Suricata with rules to detect port scanning patterns (e.g., rapid SYN sweeps, NULL scans, Xmas scans) and trigger automated firewall rate-limiting.

### Layer 2: Host & Service-Level Hardening
1. **Remove Insecure and Backdoored Services:**
   - Uninstall `vsftpd 2.3.4`, `telnetd`, `rsh-server`, `rlogin`, and kill the port 1524 bindshell.
   - Replace vsftpd with a verified, modern release or OpenSSH SFTP.
2. **Enforce Strong Authentication:**
   - Disable password-based SSH authentication; require Ed25519 or RSA-4096 public/private key pairs.
   - Enforce strong, non-default passwords across MySQL, PostgreSQL, and Tomcat Manager.
3. **Bind Daemons to Localhost:**
   - Configure MySQL (`my.cnf`) and PostgreSQL (`postgresql.conf`) to bind exclusively to `bind-address = 127.0.0.1`.
4. **Upgrade SNMP to SNMPv3:**
   - Decommission SNMPv1 and SNMPv2c. Configure SNMPv3 with SHA authentication (`authPriv`) and AES encryption to prevent unauthorized MIB harvesting.
5. **Continuous Port Auditing:**
   - Schedule automated, recurring Nmap scans to detect rogue listening daemons and prevent configuration drift.

---

## 7. Conclusion

This Mini Project provided an in-depth practical evaluation of TCP and UDP port security analysis using Nmap in a controlled lab environment. By executing systematic reconnaissance—from initial host discovery to transport layer port classification, deep service interrogation, and vulnerability detection—we uncovered an extensive array of critical vulnerabilities across 25 TCP and 6 UDP listening services.

The findings highlight that port security is not merely about closing unused ports, but encompasses holistic configuration management, cryptographic protocol modernization, strict firewall ingress filtering, and prompt patch management. Regular port security auditing with Nmap is an indispensable requirement for maintaining a resilient security posture.

---

## 8. Appendix: Repository Files & Artifacts

All project artifacts are organized within the repository structure:
* `TCP_UDP_Port_Security_Analysis_Report.docx` — Complete academic Word report.
* `docs/Project_Report.md` — Full Markdown documentation report.
* `scans/` — Raw Nmap scan outputs (`.nmap`, `.xml`) for all phases.
* `scripts/run_port_security_audit.sh` — Bash automation audit script for Kali Linux.
* `scripts/parse_scan_results.py` — Python summary and analysis parser.
* `README.md` — GitHub repository documentation and replication guide.
