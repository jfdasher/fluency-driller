---
kind: recall
status: approved
topic: types/set
entry_point: set_ops
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: compute intersection, union, and difference with set operators
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two lists `a` and `b`, return a dict with keys 'intersection', 'union', and 'difference' whose values are **sorted lists** representing: elements in both a and b, elements in either a or b, and elements in a but not b — computed using set operators (&, |, -).

## Hints
1. Convert both lists to sets, then use &, |, and - operators between them.
2. sa & sb gives common elements, sa | sb gives all elements, sa - sb gives elements only in sa.
3. Wrap each set result in sorted() to produce a sorted list before storing in the dict.
