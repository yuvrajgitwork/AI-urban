from unstructured.partition.pdf import partition_pdf


def extract_text_unstructured(pdf_path: str) -> str:
    elements = partition_pdf(filename=pdf_path)
    text_chunks = [el.text for el in elements if hasattr(el, "text") and el.text]
    return "\n".join(text_chunks)