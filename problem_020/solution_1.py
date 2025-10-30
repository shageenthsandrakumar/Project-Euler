import math
number = math.prod(list(range(1,101)))
answer = 0
while number > 0:
    answer += number%10
    number //= 10
print(answer)
