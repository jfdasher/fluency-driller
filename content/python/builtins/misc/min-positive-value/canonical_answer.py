def min_positive(numbers):
    running_min = float('inf')
    for n in numbers:
        if n > 0 and n < running_min:
            running_min = n
    return running_min
