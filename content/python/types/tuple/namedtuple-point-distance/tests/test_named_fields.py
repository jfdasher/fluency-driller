def test_named_fields():
    p = make_point(1, 2)
    assert p.x == 1 and p.y == 2
