def clamp_negatives(nums):
    return [x if x >= 0 else 0 for x in nums]
