def test_count_shared_across_instances():
    Widget.count = 0
    a = Widget()
    b = Widget()
    assert a.get_count() == b.get_count() == 2
