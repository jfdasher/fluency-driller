def test_inner_join_exact():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    left = pd.DataFrame({'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Carol']})
    right = pd.DataFrame({'id': [2, 3, 4], 'score': [88, 95, 70]})
    expected = pd.DataFrame({'id': [2, 3], 'name': ['Bob', 'Carol'], 'score': [88, 95]})
    result = fn(left, right)
    assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))
