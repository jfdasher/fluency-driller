import pandas as pd

def select_rows_cols(df):
    return df.loc[['b', 'd'], ['x', 'z']]
