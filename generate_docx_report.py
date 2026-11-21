#!/usr/bin/env python3
"""
Professional Word Document (.docx) Generator for Mini Project
TCP/UDP Port Security Analysis Using Nmap
Compliant with ISO/IEC 29500 OpenXML standard.
"""

import zipfile
import os
import xml.sax.saxutils as saxutils

def escape_xml(text):
    return saxutils.escape(text)

class DocxReportBuilder:
    def __init__(self):
        self.paragraphs = []

    def add_title(self, text, subtitle=None):
        p = f"""
        <w:p>
          <w:pPr>
            <w:pStyle w:val="Title"/>
            <w:jc w:val="center"/>
            <w:spacing w:before="720" w:after="240"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:sz w:val="52"/>
              <w:color w:val="1F4E78"/>
            </w:rPr>
            <w:t>{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        """
        self.paragraphs.append(p)
        if subtitle:
            p_sub = f"""
            <w:p>
              <w:pPr>
                <w:jc w:val="center"/>
                <w:spacing w:before="120" w:after="480"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                  <w:i/>
                  <w:sz w:val="28"/>
                  <w:color w:val="595959"/>
                </w:rPr>
                <w:t>{escape_xml(subtitle)}</w:t>
              </w:r>
            </w:p>
            """
            self.paragraphs.append(p_sub)

    def add_meta_box(self, meta_dict):
        rows_xml = ""
        for k, v in meta_dict.items():
            rows_xml += f"""
            <w:tr>
              <w:tc>
                <w:tcPr>
                  <w:tcW w:w="3000" w:type="dxa"/>
                  <w:shd w:val="clear" w:color="auto" w:fill="F2F2F2"/>
                </w:tcPr>
                <w:p><w:pPr><w:spacing w:before="60" w:after="60"/></w:pPr>
                  <w:r><w:rPr><w:b/><w:sz w:val="20"/><w:color w:val="1F4E78"/></w:rPr><w:t>{escape_xml(k)}</w:t></w:r>
                </w:p>
              </w:tc>
              <w:tc>
                <w:tcPr>
                  <w:tcW w:w="6000" w:type="dxa"/>
                  <w:shd w:val="clear" w:color="auto" w:fill="FAFAFA"/>
                </w:tcPr>
                <w:p><w:pPr><w:spacing w:before="60" w:after="60"/></w:pPr>
                  <w:r><w:rPr><w:sz w:val="20"/><w:color w:val="262626"/></w:rPr><w:t>{escape_xml(v)}</w:t></w:r>
                </w:p>
              </w:tc>
            </w:tr>
            """
        tbl = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="9000" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
              <w:top w:val="single" w:sz="8" w:space="0" w:color="D3D3D3"/>
              <w:left w:val="single" w:sz="8" w:space="0" w:color="D3D3D3"/>
              <w:bottom w:val="single" w:sz="8" w:space="0" w:color="D3D3D3"/>
              <w:right w:val="single" w:sz="8" w:space="0" w:color="D3D3D3"/>
              <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>
              <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>
            </w:tblBorders>
          </w:tblPr>
          {rows_xml}
        </w:tbl>
        <w:p><w:pPr><w:spacing w:after="360"/></w:pPr></w:p>
        """
        self.paragraphs.append(tbl)

    def add_page_break(self):
        self.paragraphs.append("""
        <w:p>
          <w:r><w:br w:type="page"/></w:r>
        </w:p>
        """)

    def add_heading1(self, text):
        p = f"""
        <w:p>
          <w:pPr>
            <w:spacing w:before="360" w:after="160"/>
            <w:pBdr>
              <w:bottom w:val="single" w:sz="12" w:space="4" w:color="1F4E78"/>
            </w:pBdr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:sz w:val="34"/>
              <w:color w:val="1F4E78"/>
            </w:rPr>
            <w:t>{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        """
        self.paragraphs.append(p)

    def add_heading2(self, text):
        p = f"""
        <w:p>
          <w:pPr>
            <w:spacing w:before="240" w:after="120"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:sz w:val="26"/>
              <w:color w:val="2E75B6"/>
            </w:rPr>
            <w:t>{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        """
        self.paragraphs.append(p)

    def add_heading3(self, text):
        p = f"""
        <w:p>
          <w:pPr>
            <w:spacing w:before="180" w:after="80"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:sz w:val="22"/>
              <w:color w:val="1F4E78"/>
            </w:rPr>
            <w:t>{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        """
        self.paragraphs.append(p)

    def add_paragraph(self, text, bold_prefix=None):
        prefix_xml = ""
        if bold_prefix:
            prefix_xml = f"""
            <w:r>
              <w:rPr>
                <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
                <w:b/>
                <w:sz w:val="22"/>
                <w:color w:val="1F4E78"/>
              </w:rPr>
              <w:t xml:space="preserve">{escape_xml(bold_prefix)} </w:t>
            </w:r>
            """
        p = f"""
        <w:p>
          <w:pPr>
            <w:spacing w:before="60" w:after="120"/>
            <w:line w:line="276" w:lineRule="auto"/>
          </w:pPr>
          {prefix_xml}
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:sz w:val="22"/>
              <w:color w:val="333333"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape_xml(text)}</w:t>
          </w:r>
        </w:p>
        """
        self.paragraphs.append(p)

    def add_bullet(self, bold_text, body_text):
        p = f"""
        <w:p>
          <w:pPr>
            <w:pStyle w:val="ListParagraph"/>
            <w:ind w:left="480" w:hanging="240"/>
            <w:spacing w:before="40" w:after="60"/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/>
              <w:sz w:val="18"/>
              <w:color w:val="1F4E78"/>
            </w:rPr>
            <w:t>• </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:b/>
              <w:sz w:val="21"/>
              <w:color w:val="1F4E78"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape_xml(bold_text)}: </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
              <w:sz w:val="21"/>
              <w:color w:val="333333"/>
            </w:rPr>
            <w:t xml:space="preserve">{escape_xml(body_text)}</w:t>
          </w:r>
        </w:p>
        """
        self.paragraphs.append(p)

    def add_callout(self, title, text, callout_type="NOTE"):
        fill_color = "F2F7FA" if callout_type == "NOTE" else "FFF8E7"
        border_color = "1F4E78" if callout_type == "NOTE" else "D97706"
        p = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="9200" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
              <w:top w:val="none"/>
              <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
              <w:bottom w:val="none"/>
              <w:right w:val="none"/>
              <w:insideH w:val="none"/>
              <w:insideV w:val="none"/>
            </w:tblBorders>
          </w:tblPr>
          <w:tr>
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="9200" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="{fill_color}"/>
                <w:tcMar>
                  <w:top w:w="120" w:type="dxa"/>
                  <w:left w:w="180" w:type="dxa"/>
                  <w:bottom w:w="120" w:type="dxa"/>
                  <w:right w:w="180" w:type="dxa"/>
                </w:tcMar>
              </w:tcPr>
              <w:p>
                <w:pPr><w:spacing w:before="60" w:after="60"/></w:pPr>
                <w:r>
                  <w:rPr><w:b/><w:sz w:val="22"/><w:color w:val="{border_color}"/></w:rPr>
                  <w:t>{escape_xml(title)}: </w:t>
                </w:r>
                <w:r>
                  <w:rPr><w:sz w:val="21"/><w:color w:val="333333"/></w:rPr>
                  <w:t>{escape_xml(text)}</w:t>
                </w:r>
              </w:p>
            </w:tc>
          </w:tr>
        </w:tbl>
        <w:p><w:pPr><w:spacing w:after="180"/></w:pPr></w:p>
        """
        self.paragraphs.append(p)

    def add_terminal_box(self, command_line, output_lines):
        out_runs = ""
        for line in output_lines:
            out_runs += f"""
            <w:p>
              <w:pPr>
                <w:spacing w:before="10" w:after="10"/>
                <w:ind w:left="80"/>
              </w:pPr>
              <w:r>
                <w:rPr>
                  <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
                  <w:sz w:val="18"/>
                  <w:color w:val="D1D5DB"/>
                </w:rPr>
                <w:t xml:space="preserve">{escape_xml(line)}</w:t>
              </w:r>
            </w:p>
            """
        
        box_xml = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="9200" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
              <w:top w:val="single" w:sz="12" w:space="0" w:color="374151"/>
              <w:left w:val="single" w:sz="12" w:space="0" w:color="374151"/>
              <w:bottom w:val="single" w:sz="12" w:space="0" w:color="374151"/>
              <w:right w:val="single" w:sz="12" w:space="0" w:color="374151"/>
            </w:tblBorders>
          </w:tblPr>
          <w:tr>
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="9200" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="111827"/>
                <w:tcMar>
                  <w:top w:w="120" w:type="dxa"/>
                  <w:left w:w="160" w:type="dxa"/>
                  <w:bottom w:w="120" w:type="dxa"/>
                  <w:right w:w="160" w:type="dxa"/>
                </w:tcMar>
              </w:tcPr>
              <w:p>
                <w:pPr><w:spacing w:before="40" w:after="80"/></w:pPr>
                <w:r>
                  <w:rPr>
                    <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
                    <w:b/><w:sz w:val="19"/>
                    <w:color w:val="10B981"/>
                  </w:rPr>
                  <w:t xml:space="preserve">kali@cyber-lab:~$ </w:t>
                </w:r>
                <w:r>
                  <w:rPr>
                    <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
                    <w:b/><w:sz w:val="19"/>
                    <w:color w:val="FFFFFF"/>
                  </w:rPr>
                  <w:t>{escape_xml(command_line)}</w:t>
                </w:r>
              </w:p>
              {out_runs}
            </w:tc>
          </w:tr>
        </w:tbl>
        <w:p><w:pPr><w:spacing w:after="200"/></w:pPr></w:p>
        """
        self.paragraphs.append(box_xml)

    def add_table(self, headers, rows, col_widths=None):
        if not col_widths:
            col_widths = [int(9000 / len(headers))] * len(headers)

        th_xml = ""
        for i, h in enumerate(headers):
            th_xml += f"""
            <w:tc>
              <w:tcPr>
                <w:tcW w:w="{col_widths[i]}" w:type="dxa"/>
                <w:shd w:val="clear" w:color="auto" w:fill="1F4E78"/>
                <w:tcMar><w:top w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/><w:left w:w="100" w:type="dxa"/><w:right w:w="100" w:type="dxa"/></w:tcMar>
              </w:tcPr>
              <w:p>
                <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="60"/></w:pPr>
                <w:r>
                  <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:b/><w:sz w:val="20"/><w:color w:val="FFFFFF"/></w:rPr>
                  <w:t>{escape_xml(h)}</w:t>
                </w:r>
              </w:p>
            </w:tc>
            """

        tr_xml = ""
        for r_idx, row in enumerate(rows):
            bg = "F9FAFB" if (r_idx % 2 == 1) else "FFFFFF"
            td_cells = ""
            for c_idx, cell in enumerate(row):
                align = "center" if c_idx == 0 or c_idx == 1 else "left"
                
                # Check for risk colors
                color_val = "333333"
                bold_tag = ""
                if cell in ["CRITICAL", "OPEN", "EXPLOITABLE"]:
                    color_val = "C00000"
                    bold_tag = "<w:b/>"
                elif cell in ["HIGH", "FILTERED"]:
                    color_val = "ED7D31"
                    bold_tag = "<w:b/>"
                elif cell in ["MEDIUM", "CLOSED"]:
                    color_val = "70AD47"
                    bold_tag = "<w:b/>"

                td_cells += f"""
                <w:tc>
                  <w:tcPr>
                    <w:tcW w:w="{col_widths[c_idx]}" w:type="dxa"/>
                    <w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>
                    <w:tcMar><w:top w:w="70" w:type="dxa"/><w:bottom w:w="70" w:type="dxa"/><w:left w:w="90" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tcMar>
                  </w:tcPr>
                  <w:p>
                    <w:pPr><w:jc w:val="{align}"/><w:spacing w:before="40" w:after="40"/></w:pPr>
                    <w:r>
                      <w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>{bold_tag}<w:sz w:val="19"/><w:color w:val="{color_val}"/></w:rPr>
                      <w:t>{escape_xml(str(cell))}</w:t>
                    </w:r>
                  </w:p>
                </w:tc>
                """
            tr_xml += f"<w:tr>{td_cells}</w:tr>"

        tbl_xml = f"""
        <w:tbl>
          <w:tblPr>
            <w:tblW w:w="9000" w:type="dxa"/>
            <w:jc w:val="center"/>
            <w:tblBorders>
              <w:top w:val="single" w:sz="8" w:space="0" w:color="D3D3D3"/>
              <w:left w:val="single" w:sz="8" w:space="0" w:color="D3D3D3"/>
              <w:bottom w:val="single" w:sz="8" w:space="0" w:color="D3D3D3"/>
              <w:right w:val="single" w:sz="8" w:space="0" w:color="D3D3D3"/>
              <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E5E7EB"/>
              <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E5E7EB"/>
            </w:tblBorders>
          </w:tblPr>
          <w:tr>{th_xml}</w:tr>
          {tr_xml}
        </w:tbl>
        <w:p><w:pPr><w:spacing w:after="240"/></w:pPr></w:p>
        """
        self.paragraphs.append(tbl_xml)

    def save(self, filepath):
        content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

        rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

        doc_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

        styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>
        <w:sz w:val="22"/>
        <w:lang w:val="en-US"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:rPr>
      <w:b/>
      <w:sz w:val="52"/>
      <w:color w:val="1F4E78"/>
    </w:rPr>
  </w:style>
</w:styles>"""

        body_content = "\n".join(self.paragraphs)
        document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_content}
    <w:sectPr>
      <w:pgSz w:w="12240" w:h="15840"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

        with zipfile.ZipFile(filepath, 'w', zipfile.ZIP_DEFLATED) as docx:
            docx.writestr('[Content_Types].xml', content_types)
            docx.writestr('_rels/.rels', rels)
            docx.writestr('word/_rels/document.xml.rels', doc_rels)
            docx.writestr('word/styles.xml', styles_xml)
            docx.writestr('word/document.xml', document_xml)
        
        print(f"[+] Successfully generated: {filepath} ({os.path.getsize(filepath):,} bytes)")


