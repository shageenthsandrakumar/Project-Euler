normal_year_sundays = [
    2,  # Year starts on Sunday (0)
    2,  # Year starts on Monday (1)
    2,  # Year starts on Tuesday (2)
    1,  # Year starts on Wednesday (3)
    3,  # Year starts on Thursday (4)
    1,  # Year starts on Friday (5)
    1   # Year starts on Saturday (6)
]

# Leap years
leap_year_sundays = [
    3,  # Leap year starts on Sunday (0)
    2,  # Leap year starts on Monday (1)
    1,  # Leap year starts on Tuesday (2)
    2,  # Leap year starts on Wednesday (3)
    2,  # Leap year starts on Thursday (4)
    1,  # Leap year starts on Friday (5)
    1   # Leap year starts on Saturday (6)
]

# 1901 started on a Tuesday (day 2)
current_day = 2
total_sundays = 0

# Process years 1901-2000
for year in range(1901, 2001):
    # Determine if leap year
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    # Add the number of Sundays for this year
    if is_leap:
        total_sundays += leap_year_sundays[current_day]
    else:
        total_sundays += normal_year_sundays[current_day]
    
    # Calculate starting day for next year
    if is_leap:
        current_day = (current_day + 2) % 7  # Leap year advances by 2
    else:
        current_day = (current_day + 1) % 7  # Normal year advances by 1

print(total_sundays)
