def test_case_4():
    assert equal(remove_banned(**{'banned': ['no'], 'words': ['yes', 'no', 'maybe', 'no', 'yes']}), ['yes', 'maybe', 'yes'])
