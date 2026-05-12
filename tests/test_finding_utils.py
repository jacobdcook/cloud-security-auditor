from src.finding_utils import (
    count_remediation_severities,
    extract_failed_checks,
    normalize_severity,
    strip_code_fence,
)


def test_extract_failed_checks_dict():
    data = {"results": {"failed_checks": [{"check_id": "CKV_AZURE_1"}]}}
    assert extract_failed_checks(data) == [{"check_id": "CKV_AZURE_1"}]


def test_extract_failed_checks_list():
    data = [
        {"results": {"failed_checks": [{"a": 1}]}},
        {"results": {"failed_checks": [{"b": 2}]}},
    ]
    out = extract_failed_checks(data)
    assert out == [{"a": 1}, {"b": 2}]


def test_extract_failed_checks_empty():
    assert extract_failed_checks({}) == []
    assert extract_failed_checks([]) == []
    assert extract_failed_checks(None) == []


def test_strip_code_fence_none():
    assert strip_code_fence("resource \"x\" {}\n") == "resource \"x\" {}\n"


def test_strip_code_fence_hcl():
    raw = "```hcl\nresource \"x\" {}\n```"
    assert strip_code_fence(raw) == "resource \"x\" {}"


def test_normalize_severity():
    assert normalize_severity("high") == "HIGH"
    assert normalize_severity(None) == "MEDIUM"
    assert normalize_severity("weird") == "UNKNOWN"


def test_count_remediation_severities():
    entries = [
        {"finding": {"severity": "Critical"}, "fix": "x"},
        {"finding": {"severity": "high"}, "fix": "y"},
        {"finding": {}, "fix": "z"},
    ]
    c = count_remediation_severities(entries)
    assert c["CRITICAL"] == 1
    assert c["HIGH"] == 1
    assert c["MEDIUM"] == 1
    assert c["UNKNOWN"] == 0
