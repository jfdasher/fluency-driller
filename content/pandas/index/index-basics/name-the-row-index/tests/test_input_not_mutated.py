def test_input_not_mutated():
    import pandas as pd
    df = pd.DataFrame({'score': [88, 95, 72], 'grade': ['B', 'A', 'C']})
    _ = fn(df)
    assert df.index.name is None, 'original df.index.name should remain None'
