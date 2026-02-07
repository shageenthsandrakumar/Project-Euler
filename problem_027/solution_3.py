import numpy as np

bound_b = 1000
bound_a = 1000
threshold = bound_b*(bound_a+bound_b)

is_prime = np.ones(((threshold+1)//2,), dtype=bool)
is_prime[0] = False 
for i in range(3, int(np.sqrt(threshold)) + 1, 2): 
    if is_prime[i//2]:
        is_prime[i*i//2::i] = False 

b_primes = 2*np.nonzero(is_prime[:(bound_b+1)//2+1])[0]+1

a_values = np.arange(-2*(bound_a//2)+1, 1000, 2)
A, B = np.meshgrid(a_values, b_primes, indexing='ij')
n_max_grid = np.zeros_like(A)
active = np.ones_like(A, dtype=bool) 

for n in range(max(b_primes)):
    values = n**2 + A*n + B
    is_prime_grid = np.ones_like(values, dtype=bool)
    is_prime_grid[values < 2] = False
    is_prime_grid[(values > 2) & (values % 2 == 0)] = False
    odd_mask = (values % 2 == 1) & (values > 2)
    is_prime_grid[odd_mask] = is_prime[values[odd_mask] // 2]
    still_prime = active & is_prime_grid
    n_max_grid[still_prime] = n
    active &= is_prime_grid 
    if not active.any():
        break

max_idx = np.unravel_index(np.argmax(n_max_grid), n_max_grid.shape)
a_final = a_values[max_idx[0]]
b_final = b_primes[max_idx[1]]

print(a_final * b_final)
