import pandas as pd

def test_split_full_name_no_mutation():
    df = pd.DataFrame({'full_name': ['Alice Bob', 'Carol Dee']})
    original_cols = list(df.columns)
    fn(df)
    assert list(df.columns) == original_cols
