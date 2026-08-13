#take the vectors, chunks and metadata and store them in the chroma vectorstore 
# so that we can retrieve them later for semantic search.
"""
1. Creating a persistent Chroma client
2. Creating/getting a collection/table
3. Create a function to add chunks, vectors, and metadata to the collection,The IDs should also be generated.
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
    ids = [f"id_{i}" for i in range(len(chunks))]

    documents = [chunk["text"] for chunk in chunks]

    collection.add(
        ids=ids,
        embeddings=vectors,
        documents=documents,
        metadatas=metadata
    )

    print(f"Documents stored: {len(documents)}")

    return collection