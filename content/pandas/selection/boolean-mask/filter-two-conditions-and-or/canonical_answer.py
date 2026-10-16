import pandas as pd

def filter_two_conditions(df):
    mask = ((df['score'] >= 80) & (df['grade'] == 'A')) | (df['score'] >= 95)
    return df[mask].reset_index(drop=True)
