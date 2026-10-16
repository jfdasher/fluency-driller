def test_result_columns_correct():
    import pandas as pd
    left = pd.DataFrame({'id': [10, 20], 'score': [5, 6]})
    right = pd.DataFrame({'id': [10, 20], 'score': [7, 8]})
    result = fn(left, right)
    assert list(result.columns) == ['id', 'score_left', 'score_right']
    assert 'score' not in result.columns
