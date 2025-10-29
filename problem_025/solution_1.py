import math
digits = 1000
phi = (1 + math.sqrt(5)) / 2
answer = math.ceil((digits-1+0.5*math.log10(5))/math.log10(phi))
print(answer)
