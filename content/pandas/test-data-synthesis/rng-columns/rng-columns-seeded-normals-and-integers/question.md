---
kind: recall
status: approved
topic: test-data-synthesis/rng-columns
entry_point: build_rng_df
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: build a DataFrame of seeded random normals and integers with default_rng
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Using `numpy.random.default_rng(seed=42)`, build a DataFrame with 5 rows and two columns:
- `'score'`: 5 standard-normal floats drawn with `rng.standard_normal(5)`
- `'count'`: 5 integers drawn uniformly from [0, 10) with `rng.integers(0, 10, size=5)`

Return the resulting DataFrame (int column dtype must be `int64`).

Expected result (values come from seed=42):

       score  count
     +-------+------+
  0  |  ...  |  ... |
  1  |  ...  |  ... |
  2  |  ...  |  ... |
  3  |  ...  |  ... |
  4  |  ...  |  ... |

Write a function `build_rng_df()` that takes no arguments and returns this DataFrame.

## Hints
1. Use `np.random.default_rng(seed=42)` to create the generator, then call its `.standard_normal()` and `.integers()` methods in that order.
2. Call `rng.standard_normal(5)` first to get the score column, then `rng.integers(0, 10, size=5)` for the count column — order matters because the RNG state advances with each call.
3. Build the DataFrame as `pd.DataFrame({'score': rng.standard_normal(5), 'count': rng.integers(0, 10, size=5)})` using the same `rng` object; `.integers()` returns `int64` by default on most platforms, but cast with `.astype('int64')` if needed.
