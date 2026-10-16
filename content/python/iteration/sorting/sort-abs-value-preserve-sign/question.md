---
kind: idiom
status: approved
topic: iteration/sorting
entry_point: sort_abs_value_preserve_sign
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: sort numbers by absolute value with key=abs
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of integers, return a new list sorted by absolute value (ascending), preserving the original sign. When two numbers have the same absolute value, the negative one should come first.

## Hints
1. Use sorted() with a key argument to control ordering.
2. Use a tuple as the key: first sort by abs(x), then by x itself to break ties (negative before positive).
3. Use key=lambda x: (abs(x), x) so that -3 comes before 3 when they tie on absolute value.
