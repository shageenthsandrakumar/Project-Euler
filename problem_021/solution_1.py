def d(n):
    if not n:
        return float('inf')
    orginal_n = n
    power_2 = 0
    while not n%2:
        n //= 2
        power_2 += 1
    answer = 2**(power_2+1)-1
    power_3 = 0
    while not n%3:
        n //= 3
        power_3 += 1
    answer *= (3**(power_3+1)-1)//2
    f = 5
    step = 2
    while f*f <= n:
        count = 0 
        while not n%f:
            n //= f
            count += 1
        if count:
            answer *= (f**(count+1)-1)//(f-1)
        f += step
        step = 6-step
    if n > 1:
        answer *= n+1
    return answer-orginal_n
threshold = 10000    
amicable_sum = 0
d_values = {}
for a in range(threshold):
    d_value = d(a)
    if d_values.get(d_value) == a and d_value != a:
        amicable_sum += d_value+a
    else:
        d_values[a] = d_value
for a in d_values:
    d_value = d_values[a]
    if threshold <= d_value < float('inf') and d_value != a:
        amicable_sum += a*int(d(d_value)==a)
print(amicable_sum)
