power = 5
digits = 1
max_sum = digits*(9**power)

while(upper_bound > 10**(digits-1)):
    digits += 1
    max_sum = digits*(9**power)
upper_bound = (digits-1)*(9**power)
p = {str(d): d**power for d in range(10)}

result = sum(n for n in range(2, upper_bound+ 1) if sum(p[d] for d in str(n)) == n)
print(result)
