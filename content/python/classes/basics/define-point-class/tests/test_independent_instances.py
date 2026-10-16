def test_independent_instances():
    p1 = Point(0, 0)
    p2 = Point(10, 20)
    assert p1.x != p2.x
    assert p1.y != p2.y
