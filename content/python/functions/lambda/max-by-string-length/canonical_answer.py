def longest_string(words):
    return max(words, key=lambda w: len(w))
