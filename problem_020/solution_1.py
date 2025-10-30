import math
number = math.factorial(100)
answer = 0
while number > 0:
    answer += number%10
    number //= 10
print(answer)
