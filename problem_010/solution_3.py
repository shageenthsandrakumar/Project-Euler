import numpy as np
limit = 2000000
K_max = (limit - 1) // 2
is_prime_k = np.ones(K_max, dtype=bool)
i_max = int(np.floor((np.sqrt(1 + 8 * K_max-1) - 1) / 4))
I = np.arange(1, i_max + 1)
J = np.arange(1, K_max) 
composite_indices = []

for i in range(1, i_max + 1):
    j_start = i
    j_end = (K_max - i-1) // (1 + 2 * i)
    if j_end < j_start:
        break
    J_slice = np.arange(j_start, j_end + 1)
    k_values = i + J_slice + 2 * i * J_slice 
    composite_indices.append(k_values)

if composite_indices:
    all_k_to_mark = np.concatenate(composite_indices)
    is_prime_k[all_k_to_mark] = False
    
prime_k_indices = np.nonzero(is_prime_k)[0]
prime_k_indices = prime_k_indices[prime_k_indices > 0]
answer = 2 # Start with the prime 2
answer += 2 * np.sum(prime_k_indices) + len(prime_k_indices)
print(answer)
