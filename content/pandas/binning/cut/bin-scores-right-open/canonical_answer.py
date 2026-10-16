import pandas as pd

def bin_scores(df):
    out = df.copy()
    out['grade'] = pd.cut(
        df['score'],
        bins=[0, 60, 70, 80, 90, 100],
        labels=['F', 'D', 'C', 'B', 'A'],
        right=False,
        include_lowest=True
    )
    return out
