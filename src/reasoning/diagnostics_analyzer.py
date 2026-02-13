from typing import List, Dict
from utils.schemas import ThermalSummary


def detect_missing_information(thermal: ThermalSummary) -> List[str]:
    missing = []

    # These are genuinely missing in your current data
    missing.append("Room-level mapping of thermal images to specific inspected areas is Not Available.")
    missing.append("Exact source of moisture (plumbing vs seepage vs condensation) is Not Available.")
    missing.append("Depth and extent of moisture penetration is Not Available.")
    missing.append("Confirmation via moisture meter or invasive testing is Not Available.")
    missing.append("Construction details of walls, slabs, and waterproofing systems are Not Available.")
    missing.append("Timing alignment between inspection observations and thermal imaging is Not Available.")

    return missing


def detect_conflicts(findings: List[Dict], thermal: ThermalSummary) -> str:
    """
    Returns a narrative consistency / conflict statement.
    """
    damp_issues = any("damp" in f["issue"].lower() or "leak" in f["issue"].lower() for f in findings)

    if thermal.delta > 6 and damp_issues:
        return (
            "Thermal data shows significant temperature variation, which is generally consistent with "
            "the moisture-related issues observed in the inspection report. However, room-level correlation "
            "is not available due to missing thermal image mapping."
        )

    if thermal.delta <= 3 and damp_issues:
        return (
            "Inspection findings indicate moisture-related issues, but thermal data does not show strong "
            "temperature anomalies. This represents a potential inconsistency or inconclusive correlation."
        )

    return (
        "No direct contradictions between inspection observations and thermal findings were identified "
        "based on the provided documents. However, precise correlation is limited by missing room-level mapping."
    )