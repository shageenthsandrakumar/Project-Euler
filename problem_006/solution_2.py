from fractions import Fraction
n = 100
a = Fraction(n, 2)
a *= (a + Fraction(1, 3))*(4*a*a-1)
print(a.numerator)
