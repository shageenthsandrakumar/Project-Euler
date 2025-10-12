import math

# constants
phi = (1 + math.sqrt(5)) / 2
psi = (1 - math.sqrt(5)) / 2

# powers for even fibinacci terms
ephi = phi**3
epsi = psi**3
N = 0
E_N = 0
while E_N < 4000000:
    N += 1
    E_N = (ephi**N - epsi**N) / sqrt5
#N represents index of first even fibinacci number over threshold.
#Use one less to represent indicies of numbers below threshold. 
N -= 1

# geometric series sums
sum_ephi = ephi * (ephi**N - 1) / (ephi - 1)
sum_epsi = epsi * (epsi**N - 1) / (epsi - 1)

# total sum of even Fibonacci numbers
sum_even = (sum_ephi - sum_epsi) / math.sqrt(5)

# round to nearest integer for exact sum
sum_even = round(sum_even)
print(sum_even)
