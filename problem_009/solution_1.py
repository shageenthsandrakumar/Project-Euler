import math
P = 1000
triplets = []
if P % 2 != 0:
    print(f"Perimeter {P} is not an even integer, no integer Pythagorean Triples can exist.")
else:
    for a in range(1,(P-1)//3+1):
        numerator = P * (P - 2 * a)
        denominator = 2 * (P - a)
        if not numerator % denominator:
            b = numerator//denominator
            c = P - a - b
            if a <= b:
                if a**2 + b**2 == c**2:
                    triplets.append((a, b, c))
if triplets:
    print(f"Found {len(triplets)} Pythagorean Triplet(s) where a + b + c = {P}:")
    for a, b, c in triplets:
        print(f"a, b, c = {a}, {b}, {c}")
    answer = a*b*c
    print(f"Therefore product abc is {answer}") 
else:
    print(f"No Pythagorean Triplet found where a + b + c = {P}.")

