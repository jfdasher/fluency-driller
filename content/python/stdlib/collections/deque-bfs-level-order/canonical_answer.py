from collections import deque, defaultdict

def bfs_level_order(edges, root):
    children = defaultdict(list)
    for parent, child in edges:
        children[parent].append(child)
    result = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        result.append(node)
        for child in children[node]:
            queue.append(child)
    return result
