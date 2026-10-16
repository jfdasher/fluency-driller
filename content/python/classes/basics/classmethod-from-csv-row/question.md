---
kind: idiom
status: approved
topic: classes/basics
entry_point: Employee
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: add an alternate constructor with @classmethod
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Define a class `Employee` with `__init__(self, name, department, salary)` that stores those three attributes. Add a `@classmethod` named `from_csv` that accepts a single CSV string like `'Alice,Engineering,95000'` and returns a new `Employee` instance. `salary` should be stored as a `float`.

## Hints
1. Use `str.split(',')` to break the CSV row into its three parts.
2. Remember to convert the salary part to `float` before or inside the constructor call.
3. Use `cls(name, department, salary)` to create and return the instance so subclasses also benefit.
