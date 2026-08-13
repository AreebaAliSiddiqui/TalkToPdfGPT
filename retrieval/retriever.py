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




def retrieve(query, n_results=5):
    """
    Takes a query vector and retrieves the top n_results from the Chroma collection.
    """
    query_vector = embed_query(query)
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n_results
    )
    return results