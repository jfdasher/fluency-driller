import pandas as pd

def sort_mixed(df):
    return df.sort_values(by=['dept', 'salary'], ascending=[True, False])
