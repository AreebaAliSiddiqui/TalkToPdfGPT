from retrieval.retriever import retrieve


query = "What are the principles of agility?"

results = retrieve(query, n_results=5)

print(f"Retrieved {len(results)} chunks:\n")

for chunk in results:
    print(f"Page: {chunk['page_number']}")
    print(f"Chunk: {chunk['chunk_number']}")
    print(f"Document ID: {chunk['document_id']}")
    print(f"Text: {chunk['text'][:200]}...")
    print("-" * 50)