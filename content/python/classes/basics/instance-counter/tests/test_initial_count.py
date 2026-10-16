def test_initial_count():
    Widget.count = 0
    assert Widget.get_count() == 0
