import math 
nth = 10**6
highest_number = 9
numbers = list(range(highest_number+1))
combination = ""
number = nth-1
n = len(numbers)-1
while numbers and number:
    index,number = divmod(number,math.factorial(n))
    combination += str(numbers.pop(index))
    n -= 1
for num in numbers:
    combination += str(num)
print(combination)
