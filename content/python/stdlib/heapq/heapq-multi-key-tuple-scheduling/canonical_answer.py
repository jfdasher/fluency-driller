import heapq

def schedule_jobs(jobs):
    heap = [(job['priority'], job['arrival'], job['name']) for job in jobs]
    heapq.heapify(heap)
    result = []
    while heap:
        priority, arrival, name = heapq.heappop(heap)
        result.append(name)
    return result
