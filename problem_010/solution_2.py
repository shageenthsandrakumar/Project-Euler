import numpy as np
limit = 2000000
K_max_plus = (limit - 2) // 6 + 1
sieve_plus1 = np.ones(K_max_plus, dtype=bool) 
sieve_plus1[0] = False 
K_max_minus = (limit - 6) // 6 + 1 # Use 6k+5 < LIMIT (since 6k+5 >= 5)
sieve_minus1 = np.ones(K_max_minus, dtype=bool) 
sqrt_limit = int(np.sqrt(limit))
p = 5
while p <= sqrt_limit:
    is_prime = False
    p_mod_6 = p % 6
    if p_mod_6 == 1:
        k = (p - 1) // 6
        if k < K_max_plus and sieve_plus1[k]:
            is_prime = True
    elif p_mod_6 == 5:
        k = (p - 5) // 6
        if k < K_max_minus and sieve_minus1[k]:
            is_prime = True
    if is_prime:
        start_k_1 = (p * p - 1) // 6
        if start_k_1 < K_max_plus:
            sieve_plus1[start_k_1::p] = False
        start_num_2 = p * (p + 2) 
        if p_mod_6 == 5:
            start_num_2 = p * (p + 2)
        else:
            start_num_2 = p * (p + 4)            
        start_k_2 = (start_num_2 - 5) // 6
        if start_k_2 < K_max_minus:
            sieve_minus1[start_k_2::p] = False
    if p_mod_6 == 1:
        p += 4
    else: # p_mod_6 == 5
        p += 2

answer = 2 + 3 
prime_indices_plus1 = np.nonzero(sieve_plus1)[0]
primes_plus1 = 6 * prime_indices_plus1 + 1
answer += np.sum(primes_plus1)
prime_indices_minus1 = np.nonzero(sieve_minus1)[0]
primes_minus1 = 6 * prime_indices_minus1 + 5 
answer += np.sum(primes_minus1)
print(answer) 
