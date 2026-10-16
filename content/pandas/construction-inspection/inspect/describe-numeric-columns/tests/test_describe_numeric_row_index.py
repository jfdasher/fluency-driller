def test_describe_numeric_row_index():
    import pandas as pd
    df = pd.DataFrame({'score': [85.0, 92.0, 78.0, 95.0], 'attempts': [3, 1, 4, 2]})
    result = fn(df)
    assert list(result.index) == ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
