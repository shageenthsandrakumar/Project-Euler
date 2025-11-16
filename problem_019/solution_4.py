quartet_sundays = [
    [2, 2, 2, 2],  # Quartet starts on Sunday (0)
    [2, 2, 1, 2],  # Quartet starts on Monday (1)
    [2, 1, 3, 1],  # Quartet starts on Tuesday (2)
    [1, 3, 1, 1],  # Quartet starts on Wednesday (3)
    [3, 1, 1, 3],  # Quartet starts on Thursday (4)
    [1, 1, 2, 2],  # Quartet starts on Friday (5)
    [1, 2, 2, 1]   # Quartet starts on Saturday (6)
]

# Starting day for 1901
current_day = 2  # Tuesday
total_sundays = 0

# 25 complete 4-year cycles from 1901-2000
for cycle in range(25):
    # Get sundays for this quartet
    sundays_in_quartet = quartet_sundays[current_day]
    total_sundays += sum(sundays_in_quartet)
    
    # After 4 years (1+1+1+2 days), advance by 5 days
    current_day = (current_day + 5) % 7

print(total_sundays)
