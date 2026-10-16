def test_case_3():
    assert equal(remove_banned(**{'banned': ['bad'], 'words': []}), [])
