import pandas as pd

def uppercase_name_column(df):
    out = df.copy()
    out['name'] = df['name'].str.upper()
    return out
