import pandas as pd

def check_unique_key(df: pd.DataFrame) -> bool:
    return df['id'].is_unique
