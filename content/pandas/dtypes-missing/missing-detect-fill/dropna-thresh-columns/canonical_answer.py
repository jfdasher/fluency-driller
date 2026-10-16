import pandas as pd

def drop_sparse_columns(df):
    return df.dropna(axis=1, thresh=3)
