nth = 10001
threshold = nth
composites = set()
primes = []
i = 2
while len(primes) < threshold:
    if i not in composites:
        primes.append(i)
    for p in primes:
        composites.add(i * p)
        if i % p == 0:
            break
    i += 1
nth_prime = primes[-1]
print(nth_prime)
