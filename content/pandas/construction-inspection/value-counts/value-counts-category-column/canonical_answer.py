import pandas as pd

def count_colors(df):
    return df['color'].value_counts().sort_index().sort_values(ascending=False, kind='stable')
