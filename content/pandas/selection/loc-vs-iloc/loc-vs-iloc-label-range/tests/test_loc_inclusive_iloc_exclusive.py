def test_loc_inclusive_iloc_exclusive():
    import pandas as pd
    df = pd.DataFrame({'value': [10, 20, 30, 40, 50]}, index=list('abcde'))
    loc_res, iloc_res = fn(df)
    assert list(loc_res.index) == ['b', 'c', 'd'], f'loc should include b,c,d but got {list(loc_res.index)}'
    assert list(iloc_res.index) == ['a', 'b'], f'iloc[0:2] should return rows at positions 0,1 but got {list(iloc_res.index)}'
