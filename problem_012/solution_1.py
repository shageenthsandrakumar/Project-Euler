import math
threshold = 500
def number_of_divisors(n):
    exponents_plus1 = []
    count = 0
    while not n%2:
        n //= 2
        count += 1
    exponents_plus1.append(count+1)
    count = 0
    while not n%3:
        n //= 3
        count += 1
    exponents_plus1.append(count+1)
    f = 5
    step = 2
    while f*f <= n:
        count = 0 
        while not n%f:
            n //= f
            count += 1
        f += step
        step = 6-step
        exponents_plus1.append(count+1)
    if n > 1:
        exponents_plus1.append(2)
    return math.prod(exponents_plus1)

triangle_number = 0
n = 0
divisor_count = 0
while divisor_count <= threshold:
    n += 1
    triangle_number += n
    divisor_count = number_of_divisors(triangle_number)
print(triangle_number)
