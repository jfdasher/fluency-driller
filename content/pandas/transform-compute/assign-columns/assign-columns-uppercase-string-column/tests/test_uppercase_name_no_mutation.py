def test_uppercase_name_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'name': ['alice', 'bob', 'carol'], 'score': [85, 92, 78]})
    original_names = df['name'].tolist()
    fn(df)
    assert df['name'].tolist() == original_names, 'Input df should not be mutated'
