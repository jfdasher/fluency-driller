---
kind: idiom
status: approved
topic: functions/closures
entry_point: sum_tree
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: define a nested dfs() helper that mutates a nonlocal accumulator
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Implement `sum_tree(root)` where each node is a dict with keys 'val' (int) and 'children' (list of nodes). Define a nested `dfs()` helper that mutates a nonlocal integer accumulator, then return the total sum of all node values.

## Hints
1. You need a variable defined in sum_tree's scope that dfs() can update.
2. Use the `nonlocal` keyword inside dfs() to refer to the outer `total` variable.
3. Declare `total = 0` before defining dfs(), write `nonlocal total` at the top of dfs(), then do `total += node['val']` and recurse on children.
