def test_input_not_mutated():
    import pandas as pd
    df = pd.DataFrame({'val': ['3', '7', '1']})
    original_dtype = df['val'].dtype
    fn(df)
    assert df['val'].dtype == original_dtype, 'input df was mutated'
