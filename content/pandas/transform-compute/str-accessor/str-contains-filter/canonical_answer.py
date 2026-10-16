import pandas as pd

def filter_error_rows(df):
    mask = df['message'].str.contains('error', case=False, na=False)
    return df[mask]
