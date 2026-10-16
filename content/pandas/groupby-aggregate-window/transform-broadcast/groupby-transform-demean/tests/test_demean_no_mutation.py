def test_demean_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'group': ['A', 'B', 'A', 'B', 'A'], 'value': [10, 20, 30, 40, 50]})
    original_cols = list(df.columns)
    _ = fn(df)
    assert list(df.columns) == original_cols
    assert list(df['value']) == [10, 20, 30, 40, 50]
