def test_case_1():
    assert equal(remove_banned(**{'banned': [], 'words': ['keep', 'all']}), ['keep', 'all'])
