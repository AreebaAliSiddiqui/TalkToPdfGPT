
from embeddings.embedder import embed_chunks

chunks = ["This is a test chunk sentence. It is used to test the embedding function.",
          "This is another test chunk. making it longer to test the embedding function. my name is Riva and I'm a software engineer. I have been working in the tech industry for over 10 years and have experience in various programming languages and frameworks.",
          "This is a third test chunk. It is used to test the embedding function. "]

try:
    vectors = embed_chunks(chunks)
    assert len(vectors) == len(chunks)


    print(f"Number of chunks: {len(chunks)}")
    print(f"Number of embeddings: {len(vectors)}")
    print(f"Embedding dimensions: {len(vectors[0])}")
    print(f"First 5 values: {vectors[0][:5]}")
    
except Exception as e:
    print(f"Error: {e}")