def count_digits(n):
    counts = {}
    for ch in str(n):
        counts[ch] = counts.get(ch, 0) + 1
    return counts
