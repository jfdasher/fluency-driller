import pandas as pd

def count_missing(df):
    return df.isna().sum()
