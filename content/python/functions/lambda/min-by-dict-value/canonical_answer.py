def lowest_scorer(scores):
    return min(scores, key=lambda name: scores[name])
