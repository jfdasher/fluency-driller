---
kind: idiom
status: approved
topic: stdlib/heapq
entry_point: top_k_by_abs
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: find the k largest items with heapq.nlargest and a key
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of integers, return the k numbers with the largest absolute values (in descending order of absolute value) using heapq.nlargest with a key argument.

## Hints
1. heapq.nlargest accepts an optional key= parameter just like sorted().
2. Pass key=abs to rank items by their absolute value instead of their raw value.
3. heapq.nlargest(k, nums, key=abs) returns the k elements with the biggest abs() values, ordered largest-first.
