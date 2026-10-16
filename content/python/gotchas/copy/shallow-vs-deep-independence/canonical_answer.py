import copy

def safe_clone(grid):
    original_val = grid[0][0]
    clone = copy.deepcopy(grid)
    clone[0][0] = 99
    return [clone, grid[0][0] == original_val]
