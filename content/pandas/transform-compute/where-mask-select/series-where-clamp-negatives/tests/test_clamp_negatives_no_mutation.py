def test_clamp_negatives_no_mutation():
    import pandas as pd
    s = pd.Series([3, -1, 7, -4, 0], dtype='int64')
    original_values = s.tolist()
    fn(s)
    assert s.tolist() == original_values
