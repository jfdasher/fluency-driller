---
kind: recall
status: approved
topic: index/set-reset-index
entry_point: set_multiindex
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a two-level MultiIndex with set_index([a, b])
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given df, return a new DataFrame with a two-level MultiIndex built from columns 'dept' and 'emp_id' (in that order), keeping the remaining columns.

     dept  emp_id  salary
  0   eng    101   90000
  1   eng    102   85000
  2   mkt    201   75000
  3   mkt    202   80000

Expected result (dept, emp_id become the index levels):

                  salary
  dept  emp_id
  eng   101     90000
        102     85000
  mkt   201     75000
        202     80000

## Hints
1. Pass a list of column names to set_index to create a MultiIndex.
2. df.set_index(['col_a', 'col_b']) creates a two-level MultiIndex from those two columns.
3. Use df.set_index(['dept', 'emp_id']) — the order in the list determines the outer and inner index levels.
