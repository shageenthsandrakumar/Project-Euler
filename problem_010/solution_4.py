import itertools
threshold = 2000000
prime_sum = 0
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
for p in prime_gen:
    if p < threshold:
        prime_sum += p
    else:
        break
print(prime_sum)
