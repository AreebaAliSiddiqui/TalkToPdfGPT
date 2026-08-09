from pypdf import PdfReader

file_path = "path/to/your/data" 
def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = []
    has_text = False
    for page in reader.pages:
        result = page.extract_text()
        if not result:
            continue
        text.append(result)
        has_text = True

    if not has_text:
        return ""

    return "\n".join(text)
