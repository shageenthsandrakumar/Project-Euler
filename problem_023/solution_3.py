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
PN = [6,28,496,8128]
is_abundant = np.zeros((threshold,), dtype=bool)
for a in PN:
    is_abundant[2*a::a] = True
for a in range(1,threshold):
    if not is_abundant[a]:
        if d(a) > a:
            is_abundant[a::a] = True
abundant_numbers = np.nonzero(is_abundant)[0]
i_values, j_values = np.triu_indices(len(abundant_numbers))
all_sums = abundant_numbers[i_values] + abundant_numbers[j_values]
not_abundant_sums = np.ones((threshold,), dtype=bool)
not_abundant_sums[all_sums[all_sums < threshold]] = False
answer = sum(np.nonzero(not_abundant_sums)[0])
print(answer)
