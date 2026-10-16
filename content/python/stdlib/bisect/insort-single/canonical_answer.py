import bisect

def insort_single(sorted_list, value):
    bisect.insort(sorted_list, value)
    return sorted_list
