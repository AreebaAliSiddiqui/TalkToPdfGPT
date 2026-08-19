from retrieval.retriever import retrieve


document_id = "c8da490f-d7b9-4302-9ea1-1b2f41c715be"

results = retrieve(
    "What are the principles of agility?",
    document_id=document_id
)

print(f"Retrieved {len(results)} chunks")

for chunk in results:
    print(
        f"Page: {chunk['page_number']} | "
        f"Document ID: {chunk['document_id']}"
    )