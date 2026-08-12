from vectorstore.chroma_store import add_chunks


chunks = ["doc1", "doc2", "doc3"]

vectors = [
    [1.1, 2.3, 3.2],
    [4.5, 6.9, 4.4],
    [1.1, 2.3, 3.2]
]

metadata = [
    {"chapter": 3, "verse": 16},
    {"chapter": 3, "verse": 5},
    {"chapter": 29, "verse": 11}
]


collection = add_chunks(
    chunks=chunks,
    vectors=vectors,
    metadata=metadata
)


result = collection.get(
    include=["documents", "metadatas"]
)


print(f"Documents stored: {len(result['ids'])}")

for id, document, metadata in zip(
    result["ids"],
    result["documents"],
    result["metadatas"]
):
    print(id, document, metadata)