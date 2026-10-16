def test_merge_validate_1m_no_mutation():
    import pandas as pd
    left = pd.DataFrame({'dept_id': [1, 2], 'dept_name': ['Engineering', 'Marketing']})
    right = pd.DataFrame({'dept_id': [1, 1, 2], 'employee': ['Alice', 'Bob', 'Carol']})
    left_cols_before = list(left.columns)
    right_cols_before = list(right.columns)
    fn(left, right)
    assert list(left.columns) == left_cols_before
    assert list(right.columns) == right_cols_before
