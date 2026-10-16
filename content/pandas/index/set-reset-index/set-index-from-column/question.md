---
kind: idiom
status: approved
topic: index/set-reset-index
entry_point: promote_city_index
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: promote a column to the row index with set_index
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given the DataFrame `df`, promote the `'city'` column to become the row index and return the resulting frame (the `'city'` column should no longer appear as a regular column).

```
        city  population  area
     +------+----------+------+
  0  |  NYC |   8336817 |  302 |
  1  |   LA |   3979576 |  469 |
  2  |  CHI |   2693976 |  227 |
```

Expected result:

```
            population  area
         +----------+------+
  NYC    |   8336817 |  302 |
  LA     |   3979576 |  469 |
  CHI    |   2693976 |  227 |
    ^
    +-- index.name == 'city'
```

## Hints
1. Think about the DataFrame method that moves a column into the index position.
2. pandas has a method called `set_index` that accepts a column label and promotes it.
3. Use `df.set_index('city')` — it returns a new DataFrame where `'city'` is the index and is removed from the columns.
