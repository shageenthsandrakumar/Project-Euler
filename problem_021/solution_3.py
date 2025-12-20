from functools import lru_cache
import numpy as np

amicable_sum = 0
threshold = 10000
is_prime = np.ones(((threshold+1)//2,), dtype=bool) # index i = 2*i + 1
is_prime[0] = False 
for i in range(3, int(np.sqrt(threshold)) + 1, 2): 
    if is_prime[i//2]:
        is_prime[i*i//2::i] = False 
primes = np.r_[2, 2*np.nonzero(is_prime)[0]+1]

@lru_cache(maxsize=threshold)
def d(n):
    if not n:
        return float('inf')
    orginal_n = n
    index = 0
    f = primes[index]
    answer = 1
    while f*f <= n:
        count = 0 
        while not n%f:
            n //= f
            count += 1
        if count:
            answer *= (f**(count+1)-1)//(f-1)
        index += 1
        f = primes[index]
    if n > 1:
        answer *= n+1
    return answer-orginal_n

PN = [6,28,496,8128]
exclusion = set(PN)
exclusion.add(2)
for a in range(threshold):
    if (a%2 and is_prime[a//2]) or a in exclusion:
        continue
    d_value = d(a)
    if d_value < a:
        amicable_sum += (d_value+a)*int(d(d_value) == a)
    elif threshold <= d_value < float('inf'):
        amicable_sum += a*int(d(d_value) == a)
print(amicable_sum)
