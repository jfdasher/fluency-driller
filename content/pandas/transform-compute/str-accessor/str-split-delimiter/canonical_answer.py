import pandas as pd

def split_full_name(df):
    split = df['full_name'].str.split(' ', expand=True)
    out = pd.DataFrame({'first': split[0], 'last': split[1]})
    return out
