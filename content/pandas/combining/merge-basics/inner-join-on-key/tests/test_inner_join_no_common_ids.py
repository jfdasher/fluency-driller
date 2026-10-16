def test_inner_join_no_common_ids():
    import pandas as pd
    left = pd.DataFrame({'id': [1, 2], 'name': ['Alice', 'Bob']})
    right = pd.DataFrame({'id': [3, 4], 'score': [70, 80]})
    result = fn(left, right)
    assert len(result) == 0
    assert 'id' in result.columns
    assert 'name' in result.columns
    assert 'score' in result.columns
