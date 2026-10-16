import pandas as pd

def drop_between(df):
    return df[~df['score'].between(40, 70)].reset_index(drop=True)
