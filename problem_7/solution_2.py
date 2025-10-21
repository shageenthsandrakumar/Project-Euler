import numpy as np
threshold = 10001
n = threshold
limit = int(n*(np.log(n)+np.log(np.log(n)))+1)
is_prime = np.ones(((limit+1)//2,), dtype=bool) # index i = 2*i + 1
is_prime[0] = False 
for i in range(3, int(np.sqrt(limit)) + 1, 2): 
    if is_prime[i//2]:
        is_prime[i*i//2::i] = False 
primes = np.r_[2, 2*np.nonzero(is_prime)[0]+1]
print(int(primes[n-1]))
