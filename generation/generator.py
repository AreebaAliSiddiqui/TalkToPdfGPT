import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_answer(query, retrieved_chunks):
    """
    Generates an answer based only on the retrieved PDF context.
    """

    context_parts = []

    for chunk in retrieved_chunks:
        context_parts.append(
            f"Page {chunk['page_number']}:\n{chunk['text']}"
    )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are Talk to PDF GPT.

Answer the user's question using ONLY the provided PDF context.

If the answer cannot be found in the provided context,
say that the information was not found in the PDF.

Always mention the relevant page number when possible.

PDF CONTEXT:
{context}

USER QUESTION:
{query}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# HERE MY MODEL SUCCEFULY DOES THESE STEPS :
"""PDF
 ↓
Extract text
 ↓
Create chunks
 ↓
Create Gemini embeddings
 ↓
Store vectors + text + metadata in Chroma
 ↓
User asks question
 ↓
Embed question
 ↓
Semantic search in Chroma
 ↓
Retrieve relevant chunks
 ↓
Pass chunks + page numbers to Gemini
 ↓
Generate grounded answer"""