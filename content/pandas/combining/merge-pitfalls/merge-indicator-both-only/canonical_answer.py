import pandas as pd

def ids_in_both(left: pd.DataFrame, right: pd.DataFrame) -> pd.Series:
    merged = pd.merge(left, right, on='id', how='outer', indicator=True)
    both = merged.loc[merged['_merge'] == 'both', 'id']
    return both.sort_values().reset_index(drop=True)
