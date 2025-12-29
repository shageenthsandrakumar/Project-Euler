import math
threshold = 500
def number_of_divisors(n):
    count = 0
    while not n%2:
        n //= 2
        count += 1
    answer = count+1
    count = 0
    while not n%3:
        n //= 3
        count += 1
    answer *= count+1
    f = 5
    step = 2
    while f*f <= n:
        count = 0 
        while not n%f:
            n //= f
            count += 1
        f += step
        step = 6-step
        answer *= count+1
    if n > 1:
        answer *=2
    return answer

triangle_number = 0
n = 0
divisor_count = 0
while divisor_count <= threshold:
    n += 1
    triangle_number += n
    divisor_count = number_of_divisors(triangle_number)
print(triangle_number)
