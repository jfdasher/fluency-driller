def test_empty_match():
    import pandas as pd
    df = pd.DataFrame({'category': ['A', 'C', 'E'], 'value': [1, 2, 3]})
    result = fn(df)
    assert len(result) == 0
    assert list(result.columns) == ['category', 'value']
