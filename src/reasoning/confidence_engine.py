from typing import List


def calculate_overall_confidence(findings: List[dict]) -> float:
    score_map = {
        "High": 0.9,
        "Medium": 0.7,
        "Low": 0.5
    }

    if not findings:
        return 0.0

    total = 0
    for f in findings:
        total += score_map.get(f["confidence"], 0.5)

    return round(total / len(findings), 2)