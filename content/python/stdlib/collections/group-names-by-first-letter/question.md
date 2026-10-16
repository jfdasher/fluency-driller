---
kind: idiom
status: approved
topic: stdlib/collections
entry_point: group_names_by_first_letter
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: group items with defaultdict(list)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of names, return a dict mapping each first letter (uppercase) to the sorted list of names starting with that letter. Use `defaultdict(list)` to accumulate the names before sorting.

## Hints
1. Use `defaultdict(list)` to append each name under the key `name[0].upper()`.
2. After grouping, sort each list: iterate over the defaultdict items and sort the values.
3. Build the final dict with a dict comprehension: `{k: sorted(v) for k, v in groups.items()}`.
