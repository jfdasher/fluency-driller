def sort_abs_value_preserve_sign(numbers):
    return sorted(numbers, key=lambda x: (abs(x), x))
