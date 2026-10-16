import pandas as pd

def promote_city_index(df):
    return df.set_index('city')
