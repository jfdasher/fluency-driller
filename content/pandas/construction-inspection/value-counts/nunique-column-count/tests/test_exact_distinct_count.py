def test_exact_distinct_count():
    import pandas as pd
    df = pd.DataFrame({'city': ['Paris', 'London', 'Paris', 'Berlin', 'London', 'Paris']})
    result = fn(df)
    assert result == 3
    assert type(result) is int
