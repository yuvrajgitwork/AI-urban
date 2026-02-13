# DDR Report Generation (Inspection + Thermal → Client-Ready DDR)

This project builds an AI workflow that reads a **Property Inspection Report** PDF and a **Thermal Report** PDF and generates a **Detailed Diagnostic Report (DDR)** in a structured, client-friendly format.

The pipeline is designed to be **reliable and grounded**:
- No invented facts
- Evidence-backed findings
- Explicit “Not Available” for missing info
- Clear handling of limitations and correlation constraints

---

## What This Produces

Outputs are written to:

- `data/extracted/`
  - `inspection_text.txt`
  - `thermal_text.txt`

- `data/structured/`
  - `inspection_findings.json` (LLM structured extraction)
  - `thermal_summary.json` (LLM structured thermal summary)
  - `merged_findings.json` (dedup + severity + thermal correlation + flags)
  - `structured_ddr.json` (final structured DDR input for narrative synthesis)

- `outputs/`
  - `DDR_Report.md` ✅ Final client-ready DDR (with Evidence Appendix)

---

## Architecture Overview

### 1) Parsing (PDF → text)
- `src/parsing/unstructured_parser.py` (preferred)
- `src/parsing/pdf_parser.py` (fallback)

### 2) Structured Extraction (text → JSON via LLM)
- `src/extraction/inspection_extractor.py`
- `src/extraction/thermal_extractor.py`

### 3) Reasoning Layer (deterministic, reliable)
- `src/reasoning/deduplicator.py` (remove duplicates)
- `src/reasoning/severity_engine.py` (rule-based severity)
- `src/reasoning/thermal_correlation.py` (safe thermal correlation without room overclaim)
- `src/reasoning/flags_engine.py` (risk flags)
- `src/reasoning/confidence_engine.py` (overall confidence)
- `src/reasoning/diagnostics_analyzer.py` (missing info + conflict/consistency note)
- `src/reasoning/root_cause_hypotheses.py` (hypothesis-based root causes with confidence)
- `src/reasoning/action_planner.py` (prioritized actions + verification steps)

### 4) DDR Synthesis (structured DDR → polished report via LLM)
- `src/report/ddr_struct_builder.py` (build structured DDR JSON + evidence appendix)
- `src/report/ddr_llm_writer.py` (GPT-4.1 narrative synthesis with strict grounding rules)

### 5) Orchestration
- `src/main.py` runs the full end-to-end pipeline.

---

## Setup

### Option A: GitHub Codespaces (recommended)
1. Open this repo in Codespaces
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Create dot env file
4. Set your API key in .env:

OPENAI_API_KEY=... (or your GitHub Models/OpenAI-compatible key)

**Input Files**

Place input PDFs in:
data/raw/
Expected naming convention: One inspection report PDF
                            One thermal report PDF

Example: Inspection_Report_3.pdf
         Thermal_Report_3.pdf

**Run**

From repo root:

PYTHONPATH=src python src/main.py


After successful run, the final DDR will be available at:

**outputs/DDR_Report.md   ** ---
sample ouput attached in /output

Loom video link- https://www.boomshare.ai/shared/01KHC6DN6QQDFTBJXAHYBM2YQ7
