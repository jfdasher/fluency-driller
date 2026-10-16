---
kind: idiom
status: approved
topic: control-flow/for
entry_point: name_score_dict
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
Given a list of `names` (strings) and a list of `scores` (integers) of equal length, return a dictionary mapping each name to its corresponding score. Use `zip` to walk both sequences together.

## Hints
1. You want to pair each element of `names` with the element at the same position in `scores`.
2. `zip(names, scores)` yields `(name, score)` tuples you can iterate over.
3. Use a dict comprehension: `{name: score for name, score in zip(names, scores)}`.
