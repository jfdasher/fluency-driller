---
kind: recall
status: approved
topic: stdlib/heapq
entry_point: push_pop_smallest
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: push and pop the smallest element from a min-heap
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of integers `nums`, use Python's `heapq` module to build a min-heap from the list, then push a new value `val` onto it, and return the smallest element after popping it from the heap. The original list may be modified in place.

## Hints
1. Use `heapq.heapify` to convert the list into a valid min-heap in-place before pushing.
2. After heapifying, use `heapq.heappush(nums, val)` to add the new value, then `heapq.heappop(nums)` returns the smallest element.
3. `heapq.heappop` always removes and returns the smallest element from a min-heap; combining heapify + heappush + heappop gives you the minimum of all elements including `val`.
