import numpy as np
nums = 20
is_composite = np.zeros(nums+1, dtype=bool)
primes = []
for i in range(2, nums + 1):
    if not is_composite[i]:
        primes.append(i)
    for p in primes:
        if i * p > nums:
            break
        is_composite[i * p] = True
        if not i%p:
            break
exponents = np.log(nums)//np.log(primes)
answer = int(np.prod(primes**exponents))
print(answer)
