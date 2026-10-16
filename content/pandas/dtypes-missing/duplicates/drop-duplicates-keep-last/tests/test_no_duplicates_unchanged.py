def test_no_duplicates_unchanged():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'city': ['NYC', 'LAX', 'CHI'],
        'temp': [70, 85, 60]
    })
    expected = df.copy()
    assert_frame_equal(fn(df), expected)
