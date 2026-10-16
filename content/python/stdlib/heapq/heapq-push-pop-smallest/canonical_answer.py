import heapq

def push_pop_smallest(nums, val):
    heapq.heapify(nums)
    heapq.heappush(nums, val)
    return heapq.heappop(nums)
