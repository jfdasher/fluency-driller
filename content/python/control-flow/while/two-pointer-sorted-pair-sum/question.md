---
kind: idiom
status: approved
topic: control-flow/while
entry_point: find_pair
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
Write a function `find_pair(nums, target)` that takes a sorted list of integers and a target integer, and uses two converging pointers in a while-loop to find and return a list `[left_val, right_val]` (in that order) whose sum equals the target. Return an empty list if no such pair exists. Assume at most one valid pair.

## Hints
1. Initialize left=0 and right=len(nums)-1, then move them inward based on whether the current sum is too small or too large.
2. If nums[left]+nums[right] < target, move left forward; if it's greater, move right backward; if equal, you found the pair.
3. The while condition is `left < right`; when they meet without a match, return an empty list.
