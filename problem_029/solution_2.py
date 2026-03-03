from math import log2

def get_primitive_root(a):
    for p in range(int(log2(a)), 1, -1):
        r = round(a ** (1/p))
        if r ** p == a:
            return r, p
    return a, 1

terms = set()
for a in range(2, 101):
    r, p = get_primitive_root(a)
    for b in range(2, 101):
        terms.add((r, p * b))

print(len(terms))
