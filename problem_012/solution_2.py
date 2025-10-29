threshold = 500
def number_of_divisors(n):
    exponents_plus1 = []
    power_2 = 0
    while not n%2:
        n //= 2
        power_2 += 1
    exponents_plus1.append(power_2+1)
    power_3 = 0
    while not n%3:
        n //= 3
        power_3 += 1
    exponents_plus1.append(power_3+1)
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
    return math.prod(exponents_plus1),power_2
n = 0
divisor_count = 0
while divisor_count <= threshold:
    n += 1
    tau_n,power2_n = number_of_divisors(n)
    tau_n1,power2_n1 = number_of_divisors(n+1)
    power_even = power2_n+power2_n1
    divisor_count = tau_n*tau_n1*power_even/(power_even + 1)
answer = n*(n+1)//2
print(answer)
