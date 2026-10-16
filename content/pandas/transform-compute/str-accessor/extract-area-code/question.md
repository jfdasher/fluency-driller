---
kind: idiom
status: approved
topic: transform-compute/str-accessor
entry_point: extract_area_code
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: pull a substring pattern out of a text column with .str.extract
  verified:
    ok: true
    attempts: 2
    failures: []
---
## Prompt
Given df, return a new DataFrame with a single column `'area_code'` containing the three-digit area code extracted from the `'phone'` column (format `'(NNN) NNN-NNNN'`). The result must be a string (object) dtype column.

```
         phone
      +--------------+
  0   | (212) 555-1234 |
  1   | (415) 867-5309 |
  2   | (312) 999-0000 |
```

Expected output:

```
   area_code
+-----------+
|   212     |
|   415     |
|   312     |
```

## Hints
1. Use the `.str` accessor on the `'phone'` Series to work with string methods.
2. `.str.extract(pattern)` returns a DataFrame of captured groups — use a single capturing group `(...)` around the three digits inside the parentheses.
3. The pattern `r'\((\d{3})\)'` matches a literal `(`, captures three digits, then matches a literal `)`. `.str.extract` returns a one-column DataFrame whose column is `0` by default — use a named group `(?P<area_code>\d{3})` or rename afterwards to get `'area_code'`.
