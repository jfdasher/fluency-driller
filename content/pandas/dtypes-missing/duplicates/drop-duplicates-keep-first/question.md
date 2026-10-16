---
kind: recall
status: approved
topic: dtypes-missing/duplicates
entry_point: drop_duplicates_keep_first
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: drop duplicate rows keeping the first with drop_duplicates
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame with duplicate rows removed, keeping only the first occurrence of each duplicated row (default keep='first').

```
   name  score
0  Alice     90
1    Bob     85
2  Alice     90
3  Carol     78
4    Bob     85
5  Carol     78
```

Expected result:

```
   name  score
0  Alice     90
1    Bob     85
3  Carol     78
```

## Hints
1. Pandas DataFrames have a method specifically for removing duplicate rows.
2. The method is called `drop_duplicates()` and accepts a `keep` parameter to control which occurrence to retain.
3. Call `df.drop_duplicates(keep='first')` to remove duplicate rows while keeping the first occurrence.
