def test_describe_numeric_exact():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'score': [85.0, 92.0, 78.0, 95.0], 'attempts': [3, 1, 4, 2]})
    expected = df.describe()
    assert_frame_equal(fn(df), expected)
