def remove_banned(banned: list, words: list) -> list:
    banned_set = set(banned)
    return [w for w in words if w not in banned_set]
