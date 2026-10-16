def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'score': [72, 85, 90, 96, 78, 97],
        'grade': ['B', 'A', 'B', 'A', 'A', 'C']
    })
    original_index = df.index.tolist()
    original_len = len(df)
    fn(df)
    assert len(df) == original_len
    assert df.index.tolist() == original_index
