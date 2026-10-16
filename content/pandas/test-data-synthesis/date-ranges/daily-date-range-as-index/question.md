---
kind: recall
status: approved
topic: test-data-synthesis/date-ranges
entry_point: make_daily_frame
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: create a daily date_range and use it as a DataFrame index
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a start date string `start` (e.g. `'2024-01-01'`) and an integer `n`, create a DataFrame with a daily `DatetimeIndex` of length `n` starting at `start` (index name `'date'`) and a single column `'value'` filled with integers `0` through `n-1`.

Example — `start='2024-01-01'`, `n=3`:

              value   <- columns
            +-------+
  date      |       |
  2024-01-01|     0 |
  2024-01-02|     1 |
  2024-01-03|     2 |
    ^
    +-- DatetimeIndex named 'date', freq='D'

## Hints
1. Use `pd.date_range(start=..., periods=n, freq='D')` to generate n daily timestamps.
2. Pass `name='date'` to `pd.date_range` so the resulting index already carries the correct name.
3. Build the DataFrame with `pd.DataFrame({'value': range(n)}, index=idx)` where `idx` is the DatetimeIndex.
