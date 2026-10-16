def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'price': [10.0, 15.0, 13.0]})
    original_columns = list(df.columns)
    fn(df)
    assert list(df.columns) == original_columns, 'Input DataFrame was mutated'
