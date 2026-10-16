def test_returns_new_list():
    a = [1, 2]
    b = [3, 4]
    result = merge_lists(a, b)
    result.append(99)
    assert a == [1, 2] and b == [3, 4]
