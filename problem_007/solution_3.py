import itertools
nth = 10001
primes_found = 0
last_prime = 0
def prime_generator():
    yield 2  # Start with 2
    D = {}
    for c in itertools.count(3, 2):
        if c not in D:
            D[c * c] = 2 * c
            yield c
        else:
            step = D.pop(c)
            next_multiple = c + step
            while next_multiple in D:
                next_multiple += step
            D[next_multiple] = step
prime_gen = prime_generator()
for prime in prime_gen:
    primes_found += 1
    if primes_found == nth:
        break
print(prime)
