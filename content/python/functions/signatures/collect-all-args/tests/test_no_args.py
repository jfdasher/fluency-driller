def test_no_args():
    result = collect_args()
    assert result == ((), {})
