from typing import List, Dict


def _has_any(findings: List[Dict], keywords: List[str]) -> bool:
    text = " ".join([f"{f.get('issue','')} {f.get('description','')} {f.get('area','')}".lower() for f in findings])
    return any(k.lower() in text for k in keywords)


def build_root_cause_hypotheses(findings: List[Dict]) -> List[Dict]:
    """
    Produces hypotheses with confidence + evidence pointers.
    IMPORTANT: These are hypotheses, not facts.
    """
    hypotheses = []

    # H1: Bathroom waterproofing / tile joint failure
    if _has_any(findings, ["tile joint", "tile joints", "gap between tile", "gaps between tile", "grout", "bathroom"]):
        hypotheses.append({
            "hypothesis": "Bathroom waterproofing / tile joint failure allowing moisture ingress",
            "confidence": "Medium",
            "evidence_basis": [
                "Presence of tile joint gaps in bathroom areas",
                "Multiple moisture indicators observed in bathrooms (where reported)"
            ]
        })

    # H2: Plumbing leakage (localized)
    if _has_any(findings, ["plumbing issue", "pipe", "leak", "leakage"]):
        hypotheses.append({
            "hypothesis": "Localized plumbing leakage contributing to moisture presence",
            "confidence": "Medium" if _has_any(findings, ["plumbing issue"]) else "Low",
            "evidence_basis": [
                "Inspection mentions plumbing-related issue(s) (where reported)",
                "Leakage-related observation(s) present"
            ]
        })

    # H3: External seepage via cracks
    if _has_any(findings, ["external wall", "crack", "cracks", "efflorescence"]):
        hypotheses.append({
            "hypothesis": "External seepage through cracks or building envelope defects",
            "confidence": "Low",
            "evidence_basis": [
                "External wall cracks are reported",
                "Efflorescence/dampness can be consistent with moisture migration (where reported)"
            ]
        })

    # If nothing triggered, still provide a safe hypothesis entry
    if not hypotheses:
        hypotheses.append({
            "hypothesis": "Moisture ingress is suspected based on inspection observations",
            "confidence": "Low",
            "evidence_basis": ["Moisture-related symptoms are reported, but causal linkage is Not Available."]
        })

    return hypotheses