import pandas as pd

def named_group_agg(df):
    return df.groupby('dept').agg(
        avg_salary=('salary', 'mean'),
        max_years=('years', 'max'),
        headcount=('salary', 'count'),
    )
