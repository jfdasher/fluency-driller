def test_shape_and_index():
    import pandas as pd
    df = pd.DataFrame(
        {'x': [1, 4, 7, 10], 'y': [2, 5, 8, 11], 'z': [3, 6, 9, 12]},
        index=['a', 'b', 'c', 'd']
    )
    result = fn(df)
    assert result.shape == (2, 2)
    assert list(result.index) == ['b', 'd']
    assert list(result.columns) == ['x', 'z']
