# Problem 19: Counting Sundays

**Problem source:** [Project Euler Problem 19](https://projecteuler.net/problem=19)

**Problem statement:**

You are given the following information, but you may prefer to do some research for yourself.

- 1 Jan 1900 was a Monday.
- Thirty days has September, April, June and November.
- All the rest have thirty-one,
- Saving February alone,
- Which has twenty-eight, rain or shine.
- And on leap years, twenty-nine.
- A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.

How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?

---

## Solution 1: Brute Force Day Iteration

### Approach

- Start from 1 Jan 1900 (Monday) and iterate through every single day.
- Track the current day of the week as we advance through dates.
- Check if each day is both the 1st of the month and a Sunday.
- Count all such occurrences from 1 Jan 1901 to 31 Dec 2000.
- This is the most straightforward approach but requires iterating through all 36,525 days.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Initialization**
  - Start from 1 Jan 1900: `year = 1900`, `month = 1`, `day = 1`.
  - Initialize `day_of_week = 1` (Monday, using 0=Sunday convention).
  - Set `count = 0` to track Sundays on the first.

- **Step 2: Day-by-Day Iteration**
  - The outer loop `while year <= 2000:` continues until the end of year 2000.
  - The middle loop `while month <= 12:` iterates through all months in a year.
  - The innermost loop `while day <= days_in_month:` iterates through each day.
  - **Key check:** `if day == 1 and day_of_week == 0 and year >= 1901:`
    - Only count if it's the 1st of the month (`day == 1`).
    - Only count if it's a Sunday (`day_of_week == 0`).
    - Only count starting from 1901 (`year >= 1901`).

- **Step 3: Day of Week Tracking**
  - After each day: `day_of_week = (day_of_week + 1) % 7`.
  - This cycles through: Monday(1) → Tuesday(2) → ... → Saturday(6) → Sunday(0) → Monday(1).

- **Step 4: Month and Year Management**
  - Determine `days_in_month` using the leap year rule:
    - Most months have fixed days: 31 for Jan, Mar, May, Jul, Aug, Oct, Dec; 30 for Apr, Jun, Sep, Nov.
    - February: 29 if leap year, 28 otherwise.
  - **Leap year logic:**
    ```python
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        # It's a leap year
    ```
  - After all days in a month: `month += 1`.
  - After all months in a year: `year += 1`, `month = 1`.

- **Efficiency:** This solution iterates through all 36,525 days in the century (including the starting year 1900). While conceptually simple, it performs unnecessary work by checking every single day rather than just the first of each month.

---

## Solution 2: Built-in Date Library

### Approach

- Use Python's built-in `datetime` module to handle all date arithmetic.
- Iterate through only the first day of each month from Jan 1901 to Dec 2000.
- For each first-of-month, use `.weekday()` to determine the day of week.
- Count occurrences where the weekday is Sunday (6 in Python's weekday convention).
- This is the most concise and reliable approach, leveraging well-tested library code.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Understanding Python's datetime.weekday()**
  - `weekday()` returns: Monday=0, Tuesday=1, ..., Saturday=5, Sunday=6.
  - We check for `weekday() == 6` to identify Sundays.

- **Step 2: Month Iteration**
  - Loop through years: `for year in range(1901, 2001)`.
  - Loop through months: `for month in range(1, 13)` (1=January, 12=December).
  - Create a date object for the 1st: `date(year, month, 1)`.

- **Step 3: Summing with Generator Expression**
  - The code uses a nested generator expression with `sum()`:
    ```python
    sum(1 for year in range(1901, 2001) 
          for month in range(1, 13) 
          if date(year, month, 1).weekday() == 6)
    ```
  - This is a Pythonic one-liner that:
    - Generates the value `1` for each condition that's true.
    - Sums all the `1`s to get the total count.
  - **Equivalent to:**
    ```python
    count = 0
    for year in range(1901, 2001):
        for month in range(1, 13):
            if date(year, month, 1).weekday() == 6:
                count += 1
    ```

- **Step 4: Why This Works**
  - The `datetime` module correctly handles:
    - All leap year rules (including the century exception).
    - Day-of-week calculations across any date range.
    - Month lengths automatically.
  - We only check 1,200 dates (100 years × 12 months) instead of 36,525 days.

- **Efficiency:** This solution is both concise and efficient. It examines only 1,200 dates rather than all 36,525 days. The datetime library is implemented in C and highly optimized. This is the recommended approach for production code.

---

## Solution 3: Year-Based Precomputed Pattern

### Approach

- Recognize that the number of Sundays on the 1st depends on which day of the week the year starts.
- Precompute lookup tables for normal years and leap years.
- Each table maps the starting day of the year (0-6) to the count of Sundays on the 1st.
- Iterate through years, tracking the starting day and accumulating Sunday counts.
- This approach exploits mathematical patterns to minimize computation.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Understanding the Pattern**
  - If a year starts on Sunday (day 0), certain months will have their 1st on Sunday.
  - The pattern of which months depends on:
    - The starting day of the year.
    - Whether it's a leap year (affecting when days shift).
  - Rather than computing this dynamically, we precompute and store it.

- **Step 2: Precomputed Lookup Tables**
  - **Normal year table (`normal_year_sundays`):**
    ```python
    [2, 2, 2, 1, 3, 1, 1]  # Index = starting day (0-6)
    ```
    - If a normal year starts on Sunday (0): 2 months have 1st on Sunday.
    - If it starts on Monday (1): 2 months have 1st on Sunday.
    - If it starts on Thursday (4): 3 months have 1st on Sunday.
  - **Leap year table (`leap_year_sundays`):**
    ```python
    [3, 2, 1, 2, 2, 1, 1]  # Index = starting day (0-6)
    ```
    - Similar pattern but adjusted for the extra day in February.

- **Step 3: How These Tables Were Created**
  - For each possible starting day (0-6), determine which months have their 1st on Sunday.
  - **Example: Year starts on Thursday (4) - Normal Year**
    - Jan 1: Thursday
    - Feb 1: Thursday + 31 days = Sunday (31 ≡ 3 mod 7, so Thu + 3 = Sun)
    - Mar 1: Thursday + (31+28) = 59 days = Thursday (59 ≡ 3 mod 7)
    - Continue for all 12 months...
    - Count: 3 months have 1st on Sunday
  - This process is done for all 7 starting days and both year types.

- **Step 4: Year Advancement Formula**
  - A **normal year** has 365 days = 52 weeks + 1 day.
    - Next year starts 1 day later: `(current_day + 1) % 7`.
  - A **leap year** has 366 days = 52 weeks + 2 days.
    - Next year starts 2 days later: `(current_day + 2) % 7`.

- **Step 5: Main Iteration**
  - Start with 1901, which began on Tuesday (day 2).
  - For each year from 1901 to 2000:
    - Determine if it's a leap year using the standard rule.
    - Look up the Sunday count in the appropriate table: `sundays[current_day]`.
    - Add this count to the total.
    - Advance `current_day` by 1 or 2 depending on the year type.

- **Step 6: Example Walkthrough**
  - 1901 starts on Tuesday (2), is not leap → `normal_year_sundays[2] = 2` Sundays.
  - Next year starts on Wednesday (2+1=3).
  - 1902 starts on Wednesday (3), is not leap → `normal_year_sundays[3] = 1` Sunday.
  - 1903 starts on Thursday (4), is not leap → `normal_year_sundays[4] = 3` Sundays.
  - 1904 starts on Friday (5), **is leap** → `leap_year_sundays[5] = 1` Sunday.
  - Next year starts on Sunday (5+2=7≡0).

- **Efficiency:** This solution only performs 100 iterations (one per year) with simple table lookups. No date arithmetic or month iteration required. This is the most computationally efficient approach, though it requires understanding and precomputing the patterns.

---

## Solution 4: 4-Year Cycle Optimization

### Approach

- Exploit the fact that the Gregorian calendar has a **4-year leap cycle**.
- Precompute the Sunday counts for entire 4-year cycles (quartets).
- Each quartet consists of: normal year, normal year, normal year, leap year.
- The 20th century (1901-2000) contains exactly 25 complete 4-year cycles.
- Track the starting day through cycles and sum the precomputed values.
- This reduces 100 iterations to just 25.

**Reference:** The full Python implementation is available in [`solution_4.py`](solution_4.py).

### Detailed Explanation

- **Step 1: Understanding the 4-Year Cycle**
  - Years advance: normal (1 day), normal (1 day), normal (1 day), leap (2 days).
  - Total advancement: 1 + 1 + 1 + 2 = 5 days per cycle.
  - After 4 years, the starting day advances by 5 days in the week.

- **Step 2: Precomputed Quartet Table**
  - `quartet_sundays[i]` gives an array of 4 values: Sunday counts for each year in a quartet starting on day `i`.
  ```python
  quartet_sundays = [
      [2, 2, 2, 2],  # Quartet starts on Sunday (0)
      [2, 2, 1, 2],  # Quartet starts on Monday (1)
      [2, 1, 3, 1],  # Quartet starts on Tuesday (2)
      [1, 3, 1, 1],  # Quartet starts on Wednesday (3)
      [3, 1, 1, 3],  # Quartet starts on Thursday (4)
      [1, 1, 2, 2],  # Quartet starts on Friday (5)
      [1, 2, 2, 1]   # Quartet starts on Saturday (6)
  ]
  ```

- **Step 3: How the Quartet Table Was Created**
  - For a quartet starting on day `i`, determine:
    - Year 1 (normal): Sundays using `normal_year_sundays[i]`.
    - Year 2 (normal): Starts on `(i+1)%7`, use `normal_year_sundays[(i+1)%7]`.
    - Year 3 (normal): Starts on `(i+2)%7`, use `normal_year_sundays[(i+2)%7]`.
    - Year 4 (leap): Starts on `(i+3)%7`, use `leap_year_sundays[(i+3)%7]`.
  - **Example: Quartet starting on Tuesday (2)**
    - Year 1: Tuesday → `normal_year_sundays[2] = 2`
    - Year 2: Wednesday → `normal_year_sundays[3] = 1`
    - Year 3: Thursday → `normal_year_sundays[4] = 3`
    - Year 4 (leap): Friday → `leap_year_sundays[5] = 1`
    - Quartet array: `[2, 1, 3, 1]`

- **Step 4: Main Loop**
  - 1901 starts on Tuesday (day 2).
  - The 100 years from 1901-2000 contain 25 complete 4-year cycles.
  - For each cycle:
    - Look up `quartet_sundays[current_day]`.
    - Sum all 4 values in the array: `sum([2, 1, 3, 1]) = 7`.
    - Add this to the running total.
    - Advance by 5 days: `current_day = (current_day + 5) % 7`.

- **Step 5: Example Cycles**
  - **Cycle 1 (1901-1904):** Starts Tuesday (2) → `[2, 1, 3, 1]` → 7 Sundays → Next starts Sunday (0).
  - **Cycle 2 (1905-1908):** Starts Sunday (0) → `[2, 2, 2, 2]` → 8 Sundays → Next starts Friday (5).
  - **Cycle 3 (1909-1912):** Starts Friday (5) → `[1, 1, 2, 2]` → 6 Sundays → Next starts Wednesday (3).
  - Continue for all 25 cycles...

- **Efficiency:** This is the most optimized solution in terms of iteration count. Only 25 loop iterations (one per 4-year cycle) compared to 100 (one per year) or 1,200 (one per month). The precomputed table makes each iteration a simple array lookup and sum. This demonstrates deep understanding of calendar mathematics.

---

## Mathematical Foundation

### The Gregorian Calendar Structure

The Gregorian calendar has a complex but predictable structure based on leap year rules:

**Leap Year Rules:**
- A year is a leap year if:
  - It's divisible by 4, **AND**
  - It's NOT divisible by 100, **OR** it IS divisible by 400.
- Expressed mathematically:
  $$\text{leap}(y) = (y \bmod 4 = 0) \land [(y \bmod 100 \neq 0) \lor (y \bmod 400 = 0)]$$

**Examples:**
- 1900: divisible by 4 ✓, divisible by 100 ✓, NOT divisible by 400 ✗ → **Not leap**
- 1904: divisible by 4 ✓, NOT divisible by 100 ✓ → **Leap**
- 2000: divisible by 4 ✓, divisible by 100 ✓, divisible by 400 ✓ → **Leap**

### Day Advancement Through Years

**Normal Year (365 days):**
- 365 = 52 weeks + 1 day
- If Jan 1 is on day $d$, next Jan 1 is on day $(d+1) \bmod 7$

**Leap Year (366 days):**
- 366 = 52 weeks + 2 days
- If Jan 1 is on day $d$, next Jan 1 is on day $(d+2) \bmod 7$

**4-Year Cycle:**
- Normal + Normal + Normal + Leap = 1 + 1 + 1 + 2 = 5 days advancement
- Starting day after 4 years: $(d+5) \bmod 7$

### Why Precomputation Works

For any given starting day of the year, the pattern of which months have their 1st on Sunday is **fixed** and depends only on:
1. The starting day (0-6)
2. Whether it's a leap year (affects February)

Since there are only 7 possible starting days and 2 year types (normal/leap), we only need to compute 14 patterns total. These patterns repeat predictably, making precomputation highly effective.

### The 400-Year Cycle

The Gregorian calendar repeats exactly every 400 years because:
- 400 years = 303 normal years + 97 leap years
- Total days = $303 \times 365 + 97 \times 366 = 146{,}097$ days
- $146{,}097 = 20{,}871 \text{ weeks}$ (exactly, no remainder)

This means the calendar on 1 Jan 2001 is identical to 1 Jan 2401.

---

## Comparison of Solutions

| Aspect | Solution 1<br>(Day Iteration) | Solution 2<br>(datetime) | Solution 3<br>(Year Pattern) | Solution 4<br>(Quartet Cycle) |
|--------|------------------------------|--------------------------|------------------------------|-------------------------------|
| **Approach** | Iterate all days | Library functions | Precomputed year patterns | Precomputed 4-year cycles |
| **Iterations** | 36,525 days | 1,200 months | 100 years | 25 cycles |
| **Dependencies** | None | Python datetime | None | None |
| **Precomputation** | None | None | 14 patterns (7×2) | 7 quartet arrays |
| **Code Clarity** | ★★★★★ | ★★★★★ | ★★★ | ★★★ |
| **Speed** | Slowest | Very fast | Very fast | Fastest |
| **Educational Value** | Shows basic logic | Production approach | Calendar mathematics | Advanced optimization |
| **Best For** | Understanding | Production code | Efficiency | Competition/optimization |

---

## Output

```
171
```

---

## Notes

- There are exactly **171 Sundays** that fell on the first of the month during the 20th century (1 Jan 1901 to 31 Dec 2000).
- **Solution 2** (datetime library) is the recommended approach for production code: it's concise, reliable, and leverages well-tested library code.
- **Solution 4** (quartet optimization) demonstrates deep understanding of calendar mathematics and is the most computationally efficient, but at the cost of complexity.
- **Solution 3** bridges the gap between manual calculation and extreme optimization, showing how recognizing patterns can dramatically improve efficiency.
- **Solution 1** is valuable for understanding the problem but impractical due to excessive iteration.
- The problem illustrates an important software engineering principle: **use existing, well-tested libraries when available** (Solution 2), but understanding the underlying mathematics (Solutions 3 & 4) enables optimization when needed.
- The estimate $\frac{1200}{7} \approx 171.4$ is remarkably close to the actual answer, showing that Sundays are roughly evenly distributed across the first of months.
- All four solutions correctly handle the century leap year rule: 1900 was not a leap year, but 2000 was.
- The 20th century started on Tuesday (1 Jan 1901) and ended on Sunday (31 Dec 2000), coincidentally bookending with the day we're counting.
