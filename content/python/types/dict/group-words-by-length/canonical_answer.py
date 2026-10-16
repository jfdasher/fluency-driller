def group_words_by_length(words):
    result = {}
    for word in words:
        result.setdefault(str(len(word)), []).append(word)
    return result
