from collections import deque

def process_tasks(tasks, cancellations):
    queue = deque(tasks)
    cancelled = set(cancellations)
    result = []
    while queue:
        task = queue.popleft()
        if task not in cancelled:
            result.append(task)
    return result
