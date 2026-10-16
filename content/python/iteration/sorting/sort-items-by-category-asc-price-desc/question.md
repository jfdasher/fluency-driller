---
kind: idiom
status: approved
topic: iteration/sorting
entry_point: sort_items_by_category_asc_price_desc
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: stable two-pass sort with mixed ascending/descending keys
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a list of dicts, each with keys 'name', 'category', and 'price', sort them so items are grouped by category in ascending alphabetical order. Within each category, items with a higher price come first. Use a stable two-pass sort: first sort by price descending, then sort by category ascending.

## Hints
1. A stable two-pass sort lets you achieve a multi-key sort without a tuple key: sort by the secondary criterion first, then by the primary criterion.
2. Sort by price descending first (so within each category the expensive items are already ordered), then sort by category ascending (stability keeps the price order intact).
3. sorted(items, key=lambda x: x['price'], reverse=True) then sorted(result, key=lambda x: x['category']).
