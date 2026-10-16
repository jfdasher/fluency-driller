def test_no_mutation_of_inputs():
    import pandas as pd
    left = pd.DataFrame({'val_a': [1, 2, 3]}, index=['a', 'b', 'c'])
    right = pd.DataFrame({'val_b': [20, 30, 40]}, index=['b', 'c', 'd'])
    left_cols_before = list(left.columns)
    right_cols_before = list(right.columns)
    fn(left, right)
    assert list(left.columns) == left_cols_before
    assert list(right.columns) == right_cols_before
