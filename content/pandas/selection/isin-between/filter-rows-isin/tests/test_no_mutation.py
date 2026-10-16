def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'category': ['A', 'B', 'C', 'D', 'B', 'A'], 'value': [10, 20, 30, 40, 50, 60]})
    original_len = len(df)
    original_cats = df['category'].tolist()
    fn(df)
    assert len(df) == original_len
    assert df['category'].tolist() == original_cats
