limit = 2000000
is_prime = np.ones((limit//2,), dtype=bool) # index i = 2*i + 1
is_prime[0] = False 
for i in range(3, int(np.sqrt(limit)) + 1, 2): 
    if is_prime[i//2]:
        is_prime[i*i//2::i] = False 
primes = np.r_[2, 2*np.nonzero(is_prime)[0]+1]
answer = sum(primes)
print(answer)
