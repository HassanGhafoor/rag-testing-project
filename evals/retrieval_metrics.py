def recall_at_k(retrieved, relevant, k):
    top_k = retrieved[:k]
    return len(set(top_k) & set(relevant)) / len(relevant)


def precision_at_k(retrieved, relevant, k):
    top_k = retrieved[:k]
    return len(set(top_k) & set(relevant)) / len(top_k)


def reciprocal_rank(retrieved, relevant):
    for rank, chunk_id in enumerate(retrieved, start=1):
        if chunk_id in relevant:
            return 1.0 / rank
    return 0.0