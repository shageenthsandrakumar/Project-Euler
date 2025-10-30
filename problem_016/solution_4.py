number = 2**1000
answer = 0
while number:
    number, digit = divmod(number, 10)
    answer += digit
print(answer)
