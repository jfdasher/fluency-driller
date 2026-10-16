---
kind: recall
status: approved
topic: stdlib/heapq
entry_point: k_smallest
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
Given a list of integers `nums` and an integer `k`, use `heapq.heappush` and `heapq.heappop` (not `heapq.nsmallest`) to return a list of the `k` smallest elements from `nums` in ascending order.

## Hints
1. Push every element of `nums` onto an initially empty heap using `heapq.heappush`.
2. Once all elements are pushed, call `heapq.heappop` exactly `k` times; each pop yields the current minimum.
3. Collect the `k` popped values into a list and return it — they will naturally come out in ascending order because `heappop` always removes the smallest.
