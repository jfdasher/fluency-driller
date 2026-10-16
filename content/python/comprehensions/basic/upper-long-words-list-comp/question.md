---
kind: idiom
status: approved
topic: comprehensions/basic
entry_point: upper_long_words
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: rewrite a map/filter chain as a comprehension
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Rewrite the following as a single list comprehension (no explicit map/filter calls):

```python
def upper_long_words(words):
    return list(map(lambda w: w.upper(), filter(lambda w: len(w) > 3, words)))
```

The function takes a list of strings and returns an uppercase version of every word that is longer than 3 characters.

## Hints
1. List comprehensions support an `if` guard: `[expr for item in iterable if condition]`.
2. Apply `.upper()` inside the expression part and use `len(w) > 3` as the condition.
3. Write `[w.upper() for w in words if len(w) > 3]`.
