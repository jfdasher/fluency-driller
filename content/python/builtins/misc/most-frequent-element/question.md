---
kind: idiom
status: approved
topic: builtins/misc
entry_point: most_frequent
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: find the element with the largest computed key using max(key=...)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a non-empty list of integers, return the element that appears most often. If there is a tie, return whichever `max` naturally picks. Use `max` with a `key` argument.

## Hints
1. You want the element whose frequency (count in the list) is highest — think about what method tells you how many times a value appears.
2. `max` accepts `key=` to transform each element before comparison; pass a callable that counts occurrences.
3. Use `max(nums, key=nums.count)` to find the element with the highest count.
