import pandas as pd

def merge_with_suffixes(left, right):
    return pd.merge(left, right, on='id', suffixes=('_left', '_right'))
