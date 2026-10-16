import bisect

def insertion_point(sorted_list, target):
    return bisect.bisect_left(sorted_list, target)
