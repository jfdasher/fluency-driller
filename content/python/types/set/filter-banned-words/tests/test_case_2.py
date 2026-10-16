def test_case_2():
    assert equal(remove_banned(**{'banned': ['a', 'b', 'c'], 'words': ['a', 'b', 'c']}), [])
