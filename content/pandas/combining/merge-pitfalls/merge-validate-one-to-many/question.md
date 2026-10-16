---
kind: idiom
status: approved
topic: combining/merge-pitfalls
entry_point: merge_one_to_many
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: assert a one-to-many relationship with merge(validate='1:m')
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a left DataFrame `left` and a right DataFrame `right`, merge them on `'dept_id'` with a left join and assert a one-to-many relationship (each `dept_id` in `left` appears at most once) using `validate='1:m'`. Return the merged DataFrame.

`left`:

   dept_id  dept_name
+--------+----------+
0 |      1 | Engineering |
1 |      2 | Marketing   |

`right`:

   dept_id  employee
+--------+---------+
0 |      1 | Alice   |
1 |      1 | Bob     |
2 |      2 | Carol   |

Return the result of the validated merge.

## Hints
1. Use `pd.merge()` with `how='left'` and the `on` parameter set to `'dept_id'`.
2. Pass `validate='1:m'` to `pd.merge()` to enforce that the left key is unique; it raises `MergeError` if not.
3. The full call is `pd.merge(left, right, on='dept_id', how='left', validate='1:m')`.
