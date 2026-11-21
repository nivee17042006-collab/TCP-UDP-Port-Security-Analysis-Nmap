#!/bin/bash
# ==============================================================================
# Script Name: run_port_security_audit.sh
# Project: TCP/UDP Port Security Analysis Using Nmap
# Target Environment: Controlled Lab (Kali Linux -> Metasploitable 2)
# Author: Cybersecurity Intern
# Organization: Trionix Tech Mini Project
# ==============================================================================

set -e

# Default Target IP (Metasploitable 2 VM in host-only / internal network)
TARGET_IP="${1:-192.168.56.101}"
OUTPUT_DIR="./scans"

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================================${NC}"
echo -e "${GREEN}   TCP/UDP Port Security Analysis & Vulnerability Audit Tool${NC}"
echo -e "${BLUE}====================================================================${NC}"
echo -e "Target IP : ${YELLOW}${TARGET_IP}${NC}"
echo -e "Scan Date : $(date)"
echo -e "Output Dir: ${OUTPUT_DIR}\n"

# Check root privilege
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}[!] Error: This script must be run as root (sudo) for raw packet TCP SYN (-sS) and UDP (-sU) scans.${NC}"
   exit 1
fi

mkdir -p "${OUTPUT_DIR}"

# Step 1: Host Discovery (Ping Sweep)
echo -e "${YELLOW}[*] Phase 1: Host Discovery (ARP/ICMP Ping Sweep)...${NC}"
nmap -sn -PR "${TARGET_IP}" -oN "${OUTPUT_DIR}/01_network_host_discovery.nmap"
echo -e "${GREEN}[+] Host discovery complete.${NC}\n"

# Step 2: TCP Fast Stealth SYN Scan (Top 1000 ports)
echo -e "${YELLOW}[*] Phase 2: TCP SYN Stealth Scan (Top 1000 ports)...${NC}"
nmap -sS -v -T4 "${TARGET_IP}" -oN "${OUTPUT_DIR}/02_tcp_syn_stealth_scan.nmap"
echo -e "${GREEN}[+] TCP SYN scan complete.${NC}\n"

# Step 3: Full TCP Port Scan (1-65535)
echo -e "${YELLOW}[*] Phase 3: Comprehensive TCP Scan (All 65535 ports)...${NC}"
nmap -sS -p- -T4 "${TARGET_IP}" -oN "${OUTPUT_DIR}/03_tcp_full_port_scan.nmap"
echo -e "${GREEN}[+] Full TCP scan complete.${NC}\n"

# Step 4: Service Version & OS Detection
echo -e "${YELLOW}[*] Phase 4: Service Version Fingerprinting & OS Detection (-sV -O -A)...${NC}"
nmap -sS -sV -O -A -T4 "${TARGET_IP}" -oN "${OUTPUT_DIR}/04_tcp_service_os_detection.nmap"
echo -e "${GREEN}[+] Service & OS fingerprinting complete.${NC}\n"

# Step 5: UDP Port Scan (Top 50 Services)
echo -e "${YELLOW}[*] Phase 5: UDP Port Scan (Top 50 UDP services)...${NC}"
nmap -sU --top-ports 50 -v -T4 "${TARGET_IP}" -oN "${OUTPUT_DIR}/05_udp_top_ports_scan.nmap"
echo -e "${GREEN}[+] UDP top ports scan complete.${NC}\n"

# Step 6: Targeted UDP Service Fingerprinting
echo -e "${YELLOW}[*] Phase 6: Targeted UDP Service Version Detection...${NC}"
nmap -sU -sV -p 53,69,111,137,161,2049 "${TARGET_IP}" -oN "${OUTPUT_DIR}/06_udp_service_version_scan.nmap"
echo -e "${GREEN}[+] UDP service version scan complete.${NC}\n"

# Step 7: Nmap Scripting Engine (NSE) Vulnerability Scan
echo -e "${YELLOW}[*] Phase 7: Nmap Scripting Engine (NSE) Vulnerability Audit...${NC}"
nmap --script vuln -p 21,22,23,25,80,139,445,1524,3632,6667 "${TARGET_IP}" -oN "${OUTPUT_DIR}/07_nse_vulnerability_audit.nmap"
echo -e "${GREEN}[+] NSE vulnerability audit complete.${NC}\n"

echo -e "${BLUE}====================================================================${NC}"
echo -e "${GREEN}[✓] Port Security Analysis Completed Successfully!${NC}"
echo -e "Results saved under: ${OUTPUT_DIR}/"
echo -e "${BLUE}====================================================================${NC}"
