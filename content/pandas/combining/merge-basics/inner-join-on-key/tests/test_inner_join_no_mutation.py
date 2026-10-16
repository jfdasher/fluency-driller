def test_inner_join_no_mutation():
    import pandas as pd
    left = pd.DataFrame({'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Carol']})
    right = pd.DataFrame({'id': [2, 3, 4], 'score': [88, 95, 70]})
    left_cols_before = list(left.columns)
    right_cols_before = list(right.columns)
    fn(left, right)
    assert list(left.columns) == left_cols_before
    assert list(right.columns) == right_cols_before
