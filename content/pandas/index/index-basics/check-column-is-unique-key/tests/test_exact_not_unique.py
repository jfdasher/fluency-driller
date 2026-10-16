def test_exact_not_unique():
    import pandas as pd
    df = pd.DataFrame({'id': [1, 2, 2], 'name': ['Alice', 'Bob', 'Bob2']})
    result = fn(df)
    assert result is False
