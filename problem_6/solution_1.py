n = 100
nums = list(range(n+1))
answer = sum(nums)**2-sum([num**2 for num in nums])
print(answer)
