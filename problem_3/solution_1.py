n = 600851475143
f = 2
factors = []
while f <= n:
    if not n%f:
        n //= f
        factors.append(f)
    else:
        f += 1
print(max(factors))
