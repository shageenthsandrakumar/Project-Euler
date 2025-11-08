grid_size = 20
grid = [[0]*(grid_size+1) for _ in range(grid_size+1)]

for i in range(grid_size+1):
    grid[grid_size][i] = 1
    grid[i][grid_size] = 1

for i in range(grid_size-1, -1, -1):
    for j in range(grid_size-1, -1, -1):
        grid[i][j] = grid[i+1][j] + grid[i][j+1]

print(grid[0][0])
