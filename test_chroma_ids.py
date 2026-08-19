from vectorstore.chroma_store import collection


results = collection.get(
    include=["metadatas"]
)

print(f"Total stored chunks: {len(results['metadatas'])}")

for metadata, chunk_id in zip(
    results["metadatas"],
    results["ids"]
):
    print(
        f"ID: {chunk_id} | "
        f"Document ID: {metadata['document_id']} | "
        f"Page: {metadata['page_number']} | "
        f"Chunk: {metadata['chunk_number']}"
    )