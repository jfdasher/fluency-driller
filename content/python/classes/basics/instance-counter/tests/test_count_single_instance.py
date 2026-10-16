def test_count_single_instance():
    Widget.count = 0
    Widget()
    assert Widget.count == 1
