def replicate_row_mutate_one(row, m, col, val):
    grid = [list(row) for _ in range(m)]
    grid[0][col] = val
    return grid
