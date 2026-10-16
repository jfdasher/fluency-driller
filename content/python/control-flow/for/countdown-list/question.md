---
kind: recall
status: retired
topic: control-flow/for
entry_point: countdown
grader: python
modality: code
retired:
  date: 2026-06-24
  reason: >-
    judge demands for-loop construction due to canonical answer, but prompt
    almost invites comprehension one-liner. Question also fails to drill use of
    range() by providing the correct arguments in the question.
provenance:
  model: claude-sonnet-4-6
  source_topic: count down with range(n - 1, -1, -1)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `countdown(n)` that returns a list of integers counting down from `n-1` to `0` (inclusive), using `range(n - 1, -1, -1)`.

## Hints
1. Use a for loop with range that starts at n-1 and stops before -1.
2. range(n - 1, -1, -1) produces n-1, n-2, ..., 1, 0.
3. Append each value of i in the loop to a list and return it.
