---
kind: idiom
status: approved
topic: iteration/sorting
entry_point: partition_and_sort_abs
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
Given a list of integers, return a dict with two keys: 'positives' mapped to the non-negative numbers sorted by absolute value ascending, and 'negatives' mapped to the negative numbers sorted by absolute value ascending (i.e., closest to zero first).

## Hints
1. Split numbers into two lists using list comprehensions, then sort each with sorted().
2. Use key=abs when sorting each sublist so they are ordered by absolute value.
3. Return {'positives': sorted([x for x in numbers if x >= 0], key=abs), 'negatives': sorted([x for x in numbers if x < 0], key=abs)}.
