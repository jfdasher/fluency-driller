import pandas as pd

def proportions(s: pd.Series) -> pd.Series:
    result = s.value_counts(normalize=True)
    result.name = None
    return result
