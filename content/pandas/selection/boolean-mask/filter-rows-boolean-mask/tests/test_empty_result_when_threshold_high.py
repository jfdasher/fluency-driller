def test_empty_result_when_threshold_high():
    import pandas as pd
    df = pd.DataFrame({'name': ['Alice', 'Bob'], 'score': [50, 60]})
    result = fn(df, 100)
    assert len(result) == 0
    assert list(result.columns) == ['name', 'score']
