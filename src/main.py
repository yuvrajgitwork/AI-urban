import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent))
import json

from parsing.unstructured_parser import extract_text_unstructured
from parsing.pdf_parser import extract_text_pdfplumber

from extraction.inspection_extractor import extract_inspection_structured
from extraction.thermal_extractor import extract_thermal_structured

from reasoning.deduplicator import deduplicate_findings
from reasoning.severity_engine import apply_severity
from reasoning.thermal_correlation import correlate_with_thermal
from reasoning.flags_engine import generate_flags
from reasoning.confidence_engine import calculate_overall_confidence
from reasoning.root_cause_hypotheses import build_root_cause_hypotheses
from reasoning.action_planner import build_action_plan
from report.ddr_generator import generate_ddr
from reasoning.diagnostics_analyzer import detect_missing_information, detect_conflicts
from report.ddr_struct_builder import build_structured_ddr
from report.ddr_llm_writer import generate_ddr_with_llm

RAW_DIR = Path("data/raw")
EXTRACTED_DIR = Path("data/extracted")
STRUCTURED_DIR = Path("data/structured")


# -----------------------------
# 1️⃣ Parsing Stage
# -----------------------------
def parse_documents():
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    inspection_pdf = next(RAW_DIR.glob("Inspection_*.pdf"), None)
    thermal_pdf = next(RAW_DIR.glob("Thermal_*.pdf"), None)

    if not inspection_pdf or not thermal_pdf:
        raise FileNotFoundError("Inspection or Thermal PDF not found in data/raw")
    print("🔍 Extracting Inspection Report...")
    try:
        inspection_text = extract_text_unstructured(str(inspection_pdf))
        print("✅ Used unstructured for Inspection")
    except Exception as e:
        print("⚠️ Fallback to pdfplumber for Inspection:", e)
        inspection_text = extract_text_pdfplumber(str(inspection_pdf))

    print("🔍 Extracting Thermal Report...")
    try:
        thermal_text = extract_text_unstructured(str(thermal_pdf))
        print("✅ Used unstructured for Thermal")
    except Exception as e:
        print("⚠️ Fallback to pdfplumber for Thermal:", e)
        thermal_text = extract_text_pdfplumber(str(thermal_pdf))

    (EXTRACTED_DIR / "inspection_text.txt").write_text(inspection_text, encoding="utf-8")
    (EXTRACTED_DIR / "thermal_text.txt").write_text(thermal_text, encoding="utf-8")

    return inspection_text, thermal_text


# -----------------------------
# 2️⃣ Structuring Stage (LLM)
# -----------------------------
def structure_documents(inspection_text, thermal_text):
    STRUCTURED_DIR.mkdir(parents=True, exist_ok=True)

    print("🧠 Structuring Inspection with LLM...")
    inspection_findings = extract_inspection_structured(inspection_text)

    print("🧠 Structuring Thermal with LLM...")
    thermal_summary = extract_thermal_structured(thermal_text)

    # Save inspection findings
    with open(STRUCTURED_DIR / "inspection_findings.json", "w") as f:
        json.dump([f.model_dump() for f in inspection_findings], f, indent=2)

    # Save thermal summary
    with open(STRUCTURED_DIR / "thermal_summary.json", "w") as f:
        json.dump(thermal_summary.model_dump(), f, indent=2)

    print("✅ Structured data saved.")

    return inspection_findings, thermal_summary


# -----------------------------
# 3️⃣ Reasoning Stage
# -----------------------------
def reasoning_stage(inspection_findings, thermal_summary):
    print("🧠 Running reasoning layer...")

    # Deduplicate
    deduped = deduplicate_findings(inspection_findings)

    # Apply severity scoring
    enriched = apply_severity(deduped)

    # Correlate with thermal data
    correlated = correlate_with_thermal(enriched, thermal_summary)

    # Generate flags
    final_findings = generate_flags(correlated)

    overall_confidence = calculate_overall_confidence(final_findings)
     
    # Save merged findings
    with open(STRUCTURED_DIR / "merged_findings.json", "w") as f:
        json.dump(final_findings, f, indent=2)
    
    # Detect missing info & conflicts
    missing_info = detect_missing_information(thermal_summary)
    consistency_note = detect_conflicts(final_findings, thermal_summary)
    hypotheses = build_root_cause_hypotheses(final_findings)
    action_plan = build_action_plan(final_findings)
    # Build structured DDR
    structured_ddr = build_structured_ddr(
        final_findings,
        thermal_summary,
        overall_confidence,
        missing_info,
        consistency_note,
        hypotheses,
        action_plan
    )

    # Save structured DDR JSON (optional, but great for demo)
    with open(STRUCTURED_DIR / "structured_ddr.json", "w") as f:
        json.dump(structured_ddr, f, indent=2)

    # Generate final DDR via LLM
    print("📝 Generating final DDR using GPT-4.1...")
    final_ddr = generate_ddr_with_llm(structured_ddr)

    OUTPUT_DIR = Path("outputs")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_DIR / "DDR_Report.md", "w") as f:
        f.write(final_ddr)

    print("✅ Final DDR generated in outputs/DDR_Report.md")

# -----------------------------
# 🚀 Full Pipeline
# -----------------------------
def run_pipeline():
    inspection_text, thermal_text = parse_documents()
    inspection_findings, thermal_summary = structure_documents(
        inspection_text, thermal_text
    )
    reasoning_stage(inspection_findings, thermal_summary)


if __name__ == "__main__":
    run_pipeline()