from collections import Counter

def top_n_common_numbers(numbers, n):
    return [num for num, count in Counter(numbers).most_common(n)]
