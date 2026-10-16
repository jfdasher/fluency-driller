---
kind: idiom
status: approved
topic: stdlib/collections
entry_point: top_n_common_numbers
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: get the n most common items with Counter.most_common
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of integers and an integer n, return just the n most common integer values (not their counts) as a list, ordered from most to least common. Use Counter.most_common.

## Hints
1. Counter.most_common(n) returns a list of (element, count) tuples — you only need the elements.
2. Use a list comprehension to unpack just the first item from each (element, count) tuple.
3. Try: [num for num, count in Counter(numbers).most_common(n)]
