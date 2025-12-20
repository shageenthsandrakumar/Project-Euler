import numpy as np
threshold = 1000
is_prime = np.ones(((threshold+1)//2,), dtype=bool) # index i = 2*i + 1
is_prime[0] = False 
for i in range(3, int(np.sqrt(threshold)) + 1, 2): 
    if is_prime[i//2]:
        is_prime[i*i//2::i] = False 
primes = np.r_[2, 2*np.nonzero(is_prime)[0]+1]

def is_full_reptend(p):
    n = p-1
    prime_factors = []
    index = 0
    f = primes[index]
    while f*f <= n:
        is_factor = False 
        while not n%f:
            n //= f
            is_factor = True
        if is_factor:
            prime_factors.append(f)
        index += 1
        f = primes[index]
    if n > 1:
        prime_factors.append(n)
    for q in prime_factors:
        exp = int((p - 1)/q) 
        if pow(10, exp, p) == 1:
            return False
    return True
d_max = 0
for prime in reversed(primes):
    if is_full_reptend(int(prime)):
        d_max = prime
        break
print(d_max)
