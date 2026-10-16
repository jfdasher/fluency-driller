import pandas as pd

def melt_subset(df: pd.DataFrame) -> pd.DataFrame:
    return df.melt(
        id_vars=['id', 'name'],
        value_vars=['q1', 'q2'],
        var_name='quarter',
        value_name='score'
    ).reset_index(drop=True)
