from math import log2, gcd
from itertools import combinations

lower_bound = 2
upper_bound = 100

def lcm_list(numbers):
    result = 1
    for number in numbers:
        result *= number//gcd(number, result)
    return result

def count_distinct_exponents(powers,lower_bound,upper_bound):
    total = 0
    for size in range(len(powers)):
        for subset in combinations(powers, size+1):
            m = lcm_list(list(subset))
            lower = lower_bound * max(subset)
            upper = upper_bound * min(subset)
            total += (-1)**(size)*(upper // m - (lower - 1) // m)
    return total
    
def get_primitive_root(a):
    for p in range(int(log2(a)), 1, -1):
        r = round(a ** (1/p))
        if r ** p == a:
            return r, p
    return a, 1

root_powers = []
for a in range(lower_bound, upper_bound + 1):
    r, p = get_primitive_root(a)
    for i, (root, plist) in enumerate(root_powers):
        if root == r:
            root_powers[i] = (root, plist + [p])
            break
    else:
        root_powers.append((r, [p]))

total = sum(count_distinct_exponents(plist,lower_bound,upper_bound) for _, plist in root_powers)
print(total) 
