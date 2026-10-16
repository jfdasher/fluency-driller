import pandas as pd

def drop_duplicates_keep_last(df):
    return df.drop_duplicates(subset='city', keep='last')
