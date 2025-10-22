import math

# constants
phi = (1 + math.sqrt(5)) / 2
psi = (1 - math.sqrt(5)) / 2

# powers for even fibinacci terms
ephi = phi**3
epsi = psi**3
threshold = 4000000

#Using Binet's approximation to find a candidate value for N
n_cand = math.log(threshold * math.sqrt(5)) // math.log(ephi)

#We must check index below just in case because Binet's appoximation is an upper bound. 
N = n_cand-1
E_N = (ephi**N - epsi**N) / math.sqrt(5)
while E_N < threshold:
    N += 1
    E_N = (ephi**N - epsi**N) / math.sqrt(5)

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
