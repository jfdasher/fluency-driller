---
kind: idiom
status: approved
topic: reshaping/melt
entry_point: melt_subset
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: melt only a subset of measure columns while keeping the id columns
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given `df` with columns `id`, `name`, `q1`, `q2`, `q3`, melt **only** the `q1` and `q2` columns into long form (keeping `id` and `name` as identifier columns), naming the new indicator column `'quarter'` and the new value column `'score'`. Return the resulting DataFrame with the default integer index.

```
   id  name   q1   q2   q3
+----+------+----+----+----+
0|  1 | Ada  | 10 | 20 | 30 |
1|  2 | Bob  | 40 | 50 | 60 |
```

Expected result (row order matches pandas default melt order — id vars repeated, value_vars cycled):

```
   id  name quarter  score
+----+------+-------+------+
0|  1 | Ada  |  q1   |  10  |
1|  2 | Bob  |  q1   |  40  |
2|  1 | Ada  |  q2   |  20  |
3|  2 | Bob  |  q2   |  50  |
```

Note: `q3` must **not** appear in the output.

## Hints
1. Use `pd.DataFrame.melt` with both `id_vars` and `value_vars` keyword arguments.
2. Pass `var_name='quarter'` and `value_name='score'` to name the new indicator and value columns; only list `['q1', 'q2']` in `value_vars`.
3. `df.melt(id_vars=['id', 'name'], value_vars=['q1', 'q2'], var_name='quarter', value_name='score')` gives the answer; call `.reset_index(drop=True)` to get a clean 0-based index.
