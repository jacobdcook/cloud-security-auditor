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

    for i, entry in enumerate(results, 1):
        finding = entry["finding"]
        fix = entry["fix"]
        
        # Extract issue name (check_name from Checkov findings)
        issue_name = finding.get('check_name', finding.get('issue', 'Security Issue'))
        
        # Extract resource name
        resource = finding.get('resource', 'N/A')
        
        # Extract resource type from resource name (e.g., "azurerm_storage_account" from "azurerm_storage_account.insecure_storage")
        resource_type = resource.split('.')[0] if '.' in resource else 'N/A'
        
        # Extract severity if available
        severity = finding.get('severity', 'Medium')  # Default to Medium if not specified
        
        # Clean up the fix code (remove markdown code blocks)
        fix_clean = fix
        if fix_clean.startswith('```'):
            # Remove markdown code block markers
            lines = fix_clean.split('\n')
            # Remove first line (```hcl or ```terraform)
            if lines[0].startswith('```'):
                lines = lines[1:]
            # Remove last line if it's just ```
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            fix_clean = '\n'.join(lines)
        
        # Add page break if needed (every 3 findings or if content is getting long)
        if i > 1 and i % 3 == 1:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="Cloud Security Audit Report (continued)", ln=True, align='C')
        
        pdf.ln(8)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, txt=f"Finding #{i}: {issue_name}", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 6, txt=f"Resource: {resource}\nType: {resource_type}\nSeverity: {severity}")
        pdf.ln(3)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, txt="AI Remediation:", ln=True)
        pdf.set_font("Courier", size=8)
        # Split long code blocks into smaller chunks for better formatting
        for line in fix_clean.split('\n'):
            if len(line) > 80:
                # Break long lines
                words = line.split(' ')
                current_line = ""
                for word in words:
                    if len(current_line + word) < 80:
                        current_line += word + " "
                    else:
                        if current_line:
                            pdf.multi_cell(0, 4, txt=current_line.strip())
                        current_line = word + " "
                if current_line:
                    pdf.multi_cell(0, 4, txt=current_line.strip())
            else:
                pdf.multi_cell(0, 4, txt=line)
        pdf.ln(2)

    pdf.output(pdf_path)
    print(f"PDF report generated: {pdf_path}")
