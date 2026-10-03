import sys

import requests

from search import search

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "llama3.1:8b"

INSTRUCTIONS = """You are an assistant for Nimbus Logistics employees.
Answer the question using ONLY the information in the context below.
If the context does not contain the answer, say: "I don't know based on the company documents."
Keep the answer short."""


def build_prompt(question, hits):
    context = "\n\n---\n\n".join(hit["text"] for hit in hits)
    return f"{INSTRUCTIONS}\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"


def answer(question):
    hits = search(question)
    prompt = build_prompt(question, hits)
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        },
    )
    return response.json()["response"], hits


if __name__ == "__main__":
    question = sys.argv[1]
    text, hits = answer(question)
    print("Cards used:")
    for hit in hits:
        print(f"  {hit['distance']:.3f}  {hit['id']}")
    print("\nAnswer:")
    print(text)