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
    remediations = []
    for finding in all_findings:
        fix = get_remediation(finding)
        remediations.append({"finding": finding, "fix": fix})

    # 4. Reporting
    print("\n📊 Generating Security Report...")
    generate_report(remediations)

    print("\n✅ Audit complete! Check the reports directory.")

if __name__ == "__main__":
    main()
