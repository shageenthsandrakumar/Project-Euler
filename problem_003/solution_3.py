n = 600851475143
max_factor = 0
while not n%2:
    max_factor = 2 
    n //= 2
while not n%3:
    max_factor = 3
    n //= 3
f = 5
toggle = False
while f*f <= n:
    while not n%f:
        max_factor = f
        n //= f
    f += 2+2*int(toggle)
    toggle = not toggle
if n > 1:
    max_factor = n
print(max_factor)
