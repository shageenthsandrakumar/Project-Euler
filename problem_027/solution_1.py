import numpy as np
bound_b = 1000
bound_a = 1000
threshold = bound_b*(bound_a+bound_b)
is_prime = np.ones(((threshold+1)//2,), dtype=bool) # index i = 2*i + 1
is_prime[0] = False 
for i in range(3, int(np.sqrt(threshold)) + 1, 2): 
    if is_prime[i//2]:
        is_prime[i*i//2::i] = False 
b_primes = 2*np.nonzero(is_prime[:(bound_b+1)//2+1])[0]+1
n_max = 0
a_final = 0
b_final = 0
for a in range(-999,1000,2):
    for b in b_primes:
        for n in range(b):
            value = n*n+a*n+b
            stop = False
            if value < 2:
                stop = True
            elif (not is_prime[value//2] and value%2) or (value%2-1 and value != 2):
                stop = True
            if stop:
                if n > n_max:
                    n_max = n
                    a_final = a
                    b_final = b
                break

print(a_final*b_final)  
