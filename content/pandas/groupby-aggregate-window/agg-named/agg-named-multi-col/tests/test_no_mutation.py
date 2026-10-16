import pandas as pd

def test_no_mutation():
    df = pd.DataFrame({
        'dept': ['A', 'A', 'B', 'B'],
        'salary': [50000, 60000, 70000, 80000],
        'years': [3, 5, 7, 9]
    })
    original_cols = list(df.columns)
    original_len = len(df)
    fn(df)
    assert list(df.columns) == original_cols
    assert len(df) == original_len
