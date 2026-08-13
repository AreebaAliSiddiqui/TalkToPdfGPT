from retrieval.retriever import retrieve
from generation.generator import generate_answer


query = "What are the principles of agility?"

retrieved_chunks = retrieve(query, n_results=5)

answer = generate_answer(
    query,
    retrieved_chunks
)


print("\nAnswer:")
print(answer)