#take the vectors, chunks and metadata and store them in the chroma vectorstore 
# so that we can retrieve them later for semantic search.
"""
1. Creating a persistent Chroma client
2. Creating/getting a collection/table
3. Create a function to add chunks, vectors, and metadata to the collection,The IDs should also be generated.
4. Make the vector store capable of filtering by document_id
"""
import chromadb
from datetime import datetime


client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="documents_gemini",
    embedding_function=None,
    metadata={
        "description": "Talk to PDF GPT documents",
        "created": str(datetime.now())
    }
)


def add_chunks(chunks, vectors, metadata):
    ids = [
    f"{item['document_id']}_page_{item['page_number']}_chunk_{item['chunk_number']}"
    for item in metadata
]

    documents = [chunk["text"] for chunk in chunks]

    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=documents,
        metadatas=metadata
    )

    print(f"Documents stored: {len(documents)}")

    return collection