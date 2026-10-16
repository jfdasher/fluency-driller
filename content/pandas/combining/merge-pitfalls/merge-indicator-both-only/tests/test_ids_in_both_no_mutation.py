def test_ids_in_both_no_mutation():
    import pandas as pd
    left = pd.DataFrame({'id': [1, 2, 3], 'val_l': ['a', 'b', 'c']})
    right = pd.DataFrame({'id': [1, 3, 5], 'val_r': ['x', 'y', 'z']})
    left_cols_before = list(left.columns)
    right_cols_before = list(right.columns)
    fn(left, right)
    assert list(left.columns) == left_cols_before
    assert list(right.columns) == right_cols_before
