import subprocess
import json

from src.finding_utils import extract_failed_checks


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
            return extract_failed_checks(data)
    except Exception as e:
        print(f"Error running Checkov: {e}")
        return []
    return []
