nth = 10001
threshold = nth
primes = []
n = 1
while len(primes) < threshold:
    n += 1
    if not any(n % p == 0 for p in primes):
        primes.append(n)
nth_prime = n
print(nth_prime)
