from functools import lru_cache
grid_size = 20
@lru_cache((grid_size+1)**2)
def paths(i, j):
    if i == grid_size or j == grid_size:
        return 1
    return paths(i+1, j) + paths(i, j+1)
print(paths(0,0))
