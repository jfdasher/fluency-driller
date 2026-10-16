def test_same_object_with_copy():
    x = [1, 2, 3]
    y = [1, 2, 3]
    assert same_object(x, y) == False
