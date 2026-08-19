
from ingestion.pdf_loader import extract_text_from_pdf
from ingestion.chunker import chunk_text
from embeddings.embedder import embed_chunks
from vectorstore.chroma_store import add_chunks, find_document_by_hash
import uuid
import hashlib

def calculate_file_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()

def ingest_pdf(file_path):
   
    document_hash = calculate_file_hash(file_path)

    existing_document_id = find_document_by_hash(document_hash)

    if existing_document_id:
        return existing_document_id
    
    pages = extract_text_from_pdf(file_path)

    chunks = chunk_text(pages)

    vectors = embed_chunks(chunks)

    document_id = str(uuid.uuid4())
    
    metadata_list = []
    for chunk in chunks:
        metadata_list.append({
            "page_number": chunk["page_number"],
            "chunk_number": chunk["chunk_number"],
            "document_id": document_id,
            "document_hash": document_hash
        })

    add_chunks(chunks, vectors, metadata_list)
    return document_id