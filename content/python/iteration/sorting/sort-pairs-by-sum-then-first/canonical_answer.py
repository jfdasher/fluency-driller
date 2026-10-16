def sort_pairs_by_sum_then_first(pairs):
    return sorted(pairs, key=lambda p: (p[0] + p[1], p[0]))
