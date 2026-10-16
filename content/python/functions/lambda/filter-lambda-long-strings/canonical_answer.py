def keep_long(words, min_len):
    return list(filter(lambda w: len(w) > min_len, words))
