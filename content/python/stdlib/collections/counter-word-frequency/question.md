---
kind: idiom
status: approved
topic: stdlib/collections
entry_point: word_frequency
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
Given a list of words, return a dict mapping each word to the number of times it appears. Use `collections.Counter` instead of a manual loop.

## Hints
1. collections.Counter accepts any iterable and tallies elements automatically.
2. Counter(words) returns a Counter object; convert it to a plain dict with dict().
3. return dict(Counter(words)) is the complete idiomatic solution.
