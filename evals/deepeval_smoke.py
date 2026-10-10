import requests
from deepeval.metrics import FaithfulnessMetric
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase

API = "http://127.0.0.1:8000"
QUESTION = "How many annual leave days do employees get?"

response = requests.post(f"{API}/ask", json={"question": QUESTION}, timeout=120)
data = response.json()

test_case = LLMTestCase(
    input=QUESTION,
    actual_output=data["answer"],
    retrieval_context=[hit["text"] for hit in data["hits"]],
)

judge = OllamaModel(model="llama3.1:8b", temperature=0)
metric = FaithfulnessMetric(model=judge, threshold=0.7, async_mode=False, verbose_mode=True)
metric.measure(test_case)

print("Answer:", data["answer"])
print("Score:", metric.score)
print("Reason:", metric.reason)