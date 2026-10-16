def test_exact_merge_with_suffixes():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    left = pd.DataFrame({'id': [1, 2], 'score': [80, 90]})
    right = pd.DataFrame({'id': [1, 2], 'score': [75, 85]})
    expected = pd.DataFrame({
        'id': pd.array([1, 2], dtype='int64'),
        'score_left': pd.array([80, 90], dtype='int64'),
        'score_right': pd.array([75, 85], dtype='int64'),
    })
    result = fn(left, right)
    assert_frame_equal(result, expected, check_like=False)
