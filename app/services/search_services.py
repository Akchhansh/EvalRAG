from app.services.embedding_services import generate_embeddings
from app.services.qdrant_services import client, COLLECTION_NAME

def search_documents(query, limit=3):
    query_embedding = generate_embeddings(query)
    results=client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding.tolist(),
        limit=limit
    )
    return results.points

