from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=300,
        length_function=len,
    )
    chunks = []

    if isinstance(pages, str):
        pages = [{"page_number": 1, "text": pages}]

    for page in pages:
        page_text = page.get("text", "")
        if not page_text:
            continue

        for chunk_number, chunk in enumerate(text_splitter.split_text(page_text), start=1):
            chunks.append({
                "text": chunk,
                "page_number": page.get("page_number"),
                "chunk_number": chunk_number,
            })

    return chunks



