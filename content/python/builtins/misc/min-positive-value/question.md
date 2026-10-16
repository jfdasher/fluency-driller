---
kind: idiom
status: approved
topic: builtins/misc
entry_point: min_positive
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: initialize a running minimum with float('inf') as a sentinel
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `min_positive(numbers)` that returns the smallest positive (> 0) number in the list, or `float('inf')` if no positive number exists. Initialize your running minimum with `float('inf')` as a sentinel.

## Hints
1. Start with a variable set to float('inf') so any positive number will be smaller than it.
2. Loop through numbers, and for each positive number, update your running minimum if it is smaller than the current minimum.
3. Return the running minimum after the loop; if no positive number was found, it will still be float('inf').
