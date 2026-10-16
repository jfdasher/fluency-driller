from collections import Counter

def top_n_common_words(words, n):
    return [list(item) for item in Counter(words).most_common(n)]
