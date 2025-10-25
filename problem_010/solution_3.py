import numpy as np
limit = 2000000
K_max =  (limit-2)//2
is_prime_k = np.ones(K_max+1, dtype=bool)
is_prime_k[0] = False
i_max = int((-1 + np.sqrt(1 + 2 * K_max))/ 2)
for i in range(1, i_max + 1):
    j_start = i
    j_end = (K_max - i) // (1 + 2 * i)
    if j_end < j_start:
        break
    J_slice = np.arange(j_start, j_end + 1)
    k_values = i + J_slice + 2 * i * J_slice 
    is_prime_k[k_values] = False
primes = np.r_[2,2*np.nonzero(is_prime_k)[0]+1]
answer = np.sum(primes)
print(answer)
