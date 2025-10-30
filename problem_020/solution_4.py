import math
number = math.factorial(100)
answer = 0
while number:
    number, digit = divmod(number, 10)
    answer += digit
print(answer)
