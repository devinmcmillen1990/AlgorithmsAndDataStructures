import json
from pathlib import Path


def load_test_cases(path: Path) -> list[dict]:
    cases = json.loads(path.read_text(encoding="utf-8"))
    _validate_test_cases(path, cases)
    return cases

def _validate_test_cases(path, cases):
    if not isinstance(cases, list) or not cases:    raise ValueError(f"{path}: expected a nonempty JSON list.")
    for number, case in enumerate(cases, start=1):
        if not isinstance(case, dict):              raise ValueError(f"Case {number} must be a JSON object.")
        if not isinstance(case.get("name"), str):   raise ValueError(f"Case {number} needs an str 'name'.")
        if not isinstance(case.get("input"), str):  raise ValueError(f"Case {number} needs an str 'input'.")
        if type(case.get("expected")) is not int:   raise ValueError(f"Case {number} needs an int 'expected'")