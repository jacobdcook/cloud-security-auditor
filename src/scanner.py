import subprocess
import json

def scan_terraform(path):
    """
    Runs Checkov on the specified path and returns findings.
    """
    print(f"Scanning HCL files in {path}...")
    try:
        # Running checkov via subprocess
        result = subprocess.run(
            ["checkov", "-d", path, "-o", "json"],
            capture_output=True,
            text=True
        )
        if result.stdout:
            data = json.loads(result.stdout)
            # Simplified findings extraction
            findings = []
            if isinstance(data, list):
                for report in data:
                    findings.extend(report.get("results", {}).get("failed_checks", []))
            else:
                findings = data.get("results", {}).get("failed_checks", [])
            return findings
    except Exception as e:
        print(f"Error running Checkov: {e}")
        return []
    return []
