def first_mismatch_index(a, b):
    for i, val in enumerate(a):
        if val != b[i]:
            return i
    return -1
