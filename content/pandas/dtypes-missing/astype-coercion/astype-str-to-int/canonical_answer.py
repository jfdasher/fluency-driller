import pandas as pd

def cast_val_to_int(df):
    out = df.copy()
    out['val'] = df['val'].astype('int64')
    return out
