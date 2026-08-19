import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Read host & port from environment variables (defaults to localhost:6333)
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

COLLECTION_NAME = "documents"

def create_collection():
    collections = client.get_collections().collections
    names = [collection.name for collection in collections]
    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

import uuid
def store_embeddings(chunks, embeddings, filename):
    points = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload={
                    "text": chunk,
                    "filename": filename,
                    "chunk": i
                }
            )
        )
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )