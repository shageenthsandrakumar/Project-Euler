# Letter counts for basic number words
ones = [3, 3, 5, 4, 4, 3, 5, 5, 4]      # one through nine
teens = [3, 6, 6, 8, 8, 7, 7, 9, 8, 8]  # ten through nineteen
tens = [6, 6, 5, 5, 5, 7, 6, 6]         # twenty through ninety

# 1-9
total_1_9 = sum(ones) 

# 10-19
total_10_19 = sum(teens) 

# 1-99: each tens word (20-90) appears 10 times, plus 10-19, plus 1-9 appears 9 more times
total_1_99 = 10 * sum(tens) + total_10_19 + 9 * total_1_9 

# 1-1000:
# 100 * (sum of "X hundred" for X=1-9, plus "and" for 1-99 in each hundred)
# = 100 * (10*9 letters for "hundred" + 36 letters for digit words) 
# - 9*3 (no "and" for round hundreds like "one hundred")
# + 10 * 854 (the 1-99 pattern appears in standalone 1-99 plus each hundred)
# + 11 (onethousand)
total = 100 * (10 * 9 + total_1_9) - 9 * 3 + 10 * total_1_99 + 11
print(total)
