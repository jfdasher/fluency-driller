import pandas as pd

def count_rows_per_group(df):
    return df.groupby('dept').size()
