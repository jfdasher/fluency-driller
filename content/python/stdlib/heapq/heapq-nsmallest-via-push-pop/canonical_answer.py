import heapq

def k_smallest(nums, k):
    heap = []
    for n in nums:
        heapq.heappush(heap, n)
    result = []
    for _ in range(k):
        result.append(heapq.heappop(heap))
    return result
