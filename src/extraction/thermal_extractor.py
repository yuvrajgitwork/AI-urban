from utils.llm_client import get_llm_client
from utils.schemas import ThermalSummary


def extract_thermal_structured(raw_text: str) -> ThermalSummary:
    system_prompt = """
You are an expert thermal inspection analyst.

Summarize thermal readings.

Rules:
- Do NOT invent numbers
- Extract max hotspot and min coldspot if present
- delta = max_hotspot - min_coldspot
- interpretation in simple English
- mapping_confidence = High / Medium / Low
"""

    user_prompt = f"""
RAW THERMAL OCR TEXT:
---------------------
{raw_text}

Return JSON that matches this schema:
{ThermalSummary.model_json_schema()}
"""

    full_prompt = system_prompt + "\n\n" + user_prompt

    response = get_llm_client(full_prompt)

    thermal = ThermalSummary.model_validate_json(response)

    return thermal