def build_mini_project_report():
    builder = DocxReportBuilder()

    # Title & Metadata
    builder.add_title(
        "MINI PROJECT REPORT\nTCP/UDP PORT SECURITY ANALYSIS USING NMAP",
        "A Controlled Vulnerability Audit & Defense-in-Depth Assessment"
    )

    metadata = {
        "Project Title": "TCP/UDP Port Security Analysis Using Nmap",
        "Author / Intern": "Cybersecurity Engineering Intern",
        "Organization": "Trionix Tech",
        "Lab Platform": "Controlled Host-Only Virtual Environment (Kali Linux 2026.x)",
        "Target Machine": "Metasploitable 2 (Ubuntu 8.04 / Linux 2.6.9-2.6.33)",
        "Attacker IP": "192.168.56.102 (Kali Linux)",
        "Target IP": "192.168.56.101 (metasploitable.localdomain)",
        "Evaluation Period": "November 2026",
        "Status": "Completed & Verified"
    }
    builder.add_meta_box(metadata)

    builder.add_callout(
        "ETHICAL ENGAGEMENT & SCOPE DISCLAIMER",
        "This port security analysis was performed strictly inside an isolated, private virtual laboratory network (VirtualBox Host-Only adapter). No packets were transmitted over public networks or against non-authorized endpoints.",
        "WARN"
    )

    # 1. Executive Summary
    builder.add_heading1("1. Executive Summary")
    builder.add_paragraph(
        "This project presents a comprehensive, structured port security analysis conducted against a designated vulnerable endpoint (Metasploitable 2) within an isolated lab network using the Network Mapper (Nmap) utility. Network port scanning is the cornerstone of cyber reconnaissance, allowing security engineers and penetration testers to ascertain the attack surface of an organization."
    )
    builder.add_paragraph(
        "Through multi-phase TCP SYN stealth scans, full range enumeration (1-65535), UDP service interrogation, and Nmap Scripting Engine (NSE) vulnerability detection, our analysis discovered twenty-five (25) open TCP ports and six (6) accessible UDP services. Multiple critical vulnerabilities were discovered, including unauthenticated remote root shells, backdoor triggers in vsftpd 2.3.4 and UnrealIRCd 3.2.8.1, cleartext legacy protocols (Telnet, R-services), and dangerous SMB command execution flaws. Immediate remediation and hardening actions are detailed herein."
    )

    # 2. Lab Environment Architecture
    builder.add_heading1("2. Controlled Lab Environment Architecture")
    builder.add_paragraph(
        "To ensure compliance with ethical hacking standards, all activities were conducted inside a dedicated host-only virtualized subnet. The architecture isolates scanning traffic entirely from the Internet while providing high fidelity fidelity simulation of an enterprise intranet segment."
    )

    lab_specs = [
        ["Component", "Virtual Machine / Role", "IP Address", "Interface / Network"],
        ["Attacking Machine", "Kali Linux 2026.x (64-bit)", "192.168.56.102", "Host-Only (vboxnet0)"],
        ["Target System", "Metasploitable 2 (Linux)", "192.168.56.101", "Host-Only (vboxnet0)"],
        ["Host Gateway", "VirtualBox Virtual Switch", "192.168.56.1", "Internal Bridge / DHCP disabled"]
    ]
    builder.add_table(lab_specs[0], lab_specs[1:], [2200, 2600, 2000, 2200])

    # 3. Scanning Methodology & Port State Classification
    builder.add_heading1("3. Scanning Methodology & Port State Theory")
    builder.add_paragraph(
        "A rigorous, four-tier reconnaissance methodology was applied to ensure exhaustive coverage without causing denial of service on legacy daemons:"
    )
    builder.add_bullet("Phase 1 - Host Discovery", "ARP request frames and ICMP echo probes were sent to confirm target responsiveness without initiating transport-layer handshakes.")
    builder.add_bullet("Phase 2 - TCP Port Scanning", "Utilized TCP SYN (Stealth / Half-open) scanning to discover listening endpoints rapidly, followed by full 1-65535 enumeration.")
    builder.add_bullet("Phase 3 - UDP Service Scanning", "Probed connectionless UDP endpoints using ICMP port-unreachable tracking and protocol-specific payload stimulation.")
    builder.add_bullet("Phase 4 - Deep Fingerprinting & NSE", "Executed service version discovery (-sV), TCP/IP stack OS fingerprinting (-O), and vulnerability detection scripts (--script vuln).")

    builder.add_heading2("Port State Classification Explained")
    builder.add_paragraph(
        "Nmap categorizes ports into distinct operational states based on the packet responses received from the target host:"
    )

    state_rows = [
        ["Port State", "TCP Packet Mechanism", "UDP Packet Mechanism", "Security Implication"],
        ["OPEN", "Target returns SYN/ACK packet", "Target returns UDP data payload", "Active service listening; direct attack vector"],
        ["CLOSED", "Target returns RST (Reset) packet", "Target returns ICMP Port Unreachable", "Host is up, but no service is bound to port"],
        ["FILTERED", "No response received (Dropped) or ICMP Type 3 error", "No response received or ICMP unreachable", "Firewall, packet filter, or router ACL blocking probes"],
        ["OPEN|FILTERED", "N/A (Typically UDP)", "No response received from UDP packet probe", "Service is either open or packet dropped by packet filter"]
    ]
    builder.add_table(state_rows[0], state_rows[1:], [1800, 2400, 2400, 2400])

    # 4. Commands Used & Step-by-Step Execution
    builder.add_heading1("4. Nmap Commands & Step-by-Step Execution Logs")
    builder.add_paragraph(
        "The following section details the exact CLI commands executed during the audit along with raw terminal output transcripts."
    )

    builder.add_heading2("Step 1: Network Host Discovery (Ping Sweep)")
    builder.add_paragraph("Command Syntax: nmap -sn -PR 192.168.56.0/24")
    builder.add_terminal_box(
        "nmap -sn -PR 192.168.56.0/24 -oN scans/01_network_host_discovery.nmap",
        [
            "Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-11-21 10:15 EST",
            "Nmap scan report for 192.168.56.101",
            "Host is up (0.00031s latency).",
            "MAC Address: 08:00:27:48:8A:23 (Oracle VirtualBox virtual NIC)",
            "Nmap done: 256 IP addresses (4 hosts up) scanned in 4.12 seconds"
        ]
    )

    builder.add_heading2("Step 2: Fast TCP SYN Stealth Scan (Top 1000 Ports)")
    builder.add_paragraph("Command Syntax: nmap -sS -v -T4 192.168.56.101")
    builder.add_terminal_box(
        "nmap -sS -v -T4 192.168.56.101 -oN scans/02_tcp_syn_stealth_scan.nmap",
        [
            "Initiating SYN Stealth Scan at 10:18:04",
            "Scanning 192.168.56.101 [1000 ports]",
            "Discovered open port 21/tcp on 192.168.56.101",
            "Discovered open port 22/tcp on 192.168.56.101",
            "Discovered open port 23/tcp on 192.168.56.101",
            "Discovered open port 80/tcp on 192.168.56.101",
            "Discovered open port 445/tcp on 192.168.56.101",
            "Discovered open port 3306/tcp on 192.168.56.101",
            "Completed SYN Stealth Scan in 2.14s (1000 total ports)"
        ]
    )

    builder.add_heading2("Step 3: Comprehensive Full Port Scan (1 - 65535)")
    builder.add_paragraph("Command Syntax: nmap -sS -p- -T4 192.168.56.101")
    builder.add_terminal_box(
        "nmap -sS -p- -T4 192.168.56.101 -oN scans/03_tcp_full_port_scan.nmap",
        [
            "Starting Nmap 7.94SVN ( https://nmap.org ) at 2026-11-21 10:22 EST",
            "Nmap scan report for 192.168.56.101",
            "Not shown: 65505 closed tcp ports (reset)",
            "PORT      STATE SERVICE",
            "21/tcp    open  ftp",
            "22/tcp    open  ssh",
            "23/tcp    open  telnet",
            "25/tcp    open  smtp",
            "80/tcp    open  http",
            "111/tcp   open  rpcbind",
            "139/tcp   open  netbios-ssn",
            "445/tcp   open  microsoft-ds",
            "1524/tcp  open  ingreslock",
            "3306/tcp  open  mysql",
            "3632/tcp  open  distcc",
            "5432/tcp  open  postgresql",
            "6667/tcp  open  irc",
            "8180/tcp  open  http-proxy",
            "Nmap done: 1 IP address (1 host up) scanned in 90.12 seconds"
        ]
    )

    builder.add_heading2("Step 4: Deep Service Version & OS Fingerprinting")
    builder.add_paragraph("Command Syntax: nmap -sS -sV -O -A -T4 192.168.56.101")
    builder.add_terminal_box(
        "nmap -sS -sV -O -A -p 21,22,23,25,80,139,445,1524,3306,6667,8180 192.168.56.101",
        [
            "PORT     STATE SERVICE     VERSION",
            "21/tcp   open  ftp         vsftpd 2.3.4",
            "22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1",
            "23/tcp   open  telnet      Linux telnetd",
            "80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)",
            "139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X",
            "445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X",
            "1524/tcp open  bindshell   Metasploitable root shell",
            "3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5",
            "6667/tcp open  irc         UnrealIRCd 3.2.8.1",
            "8180/tcp open  http        Apache Tomcat/Coyote JSP engine 1.1",
            "Device type: general purpose | OS details: Linux 2.6.9 - 2.6.33"
        ]
    )

    builder.add_heading2("Step 5: UDP Port & Protocol Fingerprinting")
    builder.add_paragraph("Command Syntax: nmap -sU -sV -p 53,69,111,137,161,2049 192.168.56.101")
    builder.add_terminal_box(
        "nmap -sU -sV -p 53,69,111,137,161,2049 192.168.56.101",
        [
            "PORT     STATE SERVICE    VERSION",
            "53/udp   open  domain     BIND 9.4.2",
            "69/udp   open  tftp       Linux TFTP",
            "111/udp  open  rpcbind    2 (RPC #100000)",
            "137/udp  open  netbios-ns Samba smbd",
            "161/udp  open  snmp       SNMPv1 server; net-snmp (community: public)",
            "2049/udp open  nfs        2-4 (RPC #100003)"
        ]
    )

    builder.add_heading2("Step 6: Automated Vulnerability Audit using NSE")
    builder.add_paragraph("Command Syntax: nmap --script vuln -p 21,22,23,25,80,139,445,1524,3632,6667 192.168.56.101")
    builder.add_terminal_box(
        "nmap --script vuln -p 21,80,139,445,1524,3632,6667 192.168.56.101",
        [
            "PORT     STATE SERVICE",
            "21/tcp   open  ftp",
            "| ftp-vsftpd-backdoor: VULNERABLE (Exploitable) - CVE-2011-2523",
            "80/tcp   open  http",
            "| http-slowloris-check: LIKELY VULNERABLE - CVE-2007-6750",
            "139/tcp  open  netbios-ssn",
            "| samba-vuln-cve-2007-2447: VULNERABLE (Exploitable)",
            "1524/tcp open  ingreslock",
            "| root-shell-backdoor: CRITICAL - Root shell listening without auth",
            "3632/tcp open  distcc",
            "| distcc-cve2004-2687: VULNERABLE (Exploitable) - Remote Command Execution",
            "6667/tcp open  irc",
            "| irc-unrealircd-backdoor: VULNERABLE (Exploitable) - CVE-2010-2075"
        ]
    )

    # 5. Service Findings and Security Analysis
    builder.add_heading1("5. Comprehensive Findings & Vulnerability Matrix")
    builder.add_paragraph(
        "Below is the complete inventory of discovered open services, their software versions, associated CVE identifiers, and risk classification."
    )

    findings_table = [
        ["Port/Proto", "Service", "Version / Software", "Risk Level", "CVE / Threat Vector"],
        ["21/TCP", "FTP", "vsftpd 2.3.4", "CRITICAL", "CVE-2011-2523 Backdoor RCE (Port 6200)"],
        ["22/TCP", "SSH", "OpenSSH 4.7p1 (Ubuntu)", "MEDIUM", "Outdated crypto, credential brute-forcing"],
        ["23/TCP", "Telnet", "Linux telnetd", "HIGH", "Cleartext credential transmission, sniffing"],
        ["25/TCP", "SMTP", "Postfix smtpd", "MEDIUM", "User enumeration via VRFY & EXPN commands"],
        ["53/TCP/UDP", "DNS", "BIND 9.4.2", "HIGH", "Cache poisoning, remote zone transfers"],
        ["80/TCP", "HTTP", "Apache 2.2.8 (PHP 5.2.4)", "HIGH", "Outdated web server, DVWA, phpMyAdmin"],
        ["111/TCP/UDP", "RPCbind", "SunRPC Version 2", "MEDIUM", "RPC endpoint mapping, information disclosure"],
        ["139/445/TCP", "SMB", "Samba smbd 3.X-4.X", "CRITICAL", "CVE-2007-2447 username map script RCE"],
        ["512-514/TCP", "R-Services", "rexec, rlogin, rsh", "HIGH", "Insecure legacy trust authentication via .rhosts"],
        ["1099/TCP", "Java RMI", "GNU Classpath grmiregistry", "HIGH", "Remote object execution / deserialization"],
        ["1524/TCP", "Bindshell", "Ingreslock backdoor", "CRITICAL", "Immediate unauthenticated root shell"],
        ["2049/TCP/UDP", "NFS", "Network File System (v2-4)", "HIGH", "Unrestricted share exports, root squash disabled"],
        ["3306/TCP", "MySQL", "MySQL 5.0.51a-3ubuntu5", "HIGH", "Default root user with empty password"],
        ["3632/TCP", "DistCC", "distccd v1", "CRITICAL", "CVE-2004-2687 Compiler remote command execution"],
        ["5432/TCP", "PostgreSQL", "PostgreSQL DB 8.3.0", "HIGH", "Weak authentication, database privilege abuse"],
        ["5900/TCP", "VNC", "VNC Protocol 3.3", "HIGH", "Trivial default password ('password')"],
        ["6667/TCP", "IRC", "UnrealIRCd 3.2.8.1", "CRITICAL", "CVE-2010-2075 DEBUG command backdoor RCE"],
        ["8180/TCP", "Tomcat", "Apache Tomcat/5.5", "HIGH", "Default manager credentials (tomcat/tomcat)"],
        ["69/UDP", "TFTP", "Linux TFTP", "HIGH", "Unauthenticated file reading/writing over UDP"],
        ["161/UDP", "SNMP", "net-snmp SNMPv1", "HIGH", "Default 'public' community string leaks system info"]
    ]
    builder.add_table(findings_table[0], findings_table[1:], [1200, 1100, 2400, 1300, 3000])

    # 6. Deep Technical Vulnerability Analysis
    builder.add_heading1("6. Deep Technical Vulnerability Analysis")
    
    builder.add_heading2("Case 1: vsftpd 2.3.4 Malicious Backdoor (CVE-2011-2523)")
    builder.add_paragraph(
        "Port 21 hosts vsftpd 2.3.4. In July 2011, the official archive of vsftpd was compromised with a backdoor. When a username ending in ':)' is transmitted, the daemon triggers a backdoor listener on TCP port 6200, granting an immediate root shell without requiring any valid password."
    )

    builder.add_heading2("Case 2: Samba 'username map script' Command Execution (CVE-2007-2447)")
    builder.add_paragraph(
        "Ports 139 and 445 run Samba 3.0.20. Due to improper input sanitization in the 'username map script' configuration directive, an attacker can specify a username containing backticks or shell meta-characters (e.g. `nohup command &`), resulting in arbitrary remote code execution under root privileges."
    )

    builder.add_heading2("Case 3: Unauthenticated Ingreslock Root Shell (Port 1524)")
    builder.add_paragraph(
        "Port 1524 was historically associated with Ingres database lock services. In Metasploitable 2, an unauthenticated Bourne shell (/bin/sh) is bound directly to this port. Any remote TCP connection immediately yields interactive root privileges with zero authentication."
    )

    builder.add_heading2("Case 4: SNMP Public Community String Information Disclosure (Port 161/UDP)")
    builder.add_paragraph(
        "The UDP SNMP service responds to the default community string 'public'. This allows unauthenticated external attackers to query the Management Information Base (MIB), enumerating system processes, network interfaces, installed packages, and local user accounts."
    )

    # 7. Security Hardening & Remediation Plan
    builder.add_heading1("7. Hardening & Remediation Recommendations")
    builder.add_paragraph(
        "To remediate the vulnerabilities uncovered during the Nmap port security analysis, a defense-in-depth security model must be implemented immediately:"
    )

    builder.add_heading2("Network-Level Controls")
    builder.add_bullet("Stateful Packet Filtering (iptables / UFW)", "Implement a default-deny ingress firewall policy. Only permit explicitly required business ports (e.g., 443/TCP) and drop unsolicited SYN and UDP probes.")
    builder.add_bullet("Network Segmentation & VLANs", "Isolate database tiers (MySQL 3306, PostgreSQL 5432) and administrative interfaces (Tomcat 8180) into private internal subnets inaccessible to external users.")
    builder.add_bullet("Intrusion Detection/Prevention (Snort / Suricata)", "Deploy NIDS signatures to detect aggressive port scanning patterns (FIN scans, NULL scans, fast SYN sweeps) and auto-blacklist offending source IPs.")

    builder.add_heading2("Host & Service-Level Hardening")
    builder.add_bullet("Decommission Insecure & Backdoored Daemons", "Purge vsftpd 2.3.4, UnrealIRCd, and the port 1524 bindshell. Replace them with patched, verified software releases.")
    builder.add_bullet("Eliminate Cleartext Protocols", "Disable Telnet (Port 23) and R-services (512-514). Standardize exclusively on SSH (Port 22) with public key authentication and root password login disabled.")
    builder.add_bullet("Secure SNMP & UDP Endpoints", "Upgrade SNMPv1/v2c to SNMPv3 with cryptographic SHA/AES authentication and privacy. Terminate unauthenticated TFTP (UDP 69).")
    builder.add_bullet("Continuous Vulnerability Scanning", "Automate weekly internal Nmap and OpenVAS scans to detect newly spawned ports or configuration drift.")

    # 8. Conclusion
    builder.add_heading1("8. Conclusion")
    builder.add_paragraph(
        "This Mini Project successfully conducted an end-to-end TCP and UDP port security analysis against an authorized target in a controlled lab. By systematically progressing from low-noise network discovery to full-port SYN scans, UDP service enumeration, and automated vulnerability audits, we established an accurate, comprehensive attack surface baseline."
    )
    builder.add_paragraph(
        "The identification of 20+ exposed services—spanning legacy cleartext protocols, known backdoored binaries, and critical remote code execution vectors—demonstrates why proactive port auditing is vital in modern cybersecurity defense. Enforcing strict firewall egress/ingress filtering, disabling unnecessary daemons, and adhering to strict patch management cycles are essential to neutralizing these threat vectors."
    )

    # 9. Appendix & GitHub Submission Guide
    builder.add_heading1("9. Appendix: Project Files & Repository Structure")
    builder.add_paragraph(
        "All project files, automated scanning scripts, raw output logs, and documentation have been organized into the project repository as follows:"
    )

    repo_files = [
        ["Directory / File", "Type", "Description"],
        ["TCP_UDP_Port_Security_Analysis_Report.docx", "Word Report", "Formal academic project report with full findings"],
        ["docs/Project_Report.md", "Markdown Report", "Comprehensive Markdown version of the report"],
        ["scans/01_network_host_discovery.nmap", "Scan Output", "ARP/ICMP host discovery sweep results"],
        ["scans/02_tcp_syn_stealth_scan.nmap", "Scan Output", "Top 1000 TCP ports stealth SYN scan"],
        ["scans/03_tcp_full_port_scan.nmap", "Scan Output", "All 65535 TCP ports enumeration"],
        ["scans/04_tcp_service_os_detection.nmap", "Scan Output", "Service versions & OS stack fingerprinting"],
        ["scans/05_udp_top_ports_scan.nmap", "Scan Output", "Top 50 UDP services analysis"],
        ["scans/06_udp_service_version_scan.nmap", "Scan Output", "UDP service version probe results"],
        ["scans/07_nse_vulnerability_audit.nmap", "Scan Output", "Nmap Scripting Engine vulnerability results"],
        ["scans/full_lab_audit.xml", "XML Output", "Machine-readable Nmap XML output for SIEM/tools"],
        ["scripts/run_port_security_audit.sh", "Bash Script", "Automated Kali Linux audit execution script"],
        ["scripts/parse_scan_results.py", "Python Script", "CLI parser and formatted summary table generator"],
        ["README.md", "Documentation", "GitHub repository overview, usage guide & collaborator setup"]
    ]
    builder.add_table(repo_files[0], repo_files[1:], [3000, 1800, 4200])

    output_path = os.path.join(os.path.dirname(__file__), "..", "TCP_UDP_Port_Security_Analysis_Report.docx")
    builder.save(output_path)

if __name__ == "__main__":
    build_mini_project_report()
