import pandas as pd

def flag_duplicate_rows_subset(df):
    result = df.duplicated(subset=['name', 'dept'], keep='first')
    result.name = 'is_dup'
    return result
