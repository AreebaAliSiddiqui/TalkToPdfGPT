from retrieval.retriever import retrieve


query = "What is the main topic of Chapter 3?"

results = retrieve(query, n_results=5)

print("Retrieved documents:")
print(results["documents"])

print("\nMetadata:")
print(results["metadatas"])

print("\nDistances:")
print(results["distances"])