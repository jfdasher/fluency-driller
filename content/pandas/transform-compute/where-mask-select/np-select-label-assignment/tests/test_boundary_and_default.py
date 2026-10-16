def test_boundary_and_default():
    import pandas as pd
    df = pd.DataFrame({'score': [90, 75, 60, 59]})
    result = fn(df)
    assert list(result['grade']) == ['A', 'B', 'C', 'F'], f"got {list(result['grade'])}"
