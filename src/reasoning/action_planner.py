from typing import List, Dict


def build_action_plan(findings: List[Dict]) -> Dict[str, List[str]]:
    immediate = []
    short_term = []
    verification = []

    # Immediate based on high severity indicators
    for f in findings:
        issue = (f.get("issue") or "").lower()

        if f.get("severity") == "High":
            if "leak" in issue or "leakage" in issue:
                immediate.append("Investigate and repair the active leakage source immediately to prevent further damage.")
            if "crack" in issue:
                immediate.append("Conduct structural assessment of reported cracks and carry out appropriate repair/remediation.")

    # Short-term (common moisture contributors)
    for f in findings:
        issue = (f.get("issue") or "").lower()
        if "damp" in issue or "efflorescence" in issue:
            short_term.append("Address dampness/efflorescence areas after identifying the moisture pathway; repair finishes after source control.")
        if "tile joint" in issue or "tile joints" in issue or "gap between tile" in issue or "gaps between tile" in issue:
            short_term.append("Re-grout and seal tile joints in affected wet areas to reduce water ingress.")
        if "plumbing" in issue:
            short_term.append("Inspect plumbing lines and fittings in affected bathrooms; repair any defects found.")

    # Verification steps (diagnostic-grade)
    verification.extend([
        "Perform moisture meter readings at affected walls (skirting zones, bathrooms, adjacent rooms) to quantify moisture extent.",
        "If plumbing leakage is suspected, perform a plumbing pressure test to confirm.",
        "Repeat thermal scan post-repair to confirm anomaly reduction (room-level mapping recommended)."
    ])

    # Deduplicate while preserving order
    def dedupe(seq):
        seen = set()
        out = []
        for x in seq:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    return {
        "Immediate": dedupe(immediate) if immediate else ["Not Available"],
        "Short-term": dedupe(short_term) if short_term else ["Not Available"],
        "Verification": dedupe(verification)
    }