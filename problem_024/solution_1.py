from itertools import permutations
nth = 10**6
highest_number = 9
numbers = list(range(highest_number+1))
sorted_list = list(permutations(numbers))
combination = "".join(map(str, sorted_list[nth-1]))
print(combination)
