def test_no_duplicates_unchanged():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Carol'],
        'score': [90, 85, 78]
    })
    expected = df.copy()
    assert_frame_equal(fn(df), expected)
