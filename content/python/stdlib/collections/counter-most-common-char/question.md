---
kind: idiom
status: approved
topic: stdlib/collections
entry_point: most_common_char
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: tally items with collections.Counter instead of a manual loop
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a string, return the single most common character. If there is a tie, return the one that appears first when iterating over `Counter.most_common()`. Use `collections.Counter` instead of a manual loop.

## Hints
1. collections.Counter has a most_common(n) method that returns the n most frequent elements as (element, count) pairs.
2. Counter(s).most_common(1) gives a list with one tuple; index [0][0] extracts the character.
3. return Counter(s).most_common(1)[0][0] is the complete idiomatic solution.
