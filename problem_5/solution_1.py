import numpy as np
nums = 20
primes = [2] 
for n in range(3, nums + 1):
    if not any(n % p == 0 for p in primes):
        primes.append(n)
primes = np.array(primes) 
exponents = np.log(nums)//np.log(primes)
answer = int(np.prod(primes**exponents))
print(answer)
