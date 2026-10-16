from collections import defaultdict

def group_words_by_length(words):
    groups = defaultdict(list)
    for word in words:
        groups[str(len(word))].append(word)
    return dict(groups)
