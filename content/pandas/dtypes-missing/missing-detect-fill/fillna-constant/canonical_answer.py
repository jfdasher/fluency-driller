import pandas as pd

def fill_score(df):
    out = df.copy()
    out['score'] = df['score'].fillna(0.0)
    return out
