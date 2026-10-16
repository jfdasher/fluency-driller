def test_proportions_sum_to_one():
    import pandas as pd
    s = pd.Series(['a', 'b', 'a', 'c', 'b', 'a'])
    result = fn(s)
    assert abs(result.sum() - 1.0) < 1e-9
