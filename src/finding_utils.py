from __future__ import annotations

from typing import Any, Dict, List


def extract_failed_checks(checkov_data: Any) -> List[dict]:
    if checkov_data is None:
        return []
    findings: List[dict] = []
    if isinstance(checkov_data, list):
        for report in checkov_data:
            failed = report.get("results", {}).get("failed_checks", [])
            findings.extend(failed)
    elif isinstance(checkov_data, dict):
        findings = checkov_data.get("results", {}).get("failed_checks", [])
    else:
        return []
    return findings


def strip_code_fence(text: str) -> str:
    if not text.startswith("```"):
        return text
    lines = text.split("\n")
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines)


def normalize_severity(severity: Any) -> str:
    s = str(severity or "MEDIUM").upper()
    return s if s in {"CRITICAL", "HIGH", "MEDIUM", "LOW"} else "UNKNOWN"


def count_remediation_severities(remediation_entries: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0}
    for entry in remediation_entries:
        finding = entry.get("finding") or {}
        sev = normalize_severity(finding.get("severity", "MEDIUM"))
        counts[sev] += 1
    return counts
