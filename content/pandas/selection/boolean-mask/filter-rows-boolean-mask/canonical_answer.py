import pandas as pd

def filter_above_threshold(df, threshold):
    return df[df['score'] > threshold].reset_index(drop=True)
