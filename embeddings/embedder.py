#take the chunks , give to gemini embedding 2 so it can create vectors for each chunk and return the vectors to us.
#chunks goes in the fucntion
#embedding function returns the vectors for each chunk
#gemini api key comes from the .env file
# model for embedding is "gemini-embedding-2"
# we are embeddings multiple chunks at once, so we will use the batch embedding function from the gemini api
# if gemini api fails, we will catch exception and return an error message and raise a controlled error.

import os
from google import genai
from dotenv import load_dotenv
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def _chunk_to_text(chunk):
    if isinstance(chunk, dict):
        return chunk.get("text", "")
    return chunk



def embed_chunks(chunks):
    """
    Takes a list of text chunks and returns 
    a list of embedding vectors.
    """
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=[
            types.Content(
                parts=[
                    types.Part.from_text(text=_chunk_to_text(chunk))
                ]
            )
            for chunk in chunks
        ]
    )
    vectors = [embedding.values for embedding in response.embeddings]

    return vectors