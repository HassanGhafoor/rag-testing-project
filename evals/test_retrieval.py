import json
from pathlib import Path

import pytest
import requests

from retrieval_metrics import precision_at_k, recall_at_k, reciprocal_rank

API = "http://127.0.0.1:8000"
K = 3
GOLDEN = json.loads(Path("golden/golden.json").read_text())
ANSWERABLE = [c for c in GOLDEN if c["answerable"]]
UNANSWERABLE = [c for c in GOLDEN if not c["answerable"]]

RECALL_THRESHOLD = 0.8
MRR_THRESHOLD = 0.7



def retrieve(question, k=K):
    response = requests.post(f"{API}/retrieve", json={"question": question, "k": k}, timeout=30)
    response.raise_for_status()
    return response.json()["hits"]


KNOWN_FAILURES = {}


def as_params(cases):
    params = []
    for c in cases:
        marks = []
        if c["id"] in KNOWN_FAILURES:
            marks.append(pytest.mark.xfail(reason=KNOWN_FAILURES[c["id"]], strict=True))
        params.append(pytest.param(c, id=c["id"], marks=marks))
    return params


@pytest.mark.parametrize("case", as_params(ANSWERABLE))
def test_relevant_chunk_in_top_k(case):
    retrieved = [h["id"] for h in retrieve(case["question"])]
    assert recall_at_k(retrieved, case["expectedChunkIds"], K) > 0, (
        f"{case['id']}: none of {case['expectedChunkIds']} in top {K}: {retrieved}"
    )


def test_aggregate_retrieval_quality_gate():
    recalls, precisions, rrs = [], [], []
    for case in ANSWERABLE:
        retrieved = [h["id"] for h in retrieve(case["question"])]
        relevant = case["expectedChunkIds"]
        recalls.append(recall_at_k(retrieved, relevant, K))
        precisions.append(precision_at_k(retrieved, relevant, K))
        rrs.append(reciprocal_rank(retrieved, relevant))

    mean_recall = sum(recalls) / len(recalls)
    mean_precision = sum(precisions) / len(precisions)
    mrr = sum(rrs) / len(rrs)
    print(f"\nRecall@{K}={mean_recall:.2f}  Precision@{K}={mean_precision:.2f}  MRR={mrr:.2f}")

    assert mean_recall >= RECALL_THRESHOLD, f"Recall@{K} {mean_recall:.2f} below {RECALL_THRESHOLD}"
    assert mrr >= MRR_THRESHOLD, f"MRR {mrr:.2f} below {MRR_THRESHOLD}"


@pytest.mark.xfail(strict=True, reason=(
    "Known finding: answerable and unanswerable best-match distances overlap, "
    "so no fixed threshold separates them. Distance is a soft signal; "
    "refusal is handled by the grounded LLM prompt."
))
def test_distance_separates_answerable_from_unanswerable():
    rows = []
    for case in GOLDEN:
        best = retrieve(case["question"])[0]["distance"]
        rows.append((best, case["id"], case["answerable"]))
    rows.sort()

    print("\nBest-match distance (lower = closer):")
    for best, cid, answerable in rows:
        label = "answerable" if answerable else "UNANSWERABLE"
        print(f"  {best:.3f}  {cid}  {label}")

    worst_answerable = max(d for d, _, a in rows if a)
    best_unanswerable = min(d for d, _, a in rows if not a)
    assert worst_answerable < best_unanswerable, (
        f"Overlap: an answerable question scored {worst_answerable:.3f}, "
        f"weaker than the unanswerable one at {best_unanswerable:.3f}"
    )