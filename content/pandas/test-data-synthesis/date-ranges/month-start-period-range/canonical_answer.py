import pandas as pd

def generate_month_periods(start: str, end: str) -> pd.PeriodIndex:
    return pd.period_range(start=start, end=end, freq='M')
