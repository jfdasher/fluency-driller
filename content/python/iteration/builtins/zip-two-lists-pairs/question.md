---
kind: idiom
status: approved
topic: iteration/builtins
entry_point: pair_names_scores
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: pair two lists element-wise with zip
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given two lists `names` and `scores`, return a list of tuples pairing each name with its corresponding score using `zip`.

## Hints
1. You need to combine two lists element-wise into tuples.
2. Python's built-in `zip` function takes two iterables and yields tuples of matched elements.
3. Use `list(zip(names, scores))` to produce the final list of tuples.
