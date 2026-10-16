---
kind: idiom
status: approved
topic: stdlib/collections
entry_point: bfs_level_order
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: use collections.deque.popleft() as an O(1) queue
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of edges representing a tree (as parent-child pairs) and a root node, return the nodes in breadth-first (level) order using a collections.deque with popleft() for O(1) dequeuing.

## Hints
1. Use collections.deque instead of a list to avoid O(n) list.pop(0) calls.
2. Initialize the deque with the root, then repeatedly popleft() and enqueue children.
3. Build an adjacency map from the edges list, then do a standard BFS with deque.popleft().
