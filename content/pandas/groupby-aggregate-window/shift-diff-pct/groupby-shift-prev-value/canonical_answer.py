import pandas as pd

def add_prev_value(df):
    out = df.copy()
    out['prev_value'] = df.groupby('group')['value'].shift(1)
    return out
