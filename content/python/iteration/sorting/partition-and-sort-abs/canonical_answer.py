def partition_and_sort_abs(numbers):
    return {
        'positives': sorted([x for x in numbers if x >= 0], key=abs),
        'negatives': sorted([x for x in numbers if x < 0], key=abs)
    }
