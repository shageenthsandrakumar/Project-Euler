power = 5
digits = 1
upper_bound = digits*(9**power)

while(upper_bound > 10**(digits-1)):
    upper_bound = digits*(9**power)
    digits += 1

result = sum(n for n in range(2, upper_bound+ 1) if sum(int(d)**power for d in str(n)) == n)
print(result)
