def test_times_still_default():
    result = call_with_dot()
    assert result.count('ab') == 3
