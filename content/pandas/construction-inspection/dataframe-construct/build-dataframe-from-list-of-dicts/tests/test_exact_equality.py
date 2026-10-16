def test_exact_equality():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    records = [
        {"name": "Alice", "age": 30, "score": 88.5},
        {"name": "Bob",   "age": 25, "score": 92.0},
        {"name": "Carol", "age": 35, "score": 76.3},
    ]
    expected = pd.DataFrame({
        "name":  ["Alice", "Bob", "Carol"],
        "age":   pd.array([30, 25, 35], dtype="int64"),
        "score": [88.5, 92.0, 76.3],
    })
    result = fn(records)
    assert_frame_equal(result, expected, check_like=False)
