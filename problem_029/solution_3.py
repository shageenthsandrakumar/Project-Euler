from math import log2
lower_bound = 2
upper_bound = 100
def get_primitive_root(a):
    for p in range(int(log2(a)), 1, -1):
        r = round(a ** (1/p))
        if r ** p == a:
            return r, p
    return a, 1

root_exponents = {}

for a in range(lower_bound, upper_bound+1):
    r, p = get_primitive_root(a)
    new_exponents = {p * b for b in range(lower_bound, upper_bound+1)}
    if r not in root_exponents:
        root_exponents[r] = new_exponents
    else:
        root_exponents[r].update(new_exponents)  # only adds genuinely new ones

print(sum(len(exps) for exps in root_exponents.values()))
