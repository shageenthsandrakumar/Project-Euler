from functools import lru_cache
amicable_sum = 0
threshold = 10000
@lru_cache(maxsize=threshold+1)
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
for a in range(threshold):
    d_value = d(a)
    if d_value < a:
        amicable_sum += (d_value+a)*int(d(d_value) == a)
print(amicable_sum)
