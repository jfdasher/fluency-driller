---
kind: idiom
status: approved
topic: control-flow/while
entry_point: is_palindrome
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: converge two pointers with a while-loop condition
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `is_palindrome(s)` that uses two pointers converging from both ends of the string with a while-loop to determine if the string is a palindrome. Return True if it is, False otherwise.

## Hints
1. Start with one pointer at index 0 and another at len(s)-1, then move them toward each other.
2. The while condition should keep looping as long as the left pointer is strictly less than the right pointer.
3. Inside the loop, compare s[left] and s[right]; if they differ return False, otherwise increment left and decrement right.
