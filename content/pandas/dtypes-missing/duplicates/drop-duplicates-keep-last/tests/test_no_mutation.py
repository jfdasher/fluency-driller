def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'city': ['NYC', 'LAX', 'NYC', 'LAX', 'CHI'],
        'temp': [70, 85, 72, 88, 60]
    })
    original_len = len(df)
    fn(df)
    assert len(df) == original_len, 'Input DataFrame was mutated'
