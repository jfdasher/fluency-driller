---
kind: idiom
status: approved
topic: stdlib/bisect
entry_point: exists_in_sorted
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: find a sorted insertion point with bisect_left
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a sorted list of integers and a target, return `True` if the target exists in the list, using `bisect.bisect_left` to locate it efficiently (do NOT use the `in` operator or `list.index`).

## Hints
1. `bisect.bisect_left` returns the index where `target` would be inserted; if `target` is present, it returns the index of its leftmost occurrence.
2. After finding the index with `bisect_left`, check that the index is within bounds and that the element at that index equals the target.
3. Return `idx < len(sorted_list) and sorted_list[idx] == target` where `idx = bisect.bisect_left(sorted_list, target)`.
