import chromadb
from sentence_transformers import SentenceTransformer

from chunking import load_documents, chunk_by_section

DB_PATH = "chroma_db"
COLLECTION_NAME = "nimbus"
MODEL_NAME = "all-MiniLM-L6-v2"


def build_index():
    chunks = []
    for doc in load_documents():
        chunks.extend(chunk_by_section(doc))

    model = SentenceTransformer(MODEL_NAME)
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts).tolist()

    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[c["id"] for c in chunks],
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            {
                "source": c["source"],
                "section": c["section"],
                "status": "archived" if "archived" in c["source"] else "current",
            }
            for c in chunks
        ],
    )
    return collection


if __name__ == "__main__":
    collection = build_index()
    print(f"Stored {collection.count()} chunks in Chroma")