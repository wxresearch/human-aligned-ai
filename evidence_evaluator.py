"""Conservative, offline evidence-consistency checks for structured test cases.

Only evaluates user-authored expected phrases and forbidden patterns.
A 'pass' is NOT proof the answer is truthful, ethical, or contradiction-free.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

def evaluate_case(case: dict) -> dict:
    answer = case["answer"]
    if not isinstance(answer, str):
        raise ValueError("answer must be text")
    checks = []
    # Explicit, auditable assertions provided by a human test designer.
    for rule in case.get("required_patterns", []):
        matched = re.search(rule, answer, re.IGNORECASE | re.UNICODE) is not None
        checks.append({"name": "required: " + rule, "passed": matched})
    for rule in case.get("forbidden_patterns", []):
        matched = re.search(rule, answer, re.IGNORECASE | re.UNICODE) is not None
        checks.append({"name": "forbidden: " + rule, "passed": not matched})
    return {"id": case.get("id", "unnamed"), "passed": all(x["passed"] for x in checks),
            "checks": checks, "coverage": len(checks),
            "note": "Pattern checks only; human review required for meaning, provenance, and unsupported claims."}

def evaluate_file(path: str) -> dict:
    cases = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        raise ValueError("Fixture must be a JSON array")
    results = [evaluate_case(x) for x in cases]
    return {"passed": sum(x["passed"] for x in results),
            "total": len(results), "cases": results}
