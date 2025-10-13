n = 600851475143
f = 2
max_factor = 0
while f <= n:
    if not n%f:
        n //= f
        max_factor = f
    else:
        f += 1
print(max_factor)
