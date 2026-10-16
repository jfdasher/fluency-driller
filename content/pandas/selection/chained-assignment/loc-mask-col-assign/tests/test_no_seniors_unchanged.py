def test_no_seniors_unchanged():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'age': [10, 20, 30],
        'status': ['junior', 'junior', 'junior']
    })
    expected = pd.DataFrame({
        'age': [10, 20, 30],
        'status': ['junior', 'junior', 'junior']
    })
    assert_frame_equal(fn(df), expected)
