import json
import os
from fpdf import FPDF
import datetime

def generate_report(results):
    """
    Generates JSON and PDF reports.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("reports", exist_ok=True)

    # 1. JSON Report
    json_path = f"reports/security_audit_{timestamp}.json"
    with open(json_path, "w") as f:
        json.dump(results, f, indent=4)
    print(f"JSON report generated: {json_path}")

    # 2. PDF Report
    pdf_path = f"reports/security_audit_{timestamp}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Cloud Security Audit Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')

    for entry in results:
        pdf.ln(10)
        finding = entry["finding"]
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, txt=f"Issue: {finding.get('issue', 'N/A')}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, txt=f"Resource: {finding.get('resource', 'N/A')}\nType: {finding.get('type', 'N/A')}\nSeverity: {finding.get('severity', 'N/A')}")
        pdf.ln(2)
        pdf.set_font("Arial", "I", 10)
        pdf.multi_cell(0, 10, txt=f"AI Remediation:\n{entry['fix']}")

    pdf.output(pdf_path)
    print(f"PDF report generated: {pdf_path}")
