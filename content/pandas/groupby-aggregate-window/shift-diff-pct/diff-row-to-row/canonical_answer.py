import pandas as pd

def add_price_delta(df):
    out = df.copy()
    out['delta'] = df['price'].diff()
    return out
