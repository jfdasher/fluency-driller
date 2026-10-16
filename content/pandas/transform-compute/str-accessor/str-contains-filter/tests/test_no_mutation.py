def test_no_mutation():
    import pandas as pd
    df = pd.DataFrame({
        'message': [
            'System started normally',
            'ERROR: disk full',
            'warning: low memory',
            'error code 404 returned',
            'All systems operational'
        ]
    })
    original_len = len(df)
    fn(df)
    assert len(df) == original_len, 'Input DataFrame was mutated'
