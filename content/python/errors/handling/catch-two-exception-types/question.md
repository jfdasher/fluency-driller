---
kind: idiom
status: approved
topic: errors/handling
entry_point: safe_parse
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: catch several exception types with one except (A, B) tuple
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Write a function `safe_parse(value)` that tries to return `int(value)`. If either a `ValueError` or a `TypeError` is raised, catch both in a single `except` clause using a tuple of exception types and return `None`.

## Hints
1. Use a try/except block where the except line names both exception types.
2. In Python you can catch multiple exceptions by writing `except (ExcA, ExcB):` with a tuple.
3. Write `except (ValueError, TypeError):` as a single clause and return None inside it.
