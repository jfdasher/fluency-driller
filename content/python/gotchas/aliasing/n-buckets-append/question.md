---
kind: idiom
status: approved
topic: gotchas/aliasing
entry_point: fill_buckets
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: create n independent buckets then append to one — the [[]]*n trap
    shares a single list
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given an integer n and a list of (bucket_index, value) pairs, create n independent empty-list buckets and append each value to its corresponding bucket. Return the list of buckets. Do NOT use `[[]] * n` — that shares a single list object. Use a list comprehension or loop to create independent lists.

## Hints
1. Hint 1: Build the initial bucket list with a list comprehension: `[[] for _ in range(n)]`.
2. Hint 2: `[[]] * n` makes n references to the SAME list, so appending to one appends to all. A comprehension creates a fresh list each iteration.
3. Hint 3: `buckets = [[] for _ in range(n)]` then `for idx, val in pairs: buckets[idx].append(val)` is the correct pattern.
