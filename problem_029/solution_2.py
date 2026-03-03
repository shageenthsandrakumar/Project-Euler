from math import log2
lower_bound = 2
upper_bound = 100

def get_primitive_root(a):
    for p in range(int(log2(a)), 1, -1):
        r = round(a ** (1/p))
        if r ** p == a:
            return r, p
    return a, 1

terms = set()
for a in range(lower_bound, upper_bound+1):
    r, p = get_primitive_root(a)
    for b in range(lower_bound, upper_bound+1):
        terms.add((r, p * b))

print(len(terms))
