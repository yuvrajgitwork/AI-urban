from typing import List
from utils.schemas import ThermalSummary


def correlate_with_thermal(findings: List[dict], thermal: ThermalSummary) -> List[dict]:
    """
    Correlates inspection findings with thermal summary.
    Adds thermal support flag.
    """

    delta = thermal.delta

    for finding in findings:

        if "bathroom" in finding["area"].lower() and delta > 6:
            finding["thermal_correlation"] = (
                "Thermal data supports possible moisture presence in this area."
            )
            finding["thermal_support"] = True

        elif "wall" in finding["issue"].lower() and delta > 5:
            finding["thermal_correlation"] = (
                "Thermal variation may correspond with wall anomalies."
            )
            finding["thermal_support"] = True

        else:
            finding["thermal_correlation"] = (
                "No direct thermal mapping available for this area."
            )
            finding["thermal_support"] = False

    return findings