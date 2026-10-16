---
kind: idiom
status: approved
topic: stdlib/heapq
entry_point: top_k_scores
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: find the k largest items with heapq.nlargest and a key
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of dicts each with a 'score' key, return the k dicts with the highest 'score' values (in descending order) using heapq.nlargest with a key argument.

## Hints
1. heapq.nlargest(k, iterable, key=...) returns the k largest elements according to the key function.
2. Use a lambda that extracts the 'score' field: key=lambda r: r['score'].
3. heapq.nlargest(k, records, key=lambda r: r['score']) returns the top-k dicts ordered by score descending.
