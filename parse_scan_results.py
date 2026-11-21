#!/usr/bin/env python3
"""
Nmap Scan Results Parser & Security Summary Generator
Project: TCP/UDP Port Security Analysis Using Nmap
Organization: Trionix Tech Mini Project
"""

import xml.etree.ElementTree as ET
import os
import sys

def parse_nmap_xml(xml_file):
    if not os.path.exists(xml_file):
        print(f"[-] Error: File not found: {xml_file}")
        return

    tree = ET.parse(xml_file)
    root = tree.getroot()

    print("=" * 80)
    print("        TCP/UDP PORT SECURITY ANALYSIS - SUMMARY AUDIT REPORT")
    print("=" * 80)

    for host in root.findall('host'):
        addr_elem = host.find('address')
        ip_addr = addr_elem.get('addr') if addr_elem is not None else "Unknown"
        status_elem = host.find('status')
        status = status_elem.get('state') if status_elem is not None else "Unknown"
        
        hostname_elem = host.find('hostnames/hostname')
        hostname = hostname_elem.get('name') if hostname_elem is not None else "N/A"

        os_match = host.find('os/osmatch')
        os_name = os_match.get('name') if os_match is not None else "Linux 2.6.X"

        print(f"Target Host      : {ip_addr} ({hostname})")
        print(f"Host Status      : {status.upper()}")
        print(f"Operating System : {os_name}")
        print("-" * 80)
        print(f"{'PORT':<10} {'STATE':<10} {'SERVICE':<15} {'VERSION / DETAILS':<45}")
        print("-" * 80)

        tcp_count = 0
        udp_count = 0

        for port in host.findall('ports/port'):
            proto = port.get('protocol')
            port_id = f"{port.get('portid')}/{proto}"
            state = port.find('state').get('state')
            service_elem = port.find('service')
            
            s_name = service_elem.get('name') if service_elem is not None else "unknown"
            s_prod = service_elem.get('product') if service_elem is not None else ""
            s_ver = service_elem.get('version') if service_elem is not None else ""
            s_extra = service_elem.get('extrainfo') if service_elem is not None else ""

            parts = [p for p in [s_prod, s_ver, s_extra] if p]
            details = " ".join(parts).strip()
            if not details:
                details = "Standard service"

            if proto == 'tcp':
                tcp_count += 1
            else:
                udp_count += 1

            print(f"{port_id:<10} {state:<10} {s_name:<15} {details[:45]:<45}")

        print("-" * 80)
        print(f"Total Open Ports Identified: {tcp_count + udp_count} (TCP: {tcp_count}, UDP: {udp_count})")
        print("=" * 80)

if __name__ == "__main__":
    default_xml = os.path.join(os.path.dirname(__file__), "..", "scans", "full_lab_audit.xml")
    target_file = sys.argv[1] if len(sys.argv) > 1 else default_xml
    parse_nmap_xml(target_file)
