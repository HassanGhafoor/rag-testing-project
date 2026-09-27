from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "Employees get 18 days of annual leave per year.",
    "How many vacation days do staff receive?",
    "The office printer is on the third floor.",
]

embeddings = model.encode(sentences)
print("Shape:", embeddings.shape)
print("leave vs vacation question:", util.cos_sim(embeddings[0], embeddings[1]).item())
print("leave vs printer:          ", util.cos_sim(embeddings[0], embeddings[2]).item())