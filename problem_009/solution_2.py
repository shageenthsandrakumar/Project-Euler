import math
P = 1000
if P%2:
    print(f"Perimeter {P} is not an even integer, no integer Pythagorean Triples can exist.")
else:
    target_value = P // 2
    unique_triplets = set()
    for k in range(1, target_value + 1):
        if target_value % k == 0:
            E = target_value//k
            limit_m = int(math.sqrt(E))
            for m in range(1, limit_m + 1):
                if E%m == 0:
                    n = E//m-m
                    if m>n and n>0:
                        a = k*(m**2-n**2)
                        b = k*(2*m*n)
                        c = k*(m**2+n**2)
                        if a + b + c == P and a**2 + b**2 == c**2:
                            unique_triplets.add(tuple(sorted((a, b, c))))
triples = list(unique_triplets)
if triples:
    print(f"Found {len(triples)} Pythagorean Triplet(s) where a + b + c = {P}:")
    triples.sort()
    for triplet in triples:
        a, b, c = triplet
        print(f"a, b, c = {a}, {b}, {c}")
        answer = a*b*c
        print(f"Therefore product abc is {answer}") 
else:
    print(f"No Pythagorean Triples found for perimeter P = {P}.")

