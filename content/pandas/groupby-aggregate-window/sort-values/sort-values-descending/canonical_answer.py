import pandas as pd

def sort_by_score_desc(df):
    return df.sort_values('score', ascending=False, kind='stable')
