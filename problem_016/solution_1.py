number = 2**1000
answer = 0
while number > 0:
    answer += number%10
    number //= 10
print(answer)
