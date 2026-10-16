import pandas as pd

def inner_join_on_id(left, right):
    return pd.merge(left, right, on='id', how='inner')
