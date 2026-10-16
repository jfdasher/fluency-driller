---
kind: idiom
status: approved
topic: combining/concat
entry_point: stack_frames
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: stack two DataFrames row-wise with concat(ignore_index=True)
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given two DataFrames `top` and `bottom` with the same columns, stack them row-wise (top above bottom) and reset the index so it runs 0, 1, 2, … continuously. Return the resulting DataFrame.

`top`:

       name  score
     +------+-----+
  0  | Alice|  85 |
  1  |  Bob |  90 |

`bottom`:

       name  score
     +------+-----+
  0  | Carol|  78 |
  1  | Dave |  92 |

Expected result:

       name  score
     +------+-----+
  0  | Alice|  85 |
  1  |  Bob |  90 |
  2  | Carol|  78 |
  3  | Dave |  92 |

## Hints
1. Use `pd.concat` to combine a list of DataFrames vertically.
2. Pass `ignore_index=True` to `pd.concat` so the resulting index is reset to 0, 1, 2, …
3. `pd.concat([top, bottom], ignore_index=True)` stacks the two frames row-wise and resets the index.
