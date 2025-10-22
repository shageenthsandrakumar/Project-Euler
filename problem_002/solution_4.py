import math

# constants
phi = (1 + math.sqrt(5)) / 2
psi = (1 - math.sqrt(5)) / 2

# powers for even fibinacci terms
ephi = phi**3
epsi = psi**3
threshold = 4000000
N = 0
sum = 0
E_N = 0
while E_N < threshold:
    N += 1
    E_N = (ephi**N - epsi**N) / math.sqrt(5)
    sum += E_N

sum -= E_N
# round to nearest integer for exact sum
sum = round(sum)
print(sum)
