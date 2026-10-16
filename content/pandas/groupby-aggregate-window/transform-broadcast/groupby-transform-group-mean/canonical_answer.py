import pandas as pd

def add_group_mean(df):
    out = df.copy()
    out['group_mean_score'] = df.groupby('category')['score'].transform('mean')
    return out
