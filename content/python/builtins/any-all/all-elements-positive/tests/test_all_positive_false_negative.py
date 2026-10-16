def test_all_positive_false_negative():
    assert all_positive([1, -1, 3]) == False
