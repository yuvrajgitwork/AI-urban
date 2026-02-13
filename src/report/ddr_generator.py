from typing import List, Dict
from utils.schemas import ThermalSummary


def generate_property_summary(findings: List[Dict]) -> str:
    total = len(findings)
    high = sum(1 for f in findings if f["severity"] == "High")
    medium = sum(1 for f in findings if f["severity"] == "Medium")
    low = sum(1 for f in findings if f["severity"] == "Low")

    return (
        f"A total of {total} issues were identified during inspection. "
        f"{high} classified as High severity, "
        f"{medium} as Medium severity, "
        f"and {low} as Low severity."
    )


def generate_area_observations(findings: List[Dict]) -> Dict[str, List[Dict]]:
    area_map = {}

    for f in findings:
        area_map.setdefault(f["area"], []).append(f)

    return area_map


def generate_root_cause(findings: List[Dict], thermal: ThermalSummary) -> str:
    if thermal.delta > 7:
        return (
            "Significant thermal variation observed. Combined with dampness-related "
            "findings, this suggests potential moisture ingress or waterproofing failure."
        )
    elif thermal.delta > 4:
        return (
            "Moderate thermal variation detected. This may indicate localized moisture "
            "presence or material inconsistencies."
        )
    else:
        return (
            "No strong thermal anomalies detected. Issues may be surface-level or "
            "maintenance-related."
        )


def generate_recommendations(findings: List[Dict]) -> List[str]:
    recommendations = set()

    for f in findings:
        issue = f["issue"].lower()

        if "damp" in issue:
            recommendations.add(
                "Inspect waterproofing layers and identify potential water ingress points."
            )

        if "gap" in issue:
            recommendations.add(
                "Re-grout and seal tile joints to prevent moisture penetration."
            )

        if "crack" in issue:
            recommendations.add(
                "Conduct structural assessment of cracks and repair using approved materials."
            )

        if "leak" in issue:
            recommendations.add(
                "Inspect plumbing and ceiling slab for active leakage and repair immediately."
            )

    return list(recommendations)


def generate_missing_info(thermal: ThermalSummary) -> List[str]:
    missing = []

    if thermal.mapping_confidence.lower() != "high":
        missing.append("Thermal image-to-room mapping confidence is not High.")

    return missing


def generate_ddr(findings: List[Dict], thermal: ThermalSummary, overall_confidence: float) -> str:

    summary = generate_property_summary(findings)
    area_map = generate_area_observations(findings)
    root_cause = generate_root_cause(findings, thermal)
    recommendations = generate_recommendations(findings)
    missing_info = generate_missing_info(thermal)

    report_lines = []

    report_lines.append("# Detailed Diagnostic Report (DDR)\n")

    # Executive Summary
    report_lines.append("## Executive Summary\n")
    report_lines.append(
        f"The inspection identified {len(findings)} documented issues across the evaluated property. "
        f"The overall analytical confidence score for this report is {overall_confidence} "
        f"(scale 0–1), derived from structured evidence extraction and thermal validation.\n"
    )

    # Property Summary
    report_lines.append("## 1. Property Issue Summary\n")
    report_lines.append(summary + "\n")

    # Area Observations
    report_lines.append("## 2. Area-wise Observations\n")

    for area, items in area_map.items():
        report_lines.append(f"### {area}")
        for item in items:
            report_lines.append(
                f"- {item['issue']} "
                f"(Severity: {item['severity']}, "
                f"Thermal Support: {item.get('thermal_support', False)})"
            )
        report_lines.append("")

    # Root Cause
    report_lines.append("## 3. Probable Root Cause\n")
    report_lines.append(root_cause + "\n")

    # Recommendations
    report_lines.append("## 4. Recommended Actions\n")
    for rec in recommendations:
        report_lines.append(f"- {rec}")
    report_lines.append("")

    # Thermal Notes
    report_lines.append("## 5. Thermal Analysis Notes\n")
    report_lines.append(thermal.interpretation + "\n")

    # Evidence Traceability
    report_lines.append("## 6. Evidence Traceability\n")
    for f in findings:
        report_lines.append(
            f"- {f['area']} → {f['issue']} | Source: {f['source']}"
        )
    report_lines.append("")

    # Missing Info
    report_lines.append("## 7. Missing or Unclear Information\n")
    if missing_info:
        for m in missing_info:
            report_lines.append(f"- {m}")
    else:
        report_lines.append("None identified based on provided documents.")

    return "\n".join(report_lines)
