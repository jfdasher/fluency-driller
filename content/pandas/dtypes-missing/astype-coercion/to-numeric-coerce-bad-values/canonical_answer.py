import pandas as pd

def coerce_numeric_column(df):
    out = df.copy()
    out['value'] = pd.to_numeric(df['value'], errors='coerce')
    return out
