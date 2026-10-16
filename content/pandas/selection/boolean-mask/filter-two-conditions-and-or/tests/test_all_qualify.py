def test_all_qualify():
    import pandas as pd
    df = pd.DataFrame({
        'score': [96, 97, 98],
        'grade': ['B', 'C', 'A']
    })
    result = fn(df)
    assert len(result) == 3
