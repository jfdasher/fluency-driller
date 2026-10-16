import heapq
def top_k_scores(records, k):
    return heapq.nlargest(k, records, key=lambda r: r['score'])
