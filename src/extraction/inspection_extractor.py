from typing import List
from pydantic import TypeAdapter

from utils.llm_client import get_llm_client
from utils.schemas import Finding


def extract_inspection_structured(raw_text: str) -> List[Finding]:
    system_prompt = """
You are an expert property inspection analyst.

Extract key inspection findings from the raw inspection report.

Rules:
- Do NOT invent issues
- Only extract issues clearly mentioned
- Use direct quotes in evidence
- confidence must be High, Medium, or Low
"""

    user_prompt = f"""
RAW INSPECTION REPORT:
----------------------
{raw_text}

Return a JSON ARRAY where each item matches this schema:
{Finding.model_json_schema()}
"""

    full_prompt = system_prompt + "\n\n" + user_prompt

    # Call LLM directly (your function expects prompt)
    response = get_llm_client(full_prompt)

    # Parse LIST of findings (THIS WAS YOUR CRASH)
    adapter = TypeAdapter(List[Finding])
    findings = adapter.validate_json(response)

    return findings