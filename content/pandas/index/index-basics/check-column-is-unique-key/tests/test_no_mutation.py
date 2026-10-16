def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'id': [10, 20, 30], 'name': ['X', 'Y', 'Z']})
    original_ids = df['id'].tolist()
    fn(df)
    assert df['id'].tolist() == original_ids
