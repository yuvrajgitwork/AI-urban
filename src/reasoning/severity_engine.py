from typing import List
from utils.schemas import Finding


def calculate_severity(finding: Finding) -> str:
    """
    Rule-based severity scoring.
    Can be upgraded later to ML scoring.
    """

    issue_text = finding.issue.lower()
    description_text = finding.description.lower()

    high_keywords = ["severe", "structural", "crack", "leak", "water ingress"]
    medium_keywords = ["damp", "gap", "tile", "minor"]
    
    if any(word in issue_text or word in description_text for word in high_keywords):
        return "High"

    if any(word in issue_text or word in description_text for word in medium_keywords):
        return "Medium"

    return "Low"


def apply_severity(findings: List[Finding]) -> List[dict]:
    """
    Adds severity to findings.
    """

    enriched = []

    for finding in findings:
        severity = calculate_severity(finding)

        enriched.append({
            "area": finding.area,
            "issue": finding.issue,
            "description": finding.description,
            "severity": severity,
            "confidence": finding.confidence,
            "source": finding.source,
            "evidence": [e.model_dump() for e in finding.evidence],
        })

    return enriched