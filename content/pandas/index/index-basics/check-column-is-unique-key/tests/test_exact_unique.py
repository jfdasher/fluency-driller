def test_exact_unique():
    import pandas as pd
    df = pd.DataFrame({'id': [1, 2, 3], 'name': ['Alice', 'Bob', 'Carol']})
    result = fn(df)
    assert result is True
