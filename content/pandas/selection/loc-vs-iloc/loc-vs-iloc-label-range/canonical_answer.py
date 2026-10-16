import pandas as pd

def select_loc_iloc(df):
    loc_result = df.loc['b':'d']
    iloc_result = df.iloc[0:2]
    return (loc_result, iloc_result)
