def test_exact_filter_error_rows():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'message': [
            'System started normally',
            'ERROR: disk full',
            'warning: low memory',
            'error code 404 returned',
            'All systems operational'
        ]
    })
    expected = pd.DataFrame(
        {'message': ['ERROR: disk full', 'error code 404 returned']},
        index=[1, 3]
    )
    assert_frame_equal(fn(df), expected)
