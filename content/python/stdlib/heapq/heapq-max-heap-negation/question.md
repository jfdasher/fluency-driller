---
kind: idiom
status: approved
topic: stdlib/heapq
entry_point: max_heap_sort
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: simulate a max-heap by negating values
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Using Python's `heapq` module (which only provides a min-heap), implement `max_heap_sort(nums)` that returns a list of the integers from `nums` sorted in **descending** order. Simulate a max-heap by negating values when pushing and popping.

## Hints
1. Python's heapq is a min-heap; to get max-heap behaviour you need to invert the ordering somehow.
2. Push the negation of each value onto the heap, so the smallest negative corresponds to the largest original value.
3. When popping, negate again to recover the original value: `-heapq.heappop(heap)`.
