from fractions import Fraction
n = 10
a = Fraction(n, 2)
a *= (4 * a**2 - 1) * (a + Fraction(1, 3))
print(a.numerator)
