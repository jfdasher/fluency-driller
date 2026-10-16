def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'name': ['Alice', 'Bob', 'Carol', 'Dave'], 'score': [82, 55, 91, 70]})
    original_len = len(df)
    original_cols = list(df.columns)
    fn(df, 70)
    assert len(df) == original_len
    assert list(df.columns) == original_cols
