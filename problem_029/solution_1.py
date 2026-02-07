lower_bound = 2
upper_bound = 100
powers = set()
for a in range(lower_bound,upper_bound+1):
    for b in range(lower_bound,upper_bound+1):
        powers.add(a**b)
print(len(powers))
