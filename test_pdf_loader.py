from ingestion.pdf_loader import extract_text_from_pdf

file_path = "data/Chapter_3.pdf"  # Replace with the actual path to your PDF file
pages = extract_text_from_pdf(file_path)

for page in pages:
	print(f"Page {page['page_number']}: {page['text'][:200]}")