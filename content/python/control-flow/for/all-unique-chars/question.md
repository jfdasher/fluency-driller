---
kind: idiom
status: approved
topic: control-flow/for
entry_point: all_unique
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: detect a no-break loop completion with for-else
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `all_unique(s)` that returns True if every character in the string `s` is unique (appears only once), and False otherwise. Use a for-else construct: break when a duplicate is found, and use the else clause to confirm all characters were unique.

## Hints
1. The else clause of a for loop executes only if the loop was NOT exited via break.
2. Track seen characters in a set; break as soon as you find a character already in the set.
3. Return True in the else clause (loop finished without break = no duplicates found) and False after the loop body (reached only via break).
