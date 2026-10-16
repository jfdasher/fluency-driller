---
kind: idiom
status: approved
topic: gotchas/evaluation-order
entry_point: fib
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: roll the Fibonacci pair forward with a, b = b, a + b in one assignment
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Implement `fib(n)` that returns the n-th Fibonacci number (0-indexed, so `fib(0)==0`, `fib(1)==1`, `fib(2)==1`, …) using the idiom `a, b = b, a + b` inside a loop — no recursion, no list.

## Hints
1. Start with `a, b = 0, 1` and loop `n` times; after the loop `a` holds the answer.
2. Inside the loop use exactly one statement: `a, b = b, a + b`. Python evaluates the whole right-hand side before any assignment happens.
3. Loop `for _ in range(n): a, b = b, a + b` and return `a`. The simultaneous swap ensures `a+b` uses the *old* `a`.
