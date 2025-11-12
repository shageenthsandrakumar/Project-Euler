ones = [3, 3, 5, 4, 4, 3, 5, 5, 4]  #  one, two,three, ..., nine
teens = [3, 6, 6, 8, 8, 7, 7, 9, 8, 8]  # ten, eleven, ..., nineteen
tens = [6, 6, 5, 5, 5, 7, 6, 6]   # twenty, thirty, ..., ninety

total = sum(ones)+sum(teens)
for t in range(8):
    total += 10 * tens[t] + sum(ones)
total_1_99 = total
for digit in range(9):
    hundred = ones[digit] + 7  # "hundred" = 7 letters
    hundred_and = hundred + 3   # "and" = 3 letters
    
    # The "X hundred" itself (e.g., "one hundred")
    total += hundred
    
    # "X hundred and Y" for all 1-99
    total += 99 * hundred_and + total_1_99

# 1000
total += 11  # "onethousand" = 11 letters
print(total)
