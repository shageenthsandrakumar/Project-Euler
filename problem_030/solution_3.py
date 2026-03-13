from itertools import combinations_with_replacement
result = 0
power = 5
digits = 1
max_sum = digits*(9**power)
p = [d**power for d in range(10)]

while(upper_bound > 10**(digits-1)):
    digits += 1
    max_sum = digits*(9**power)

for length in range(2, digits):
    for combo in combinations_with_replacement(range(10), length):
        s = sum(p[d] for d in combo)
        if s-1 and sorted(int(d) for d in str(s)) == list(combo):
            result+=s
print(result)
