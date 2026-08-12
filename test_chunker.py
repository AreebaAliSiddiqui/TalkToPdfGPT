
from ingestion.chunker import chunk_text
from ingestion.pdf_loader import extract_text_from_pdf

file_path = "data/Chapter_3.pdf"  # Replace with the actual path to your PDF file
pages = extract_text_from_pdf(file_path)
chunks = chunk_text(pages)
print(f"Number of chunks: {len(chunks)}")
print(f"First chunk: {chunks[0]}")   