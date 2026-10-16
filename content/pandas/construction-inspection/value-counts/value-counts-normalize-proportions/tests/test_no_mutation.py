def test_no_mutation():
    import pandas as pd
    s = pd.Series(['x', 'y', 'x'])
    original_values = s.tolist()
    fn(s)
    assert s.tolist() == original_values
