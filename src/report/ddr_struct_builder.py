from typing import List, Dict
from utils.schemas import ThermalSummary


def _group_area_findings(findings: List[Dict]) -> Dict[str, Dict]:
    """
    Report-level grouping to avoid duplicate bullets.
    Keeps raw findings for appendix; merges narrative at area level.
    """
    areas = {}

    for f in findings:
        area = f["area"]
        areas.setdefault(area, {
            "area": area,
            "issues": [],
            "severity_levels": set(),
            "thermal_support_any": False,
            "raw_items": []
        })

        areas[area]["raw_items"].append(f)
        areas[area]["severity_levels"].add(f.get("severity", "Not Available"))
        areas[area]["thermal_support_any"] = areas[area]["thermal_support_any"] or bool(f.get("thermal_support", False))

        # Merge-style issue phrasing: de-duplicate issue strings
        issue_str = f.get("issue", "Not Available")
        if issue_str not in areas[area]["issues"]:
            areas[area]["issues"].append(issue_str)

    # convert severity set to a sorted list (High > Medium > Low)
    order = {"High": 0, "Medium": 1, "Low": 2, "Not Available": 3}
    for area in areas:
        sev = list(areas[area]["severity_levels"])
        sev.sort(key=lambda x: order.get(x, 99))
        areas[area]["severity_levels"] = sev

    return areas


def build_structured_ddr(
    findings: List[Dict],
    thermal: ThermalSummary,
    overall_confidence: float,
    missing_info: List[str],
    consistency_note: str,
    hypotheses: List[Dict],
    action_plan: Dict[str, List[str]]
) -> dict:

    high = sum(1 for f in findings if f.get("severity") == "High")
    medium = sum(1 for f in findings if f.get("severity") == "Medium")
    low = sum(1 for f in findings if f.get("severity") == "Low")

    # IMPORTANT: safer thermal statement (no room-level mapping claims)
    thermal_note = {
        "max_hotspot": thermal.max_hotspot,
        "min_coldspot": thermal.min_coldspot,
        "delta": thermal.delta,
        "interpretation": thermal.interpretation,
        "mapping_confidence": thermal.mapping_confidence,
        "constraint": "Room-level mapping of thermal images is Not Available unless explicitly provided in the thermal report text."
    }

    areas = _group_area_findings(findings)

    # Evidence appendix inputs (raw quotes + sources)
    evidence_rows = []
    for f in findings:
        ev = f.get("evidence", [])
        if not ev:
            evidence_rows.append({
                "area": f.get("area", "Not Available"),
                "issue": f.get("issue", "Not Available"),
                "source": f.get("source", "Not Available"),
                "quote": "Not Available"
            })
        else:
            for e in ev:
                evidence_rows.append({
                    "area": f.get("area", "Not Available"),
                    "issue": f.get("issue", "Not Available"),
                    "source": e.get("source", f.get("source", "Not Available")),
                    "quote": e.get("quote", "Not Available")
                })

    structured = {
        "executive_summary": {
            "total_issues": len(findings),
            "high": high,
            "medium": medium,
            "low": low,
            "overall_confidence": overall_confidence
        },
        "property_issue_summary": {
            "primary_themes": [
                "Moisture-related symptoms (dampness/efflorescence/leakage)",
                "Finish defects in wet areas (tile joint gaps)",
                "External envelope concerns (cracks)"
            ]
        },
        "area_observations": areas,  # grouped
        "severity_assessment_rules": {
            "High": "Active leakage or cracks that can impact durability/safety if unaddressed.",
            "Medium": "Moisture indicators or finish defects that may worsen and require remediation."
        },
        "probable_root_cause_hypotheses": hypotheses,
        "recommended_action_plan": action_plan,
        "thermal_analysis": thermal_note,
        "missing_information": missing_info,
        "consistency_check": consistency_note,
        "evidence_appendix": evidence_rows
    }

    return structured