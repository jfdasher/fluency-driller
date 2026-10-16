def test_shape_and_columns():
    result = fn()
    assert result.shape == (5, 2), f'Expected shape (5, 2), got {result.shape}'
    assert list(result.columns) == ['score', 'count'], f'Unexpected columns: {list(result.columns)}'
