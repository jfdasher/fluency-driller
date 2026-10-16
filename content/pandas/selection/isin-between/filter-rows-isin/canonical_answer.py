import pandas as pd

def filter_rows_isin(df):
    return df[df['category'].isin({'B', 'D'})].copy()
