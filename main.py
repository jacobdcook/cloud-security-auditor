import os
import argparse
from dotenv import load_dotenv
from src.scanner import scan_terraform
from src.auditor import audit_azure
from src.remediator import get_remediation
from src.reporter import generate_report

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Cloud Infrastructure Security Auditor")
    parser.add_argument("--path", type=str, help="Path to Terraform files", default="./terraform")
    parser.add_argument("--azure", action="store_true", help="Run dynamic Azure audit")
    args = parser.parse_args()

    print("🚀 Starting Cloud Security Audit...")

    # 1. Static Analysis
    print("\n🔍 Running Static Analysis on Terraform files...")
    static_results = scan_terraform(args.path)
    
    # 2. Dynamic Auditing (Optional)
    dynamic_results = []
    if args.azure:
        print("\n🌐 Running Dynamic Azure Audit...")
        dynamic_results = audit_azure()

    # 3. AI Remediation
    print("\n🤖 Generating AI Remediation suggestions...")
    all_findings = static_results + dynamic_results
    
    if not all_findings:
        print("No findings to remediate.")
        remediations = []
    else:
        print(f"Found {len(all_findings)} security issues. Generating fixes...\n")
        remediations = []
        for i, finding in enumerate(all_findings, 1):
            # Extract issue name for display
            issue_name = finding.get("check_name", "Security Issue")
            if isinstance(finding, dict):
                issue_name = finding.get("check_name", finding.get("issue", "Security Issue"))
            
            print(f"[{i}/{len(all_findings)}] Issue: {issue_name}")
            print(f"   Resource: {finding.get('resource', 'N/A')}")
            fix = get_remediation(finding)
            remediations.append({"finding": finding, "fix": fix})
            
            # Print the remediation
            print(f"   AI Remediation:")
            print(f"   {fix}")
            print()  # Blank line between findings

    # 4. Reporting
    print("\n📊 Generating Security Report...")
    generate_report(remediations)

    # 5. Security Posture Summary
    print("\n🛡️  Security Posture Summary:")
    print("----------------------------")
    
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
    for entry in remediations:
        finding = entry["finding"]
        severity = str(finding.get("severity", "MEDIUM")).upper()
        if severity in severity_counts:
            severity_counts[severity] += 1
        else:
            severity_counts["UNKNOWN"] += 1
            
    print(f"🔴 Critical: {severity_counts['CRITICAL']}")
    print(f"🟠 High:     {severity_counts['HIGH']}")
    print(f"🟡 Medium:   {severity_counts['MEDIUM']}")
    print(f"🔵 Low:      {severity_counts['LOW']}")
    
    total = len(remediations)
    if total > 0:
        print(f"\nTotal findings: {total}")
        print("Recommendation: Address Critical and High issues immediately.")
    else:
        print("\n✅ No security issues found. Great job!")

    print("\n✅ Audit complete! Check the reports directory.")

if __name__ == "__main__":
    main()
