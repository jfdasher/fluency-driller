import heapq
def top_k_by_abs(nums, k):
    return heapq.nlargest(k, nums, key=abs)
