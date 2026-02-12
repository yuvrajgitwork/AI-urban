from parsing.pdf_parser import extract_text_pdfplumber
from pathlib import Path

RAW_DIR = Path("data/raw")
EXTRACTED_DIR = Path("data/extracted")


def extract_all():
    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

    inspection_pdf = RAW_DIR / "Sample_Report.pdf"
    thermal_pdf = RAW_DIR / "Thermal_Images.pdf"

    print("🔍 Extracting Inspection Report with pdfplumber...")
    inspection_text = extract_text_pdfplumber(str(inspection_pdf))

    print("🔍 Extracting Thermal Report with pdfplumber...")
    thermal_text = extract_text_pdfplumber(str(thermal_pdf))

    (EXTRACTED_DIR / "inspection_text.txt").write_text(inspection_text, encoding="utf-8")
    (EXTRACTED_DIR / "thermal_text.txt").write_text(thermal_text, encoding="utf-8")

    print("✅ Extraction complete.")
    print(f"Saved to {EXTRACTED_DIR}")


if __name__ == "__main__":
    extract_all()
