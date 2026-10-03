import sys

import chromadb
from sentence_transformers import SentenceTransformer

from index import DB_PATH, COLLECTION_NAME, MODEL_NAME


def search(question, k=3):
    model = SentenceTransformer(MODEL_NAME)
    query_vector = model.encode([question]).tolist()

    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    results = collection.query(
        query_embeddings=query_vector,
        n_results=k,
        where={"status": "current"},
    )

    hits = []
    for i in range(len(results["ids"][0])):
        hits.append({
            "id": results["ids"][0][i],
            "distance": results["distances"][0][i],
            "text": results["documents"][0][i],
        })
    return hits


if __name__ == "__main__":
    question = sys.argv[1]
    for hit in search(question):
        print(f"{hit['distance']:.3f}  {hit['id']}")