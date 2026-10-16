def test_all_same_value():
    import pandas as pd
    df = pd.DataFrame({'city': ['Tokyo', 'Tokyo', 'Tokyo']})
    assert fn(df) == 1
