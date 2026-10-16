def test_exact_melt_subset():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'id': [1, 2],
        'name': ['Ada', 'Bob'],
        'q1': [10, 40],
        'q2': [20, 50],
        'q3': [30, 60]
    })
    expected = pd.DataFrame({
        'id': pd.array([1, 2, 1, 2], dtype='int64'),
        'name': ['Ada', 'Bob', 'Ada', 'Bob'],
        'quarter': ['q1', 'q1', 'q2', 'q2'],
        'score': pd.array([10, 40, 20, 50], dtype='int64')
    })
    assert_frame_equal(fn(df), expected, check_like=False)
