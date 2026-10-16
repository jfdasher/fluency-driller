def test_add_aligned_no_mutation():
    import pandas as pd
    a = pd.Series([10, 20, 30], index=[1, 2, 3])
    b = pd.Series([200, 300, 400], index=[2, 3, 4])
    a_vals_before = a.tolist()
    b_vals_before = b.tolist()
    _ = fn(a, b)
    assert a.tolist() == a_vals_before
    assert b.tolist() == b_vals_before
