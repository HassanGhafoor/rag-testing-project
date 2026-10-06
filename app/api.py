import chromadb
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

from index import DB_PATH, COLLECTION_NAME, MODEL_NAME
from answer import OLLAMA_URL, LLM_MODEL, INSTRUCTIONS

app = FastAPI(title="Nimbus RAG API")

model = SentenceTransformer(MODEL_NAME)
collection = chromadb.PersistentClient(path=DB_PATH).get_collection(COLLECTION_NAME)


class RetrieveRequest(BaseModel):
    question: str
    k: int = 3


class GenerateRequest(BaseModel):
    question: str
    context: list[str]


class AskRequest(BaseModel):
    question: str


def retrieve(question, k):
    vector = model.encode([question]).tolist()
    results = collection.query(
        query_embeddings=vector,
        n_results=k,
        where={"status": "current"},
    )
    return [
        {
            "id": results["ids"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i],
            "text": results["documents"][0][i],
        }
        for i in range(len(results["ids"][0]))
    ]


def generate(question, context):
    joined = "\n\n---\n\n".join(context)
    prompt = f"{INSTRUCTIONS}\n\nContext:\n{joined}\n\nQuestion: {question}\nAnswer:"
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        },
    )
    return response.json()["response"]


@app.post("/retrieve")
def retrieve_endpoint(req: RetrieveRequest):
    return {"question": req.question, "hits": retrieve(req.question, req.k)}


@app.post("/generate")
def generate_endpoint(req: GenerateRequest):
    return {"question": req.question, "answer": generate(req.question, req.context)}


@app.post("/ask")
def ask_endpoint(req: AskRequest):
    hits = retrieve(req.question, 3)
    answer = generate(req.question, [h["text"] for h in hits])
    return {"question": req.question, "answer": answer, "hits": hits}