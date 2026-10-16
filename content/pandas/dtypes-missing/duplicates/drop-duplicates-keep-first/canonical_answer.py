import pandas as pd

def drop_duplicates_keep_first(df):
    return df.drop_duplicates(keep='first')
