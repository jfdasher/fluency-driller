import pandas as pd

def set_multiindex(df):
    return df.set_index(['dept', 'emp_id'])
