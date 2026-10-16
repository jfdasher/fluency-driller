---
kind: recall
status: approved
topic: test-data-synthesis/date-ranges
entry_point: generate_month_periods
grader: python
modality: code
provenance:
  model: claude-sonnet-4-6
  source_topic: generate month-start periods with period_range
  verified:
    ok: true
    attempts: 1
    failures: []
---
## Prompt
Given a start string `'2023-01'`, an end string `'2023-06'`, and a frequency `'MS'`... wait — use `pd.period_range` with `freq='M'` to generate a PeriodIndex of month-start periods.

Return a `pd.PeriodIndex` covering every month from `start` to `end` (inclusive) at monthly (`'M'`) frequency.

Example: `generate_month_periods('2023-01', '2023-06')` should return a PeriodIndex like:

```
PeriodIndex(['2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06'], dtype='period[M]')
```

## Hints
1. pandas has a dedicated function for creating ranges of Period objects — look for something analogous to `date_range` but for periods.
2. `pd.period_range(start=..., end=..., freq=...)` builds a PeriodIndex; the monthly frequency string for periods is `'M'`.
3. The exact call is `pd.period_range(start=start, end=end, freq='M')` — both endpoints are included automatically.
