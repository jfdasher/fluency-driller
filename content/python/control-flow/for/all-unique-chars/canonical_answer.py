def all_unique(s):
    seen = set()
    for ch in s:
        if ch in seen:
            break
        seen.add(ch)
    else:
        return True
    return False
