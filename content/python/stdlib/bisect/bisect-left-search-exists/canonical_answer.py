import bisect

def exists_in_sorted(sorted_list, target):
    idx = bisect.bisect_left(sorted_list, target)
    return idx < len(sorted_list) and sorted_list[idx] == target
