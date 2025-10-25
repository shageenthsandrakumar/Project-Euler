import numpy as np
limit = 2000000
limit -= 1
sieve_plus1 = np.ones((limit - 1) // 6 + 1, dtype=bool) 
sieve_plus1[0] = False 
sieve_minus1 = np.ones((limit - 5) // 6 + 1, dtype=bool)  
p = 5
step = 2

while p <= int(np.sqrt(limit)):
    k = p // 6
    if (step == 4 and sieve_plus1[k]) or (step == 2 and sieve_minus1[k]):
        start_1 = p**2//6
        sieve_plus1[start_1::p] = False          
        start_2 = p*(p + step)// 6
        sieve_minus1[start_2::p] = False
    p += step
    step = 6 - step

primes_plus1 = 6*np.nonzero(sieve_plus1)[0]+1
primes_minus1 = 6*np.nonzero(sieve_minus1)[0]+ 5 
answer = 2+3+np.sum(primes_plus1)+np.sum(primes_minus1)
print(answer)
