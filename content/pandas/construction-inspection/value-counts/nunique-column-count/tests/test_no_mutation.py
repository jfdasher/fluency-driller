def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({'city': ['Paris', 'London', 'Paris', 'Berlin', 'London', 'Paris']})
    original_values = df['city'].tolist()
    fn(df)
    assert df['city'].tolist() == original_values
