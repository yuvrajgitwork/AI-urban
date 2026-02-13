from typing import List


def generate_flags(findings: List[dict]) -> List[dict]:
    """
    Flags critical findings.
    """

    for finding in findings:
        if finding["severity"] == "High":
            finding["risk_flag"] = True
        else:
            finding["risk_flag"] = False

    return findings