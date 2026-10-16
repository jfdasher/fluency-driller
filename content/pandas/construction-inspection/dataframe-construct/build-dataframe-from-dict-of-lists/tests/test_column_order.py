def test_column_order():
    import pandas as pd
    names  = ['X']
    ages   = [1]
    scores = [0.0]
    result = fn(names, ages, scores)
    assert list(result.columns) == ['name', 'age', 'score']
