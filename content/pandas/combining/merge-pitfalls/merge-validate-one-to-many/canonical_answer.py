import pandas as pd

def merge_one_to_many(left, right):
    return pd.merge(left, right, on='dept_id', how='left', validate='1:m')
