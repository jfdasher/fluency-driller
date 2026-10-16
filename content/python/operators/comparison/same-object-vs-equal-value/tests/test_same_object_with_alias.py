def test_same_object_with_alias():
    x = [1, 2, 3]
    y = x
    assert same_object(x, y) == True
