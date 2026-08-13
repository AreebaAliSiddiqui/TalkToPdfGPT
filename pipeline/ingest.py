
from ingestion.pdf_loader import extract_text_from_pdf
from ingestion.chunker import chunk_text
from embeddings.embedder import embed_chunks
from vectorstore.chroma_store import add_chunks
import uuid



def ingest_pdf(file_path):
   
    pages = extract_text_from_pdf(file_path)

    chunks = chunk_text(pages)

    vectors = embed_chunks(chunks)

    document_id = str(uuid.uuid4())
    
    metadata_list = []
    for chunk in chunks:
        metadata_list.append({
            "page_number": chunk["page_number"],
            "chunk_number": chunk["chunk_number"],
            "document_id": document_id
        })

    add_chunks(chunks, vectors, metadata_list)