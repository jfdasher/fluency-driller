import pandas as pd

def groupby_mean(df):
    return df.groupby('team')['score'].mean()
