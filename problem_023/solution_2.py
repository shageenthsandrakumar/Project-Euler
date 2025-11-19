import numpy as np
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
threshold = 28124
abundant_numbers = []
is_non_abundant = np.ones((threshold,), dtype=bool)
for a in range(1,threshold):
    if d(a) > a:
        abundant_numbers.append(a)
abundant_numbers = np.array(abundant_numbers)
i_values, j_values = np.triu_indices(len(abundant_numbers))
all_sums = abundant_numbers[i_values] + abundant_numbers[j_values]
is_non_abundant[all_sums[all_sums < threshold]] = False
answer = sum(np.nonzero(is_non_abundant)[0])
print(answer)
