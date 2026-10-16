def test_exact_values_and_dtypes():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'price': [10.0, 20.0, 50.0], 'tax_rate': [0.05, 0.10, 0.20]})
    expected = pd.DataFrame({
        'price': [10.0, 20.0, 50.0],
        'tax_rate': [0.05, 0.10, 0.20],
        'price_with_tax': [10.50, 22.00, 60.00]
    })
    assert_frame_equal(fn(df), expected)
