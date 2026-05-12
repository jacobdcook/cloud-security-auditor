import json
import os

from fpdf import FPDF
import datetime

from src.finding_utils import strip_code_fence

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
        fix_clean = strip_code_fence(fix)
        
        # For first 3 findings on page 1: limit code to 12 lines max to ensure they all fit
        is_first_page = i <= 3
        if is_first_page:
            fix_lines = fix_clean.split('\n')
            if len(fix_lines) > 12:
                fix_clean = '\n'.join(fix_lines[:12]) + '\n... (truncated for display)'
        
        # Add page break AFTER first 3 findings (so findings 1-3 are on page 1)
        if i == 4:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, txt="Cloud Security Audit Report (continued)", ln=True, align='C')
        
        # Optimize spacing for first page
        if is_first_page:
            pdf.ln(5)  # Less spacing on first page
            pdf.set_font("Arial", "B", 11)  # Slightly smaller font
        else:
            pdf.ln(8)
            pdf.set_font("Arial", "B", 12)
        
        pdf.cell(0, 6, txt=f"Finding #{i}: {issue_name}", ln=True)
        pdf.set_font("Arial", size=9 if is_first_page else 10)
        pdf.multi_cell(0, 5, txt=f"Resource: {resource}\nType: {resource_type}\nSeverity: {severity}")
        pdf.ln(2)
        pdf.set_font("Arial", "B", 9 if is_first_page else 10)
        pdf.cell(0, 5, txt="AI Remediation:", ln=True)
        pdf.set_font("Courier", size=7 if is_first_page else 8)
        # Use proper width (190mm for A4 with margins)
        code_width = 190
        line_height = 3 if is_first_page else 4
        
        # Split long code blocks into smaller chunks for better formatting
        for line in fix_clean.split('\n'):
            # Skip empty lines
            if not line.strip():
                pdf.ln(2)
                continue
            
            # Clean the line (remove any problematic characters)
            line = line.replace('\r', '').strip()
            if not line:
                continue
            
            # Break very long lines (more than 100 chars)
            if len(line) > 100:
                # Break at spaces or special characters
                words = line.split(' ')
                current_line = ""
                for word in words:
                    if len(current_line + word) < 100:
                        current_line += word + " "
                    else:
                        if current_line.strip():
                            try:
                                pdf.multi_cell(code_width, line_height, txt=current_line.strip())
                            except:
                                # If still fails, truncate further
                                pdf.multi_cell(code_width, line_height, txt=current_line.strip()[:90])
                        current_line = word + " "
                if current_line.strip():
                    try:
                        pdf.multi_cell(code_width, line_height, txt=current_line.strip())
                    except:
                        pdf.multi_cell(code_width, line_height, txt=current_line.strip()[:90])
            else:
                # Regular line - truncate if too long
                try:
                    pdf.multi_cell(code_width, line_height, txt=line)
                except:
                    # Fallback: truncate to 90 chars
                    pdf.multi_cell(code_width, line_height, txt=line[:90])
        pdf.ln(1 if is_first_page else 2)

    pdf.output(pdf_path)
    print(f"PDF report generated: {pdf_path}")
