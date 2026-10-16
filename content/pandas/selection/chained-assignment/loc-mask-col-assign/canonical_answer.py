import pandas as pd

def promote_seniors(df):
    out = df.copy()
    out.loc[out['age'] >= 65, 'status'] = 'senior'
    return out
