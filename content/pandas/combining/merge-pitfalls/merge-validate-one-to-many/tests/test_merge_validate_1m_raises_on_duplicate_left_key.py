def test_merge_validate_1m_raises_on_duplicate_left_key():
    import pandas as pd
    left = pd.DataFrame({'dept_id': [1, 1], 'dept_name': ['Engineering', 'Engineering2']})
    right = pd.DataFrame({'dept_id': [1, 2], 'employee': ['Alice', 'Bob']})
    try:
        fn(left, right)
        assert False, 'Expected MergeError was not raised'
    except pd.errors.MergeError:
        pass
