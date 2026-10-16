import pandas as pd

def agg_multi_col(df):
    return df.groupby('dept').agg(
        avg_salary=('salary', 'mean'),
        max_salary=('salary', 'max'),
        tenure=('years', 'mean')
    )
