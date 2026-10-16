---
kind: idiom
status: approved
topic: control-flow/for
entry_point: pairwise_sum
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: walk two sequences together with zip
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two lists of integers `a` and `b` of equal length, return a new list where each element is the sum of the corresponding elements from `a` and `b`. Use `zip` to walk both sequences together.

## Hints
1. You need to combine elements at the same position from both lists.
2. `zip(a, b)` produces pairs `(a[i], b[i])` that you can iterate over in a for loop or comprehension.
3. Use `[x + y for x, y in zip(a, b)]` to produce the result list.
