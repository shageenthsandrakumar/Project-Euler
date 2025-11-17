import numpy as np
from mplusa import maxplus as mp

text = """75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23"""

triangle = [[int(x) for x in line.split()] for line in text.strip().split('\n')]
levels = len(triangle)
current = np.array(triangle[-1], dtype=float).reshape(-1, 1)

for i in range(levels - 2, -1, -1):
    row_size = i + 1
    next_row_size = i + 2
    selector = np.full((row_size, next_row_size), -np.inf)
    for j in range(row_size):
        selector[j, j] = 0    
        selector[j, j + 1] = 0
    current = mp.mult_matrices(selector,current) + np.array(triangle[i]).reshape(-1, 1)
    
print(int(current[0, 0]))
