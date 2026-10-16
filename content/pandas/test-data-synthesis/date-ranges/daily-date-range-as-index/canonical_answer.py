import pandas as pd
import numpy as np

def make_daily_frame(start: str, n: int) -> pd.DataFrame:
    idx = pd.date_range(start=start, periods=n, freq='D', name='date')
    return pd.DataFrame({'value': range(n)}, index=idx)
