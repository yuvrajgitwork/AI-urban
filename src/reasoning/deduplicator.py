from typing import List
from utils.schemas import Finding


def normalize_text(text: str) -> str:
    return text.lower().strip()


def deduplicate_findings(findings: List[Finding]) -> List[Finding]:
    """
    Removes duplicate findings based on area + issue similarity.
    Keeps the first occurrence.
    """

    seen = set()
    unique_findings = []

    for finding in findings:
        key = (
            normalize_text(finding.area),
            normalize_text(finding.issue),
        )

        if key not in seen:
            seen.add(key)
            unique_findings.append(finding)

    return unique_findings