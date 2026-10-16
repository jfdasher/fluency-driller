def test_length_preserved():
    nums = [-1, -2, 3, -4, 5]
    result = clamp_negatives(nums)
    assert len(result) == len(nums)
