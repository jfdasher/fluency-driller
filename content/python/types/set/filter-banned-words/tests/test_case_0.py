def test_case_0():
    assert equal(remove_banned(**{'banned': ['spam', 'hate'], 'words': ['hello', 'spam', 'world', 'hate', 'friend']}), ['hello', 'world', 'friend'])
