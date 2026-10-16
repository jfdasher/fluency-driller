def test_bin_age_no_mutation():
    import pandas as pd

    df = pd.DataFrame({'age': [5, 22, 45, 70, 18]})
    original_cols = list(df.columns)
    fn(df)
    assert list(df.columns) == original_cols, 'Input df should not be mutated'
