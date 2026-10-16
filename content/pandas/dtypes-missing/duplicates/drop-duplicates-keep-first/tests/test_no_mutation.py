def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Alice', 'Carol', 'Bob', 'Carol'],
        'score': [90, 85, 90, 78, 85, 78]
    })
    original_len = len(df)
    fn(df)
    assert len(df) == original_len, 'Input DataFrame was mutated'
