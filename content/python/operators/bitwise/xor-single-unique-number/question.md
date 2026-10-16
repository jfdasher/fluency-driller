---
kind: idiom
status: approved
topic: operators/bitwise
entry_point: find_unique
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: find the single unique number by XOR-accumulating the list
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of integers where every integer appears exactly twice except for one, find and return the single integer that appears only once. Use XOR accumulation over the list.

## Hints
1. XOR of a number with itself is 0, and XOR of a number with 0 is the number itself.
2. Start with 0 and XOR every element in the list; duplicate pairs cancel out.
3. Use `functools.reduce` with `operator.xor`, or a simple loop accumulating `result ^= n`.
