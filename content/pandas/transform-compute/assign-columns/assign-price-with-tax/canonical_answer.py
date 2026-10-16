import pandas as pd

def add_price_with_tax(df):
    return df.assign(price_with_tax=lambda d: d['price'] * (1 + d['tax_rate']))
