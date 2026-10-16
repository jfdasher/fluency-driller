def group_numbers_by_parity(numbers):
    result = {}
    for n in numbers:
        key = 'even' if n % 2 == 0 else 'odd'
        result.setdefault(key, []).append(n)
    return result
