def test_merge_validate_1m_exact():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    left = pd.DataFrame({'dept_id': [1, 2], 'dept_name': ['Engineering', 'Marketing']})
    right = pd.DataFrame({'dept_id': [1, 1, 2], 'employee': ['Alice', 'Bob', 'Carol']})
    expected = pd.DataFrame({
        'dept_id': pd.array([1, 1, 2], dtype='int64'),
        'dept_name': ['Engineering', 'Engineering', 'Marketing'],
        'employee': ['Alice', 'Bob', 'Carol']
    })
    result = fn(left, right)
    assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))
