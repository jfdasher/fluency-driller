def test_count_increments():
    Widget.count = 0
    Widget()
    Widget()
    Widget()
    assert Widget.get_count() == 3
