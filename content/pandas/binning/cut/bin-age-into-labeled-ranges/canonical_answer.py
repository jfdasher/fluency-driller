import pandas as pd

def bin_age(df):
    out = df.copy()
    out['age_group'] = pd.cut(
        df['age'],
        bins=[0, 18, 35, 60, 100],
        labels=['youth', 'young_adult', 'middle_aged', 'senior']
    )
    return out
