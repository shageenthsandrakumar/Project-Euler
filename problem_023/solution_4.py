import numpy as np
threshold = 28124
is_prime = np.ones(((threshold+1)//2,), dtype=bool) # index i = 2*i + 1
is_prime[0] = False 
for i in range(3, int(np.sqrt(threshold)) + 1, 2): 
    if is_prime[i//2]:
        is_prime[i*i//2::i] = False 
primes = np.r_[2, 2*np.nonzero(is_prime)[0]+1]
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
is_abundant = np.zeros((threshold,), dtype=bool)
for a in PN:
    is_abundant[2*a::a] = True
is_prime_power = np.zeros((threshold,), dtype=bool)
for prime in primes:
    is_prime_power[prime ** np.arange(1, int(np.log(threshold-1)/np.log(prime)) + 1)] = True
for a in range(1,threshold):
    if is_abundant[a] or is_prime_power[a]:
        continue
    elif d(a) > a:
        is_abundant[a::a] = True
abundant_numbers = np.nonzero(is_abundant)[0]
i_values, j_values = np.triu_indices(len(abundant_numbers))
all_sums = abundant_numbers[i_values] + abundant_numbers[j_values]
not_abundant_sums = np.ones((threshold,), dtype=bool)
not_abundant_sums[all_sums[all_sums < threshold]] = False
answer = sum(np.nonzero(not_abundant_sums)[0])
print(answer)
