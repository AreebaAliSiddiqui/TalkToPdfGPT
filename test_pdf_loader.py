from ingestion.pdf_loader import extract_text_from_pdf

file_path = "data/Chapter_3.pdf"  # Replace with the actual path to your PDF file
text = extract_text_from_pdf(file_path)

print(text)