---
kind: idiom
status: approved
topic: iteration/sorting
entry_point: sort_strings_by_vowel_count_then_alpha
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: double sort with a lambda as the key
  verified:
    ok: false
    attempts: 2
    failures:
    - 'case 0: expected [''ant'', ''cat'', ''bee'', ''eel'', ''ivy''], got [''ant'',
      ''cat'', ''ivy'', ''bee'', ''eel'']'
    - 'case 1: expected [''red'', ''ace'', ''ox'', ''blue'', ''green''], got [''ox'',
      ''red'', ''ace'', ''blue'', ''green'']'
    - 'case 3: expected [''ear'', ''era'', ''are'', ''area''], got [''are'', ''ear'',
      ''era'', ''area'']'
---
## Prompt
Given a list of lowercase strings, sort them first by the number of vowels (a, e, i, o, u) in ascending order, then alphabetically for strings with the same vowel count. Return the sorted list.

## Hints
1. Use `sorted()` with a `key` argument that returns a tuple.
2. Count vowels with `sum(c in 'aeiou' for c in w)` inside the lambda.
3. Use `key=lambda w: (sum(c in 'aeiou' for c in w), w)` to sort by vowel count first, then alphabetically.
