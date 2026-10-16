import heapq

def sort_tasks_by_priority(tasks):
    heap = list(tasks)
    heapq.heapify(heap)
    result = []
    while heap:
        priority, name = heapq.heappop(heap)
        result.append(name)
    return result
