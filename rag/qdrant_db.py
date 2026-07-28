from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

client = QdrantClient(host="localhost", port=6333)

COLLECTION_NAME = "pdf_chunks"


def create_collection():

    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    # Delete old collection
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
        print("Old collection deleted.")

    # Create new collection
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print("New collection created.")


def upload_chunks(chunks, embeddings, filename):

    points = []

    for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

        point = PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "source": filename,
                "chunk_id": index
            }
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print(f"{len(points)} chunks uploaded successfully.")