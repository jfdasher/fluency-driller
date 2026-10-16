import pandas as pd

def demean_by_group(df):
    demeaned = df['value'] - df.groupby('group')['value'].transform('mean')
    return pd.DataFrame({'value_demeaned': demeaned})
