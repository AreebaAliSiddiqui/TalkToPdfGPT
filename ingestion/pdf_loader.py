from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = []
    has_text = False
    for page in reader.pages:
        result = page.extract_text()
        if result is None:
            continue
        text.append(result)
        has_text = True

    if not has_text:
        print("All pages have no text.")
        return ""

    return "\n".join(text)
