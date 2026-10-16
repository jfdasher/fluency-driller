def fill_buckets(n, pairs):
    buckets = [[] for _ in range(n)]
    for idx, val in pairs:
        buckets[idx].append(val)
    return buckets
