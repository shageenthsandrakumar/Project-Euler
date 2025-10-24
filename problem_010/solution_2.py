import numpy as np
limit = 2000000
limit -= 1
sieve_plus1 = np.ones((limit - 1) // 6 + 1, dtype=bool) 
sieve_plus1[0] = False 
sieve_minus1 = np.ones((limit - 5) // 6 + 1, dtype=bool)  
p = 5
while p <= int(np.sqrt(limit)):
    is_prime = False
    p_mod_6 = p % 6
    k = (p - p_mod_6) // 6
    if p_mod_6 == 1 and sieve_plus1[k]:
            is_prime = True
    elif p_mod_6 == 5 and sieve_minus1[k]:
            is_prime = True
    if is_prime:
        start_1 = (p * p - 1) // 6
        sieve_plus1[start_1::p] = False          
        start_2 = (p * (p + 4 - p_mod_6//2) - 5) // 6
        sieve_minus1[start_2::p] = False
    p += 4 - p_mod_6//2
answer = 5
primes_plus1 = 6*np.nonzero(sieve_plus1)[0]+1
answer += np.sum(primes_plus1)
primes_minus1 = 6*np.nonzero(sieve_minus1)[0]+ 5 
answer += np.sum(primes_minus1)
print(answer)
