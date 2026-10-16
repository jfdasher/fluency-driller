def test_exact_equality():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'score': [72, 85, 90, 96, 78, 97],
        'grade': ['B', 'A', 'B', 'A', 'A', 'C']
    })
    expected = pd.DataFrame({
        'score': [85, 96, 97],
        'grade': ['A', 'A', 'C']
    }, index=[0, 1, 2])
    result = fn(df)
    assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))
