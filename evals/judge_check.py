import sys

from deepeval.metrics import FaithfulnessMetric
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase

JUDGE_MODEL = sys.argv[1] if len(sys.argv) > 1 else "llama3.1:8b"

CONTEXT = [
    "Permanent employees accrue 22 working days of annual leave per calendar year. "
    "Nimbus does not pay cash in lieu of unused annual leave except on final settlement."
]

CASES = [
    ("good", "22 working days per calendar year.", "high"),
    ("hallucinated", "Employees get 30 days of annual leave.", "low"),
    ("half-wrong", "22 days, and unused days are paid in cash every year.", "middle"),
]

judge = OllamaModel(model=JUDGE_MODEL, temperature=0)
print(f"Judge: {JUDGE_MODEL}\n")

for name, answer, expected in CASES:
    metric = FaithfulnessMetric(model=judge, async_mode=False)
    metric.measure(LLMTestCase(
        input="How many annual leave days do employees get?",
        actual_output=answer,
        retrieval_context=CONTEXT,
    ))
    print(f"{name:13} expected {expected:7} got {metric.score:.2f}")