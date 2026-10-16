import pandas as pd

def fill_score(df):
    out = df.copy()
    out['score'] = out['score'].fillna(0)
    return out
