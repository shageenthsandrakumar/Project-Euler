import numpy as np
limit = 2000000
is_composite = np.zeros(limit+1, dtype=bool)
primes = []
answer = 0
for i in range(2, limit + 1):
    if not is_composite[i]:
        primes.append(i)
        answer += i
    for p in primes:
        if i * p > limit:
            break
        is_composite[i * p] = True
        if not i%p:
            break
print(answer)
