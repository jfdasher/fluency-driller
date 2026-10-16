---
kind: idiom
status: approved
topic: functions/closures
entry_point: collect_leaves
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
Implement `collect_leaves(root)` where each node is a dict with keys 'val' (int) and 'children' (list of nodes). A leaf is a node with no children. Define a nested `dfs()` helper that appends leaf values, in traversal order, to a list captured from the enclosing scope, then return that list. (Appending mutates the list in place, so no `nonlocal` declaration is required.)

## Hints
1. Define a list in the outer function's scope and use a nested dfs() that appends to it when a node has no children.
2. Because `list.append` mutates the list in place (rather than rebinding the name), the nested dfs() can append to the outer `leaves` directly — no `nonlocal` is needed (unlike an integer accumulator, where `total += ...` rebinds and would require it).
3. Check `if not node['children']` to identify a leaf and `leaves.append(node['val'])`, otherwise recurse into each child.
