import heapq

def max_heap_sort(nums):
    heap = []
    for n in nums:
        heapq.heappush(heap, -n)
    result = []
    while heap:
        result.append(-heapq.heappop(heap))
    return result
