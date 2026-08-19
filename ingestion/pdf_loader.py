from pypdf import PdfReader


def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
    except Exception as e:
        raise ValueError("This PDF is corrupted or cannot be read.") from e

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append({
            "page_number": page_number,
            "text": text,
        })

    return pages