from google import genai
from dotenv import load_dotenv
import os 
from vectorstore.chroma_store import collection


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def embed_query(query):
    """
    Takes a query string and returns its embedding vector.
    """
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=[query]
    )
    return response.embeddings[0].values

def retrieve(query, document_id=None, n_results=5):
    """
    Embeds the user's query and retrieves the most relevant
    chunks from Chroma.

    Returns a list of clean chunk dictionaries.
    """

    query_vector = embed_query(query)

    query_kwargs = {
        "query_embeddings" : [query_vector],
        "n_results" : n_results
    }

    if document_id:
        #results = collection.query(
        #    query_embeddings=[query_vector],
        #    n_results=n_results,
        #    where={"document_id": document_id} it meand find the closest chunk anywhere in the collection
        query_kwargs["where"] = {
            "document_id": document_id
        }

    results = collection.query(**query_kwargs)    
    
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    retrieved_chunks = []

    for document, metadata in zip(documents, metadatas):
        retrieved_chunks.append({
            "text": document,
            "page_number": metadata["page_number"],
            "chunk_number": metadata["chunk_number"],
            "document_id": metadata["document_id"]
        })

    return retrieved_chunks