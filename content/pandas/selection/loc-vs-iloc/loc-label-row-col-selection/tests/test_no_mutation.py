def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame(
        {'x': [1, 4, 7, 10], 'y': [2, 5, 8, 11], 'z': [3, 6, 9, 12]},
        index=['a', 'b', 'c', 'd']
    )
    original_shape = df.shape
    original_cols = list(df.columns)
    original_index = list(df.index)
    fn(df)
    assert df.shape == original_shape
    assert list(df.columns) == original_cols
    assert list(df.index) == original_index
