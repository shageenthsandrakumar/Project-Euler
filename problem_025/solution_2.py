import math
digits = 1000
previous = 0
current = 1
threshold = digits-1
n = 1
while math.log10(current) <= threshold:
    previous,current = current,previous+current
    n += 1
print(n)
