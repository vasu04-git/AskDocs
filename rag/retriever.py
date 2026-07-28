from qdrant_client import QdrantClient
from rag.embedding import generate_embedding

client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "pdf_chunks"


def retrieve(query, limit=5):

    query_embedding = generate_embedding(query)

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=limit
    )

    retrieved_chunks = []

    print("\n===== Retrieved Chunks =====")

    for point in results.points:

        print(point.payload["text"][:200])
        print("Score:", point.score)
        print("------------------------")

        retrieved_chunks.append({
            "text": point.payload["text"],
            "score": point.score,
            "source": point.payload.get("source"),
            "chunk_id": point.payload.get("chunk_id")
        })

    return retrieved_chunks