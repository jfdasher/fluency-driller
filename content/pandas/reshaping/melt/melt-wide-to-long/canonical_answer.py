import pandas as pd

def melt_scores(df):
    return df.melt(
        id_vars='student',
        value_vars=['q1', 'q2', 'q3'],
        var_name='quarter',
        value_name='score'
    ).reset_index(drop=True)
