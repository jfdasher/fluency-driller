---
kind: recall
status: approved
topic: construction-inspection/value-counts
entry_point: count_distinct_cities
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: count the distinct values in a column with nunique
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given the DataFrame `df` below, return the number of distinct values in the `'city'` column as a plain Python `int`.

```
   city
0  Paris
1  London
2  Paris
3  Berlin
4  London
5  Paris
```

## Hints
1. You need to find how many unique values appear in a single column — consider a Series method that counts unique elements.
2. The Series method `nunique()` returns the number of distinct non-NaN values; remember to cast the result to `int`.
3. `df['city'].nunique()` gives the count directly; wrap it with `int()` to satisfy the return-type requirement.
