---
kind: idiom
status: approved
topic: comprehensions/basic
entry_point: even_squares
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: return squares of the even numbers with a list comprehension
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `even_squares(nums)` that takes a list of integers and returns a new list containing the squares of only the even numbers, using a list comprehension.

## Hints
1. Use a list comprehension with a filtering condition: `[expr for x in nums if condition]`.
2. The condition to keep only even numbers is `x % 2 == 0`, and the expression to square is `x ** 2`.
3. Combine both: `[x ** 2 for x in nums if x % 2 == 0]`.
