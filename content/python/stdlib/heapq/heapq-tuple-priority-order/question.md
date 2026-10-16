---
kind: idiom
status: approved
topic: stdlib/heapq
entry_point: sort_tasks_by_priority
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: order a heap by a tuple priority key
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of tasks, each represented as a (priority, task_name) tuple, use heapq to repeatedly pop and return the tasks in ascending priority order (lowest number = highest priority). Return the list of task_name strings in the order they are popped.

## Hints
1. heapq compares tuples element-by-element, so (priority, name) tuples are naturally ordered by priority first.
2. Use heapq.heapify() to convert the list in-place, then heapq.heappop() repeatedly to extract in order.
3. Build a list of (priority, task_name) tuples, heapify it, then pop all items collecting the second element each time.
