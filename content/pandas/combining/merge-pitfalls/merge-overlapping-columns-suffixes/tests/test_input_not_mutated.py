def test_input_not_mutated():
    import pandas as pd
    left = pd.DataFrame({'id': [1, 2], 'score': [80, 90]})
    right = pd.DataFrame({'id': [1, 2], 'score': [75, 85]})
    left_cols_before = list(left.columns)
    right_cols_before = list(right.columns)
    fn(left, right)
    assert list(left.columns) == left_cols_before
    assert list(right.columns) == right_cols_before
