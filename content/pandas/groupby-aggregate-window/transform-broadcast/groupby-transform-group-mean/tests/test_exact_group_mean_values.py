def test_exact_group_mean_values():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'category': ['A', 'B', 'A', 'B', 'A'],
        'score': [10, 20, 30, 40, 50]
    })
    expected = pd.DataFrame({
        'category': ['A', 'B', 'A', 'B', 'A'],
        'score': [10, 20, 30, 40, 50],
        'group_mean_score': [30.0, 30.0, 30.0, 30.0, 30.0]
    })
    assert_frame_equal(fn(df), expected)
