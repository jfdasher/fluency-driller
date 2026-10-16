def highest_score(records):
    return max(records, key=lambda r: r['score'])
