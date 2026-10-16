def set_cell(m, n, row, col, val):
    grid = [[0] * n for _ in range(m)]
    grid[row][col] = val
    return grid
