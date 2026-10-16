def test_negative_coords():
    import math
    p = make_point(-3, -4)
    assert distance_from_origin(p) == 5.0
