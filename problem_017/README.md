# Problem 17: Number Letter Counts

**Problem source:** [Project Euler Problem 17](https://projecteuler.net/problem=17)

**Problem statement:**

If the numbers $1$ to $5$ are written out in words: one, two, three, four, five, then there are $3 + 3 + 5 + 4 + 4 = 19$ letters used in total.

If all the numbers from $1$ to $1000$ (one thousand) inclusive were written out in words, how many letters would be used?

**NOTE:** Do not count spaces or hyphens. For example, $342$ (three hundred and forty-two) contains $23$ letters and $115$ (one hundred and fifteen) contains $20$ letters. The use of "and" when writing out numbers is in compliance with British usage.

---

## Solution 1: External Library (num2words)

### Approach

- Use the `num2words` Python library to convert each number to its word representation.
- Remove spaces and hyphens from each word string.
- Sum the lengths of all cleaned strings.
- This is the simplest approach requiring minimal code.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Library Usage**
  - The `num2words` library provides a built-in function to convert integers to their English word representations.
  - For example: `num2words(342)` returns `"three hundred and forty-two"`.
  - This library handles all the complex rules of English number naming automatically.

- **Step 2: String Cleaning**
  - The expression `.replace(" ", "").replace("-", "")` removes all spaces and hyphens.
  - This is necessary because the problem explicitly states: "Do not count spaces or hyphens."
  - Example: `"three hundred and forty-two"` becomes `"threehundredandfortytwo"`.

- **Step 3: List Comprehension**
  - The code uses a list comprehension to process all numbers from 1 to 1000:
    ```python
    [len(num2words(i).replace(" ", "").replace("-", "")) for i in range(1, 1001)]
    ```
  - For each number `i`, it:
    1. Converts `i` to words using `num2words(i)`
    2. Removes spaces and hyphens
    3. Calculates the length using `len()`
  - This creates a list of 1000 integers, where each integer is the letter count for that number.

- **Step 4: Summation**
  - The `sum()` function adds all 1000 letter counts together.
  - This gives the total number of letters used for all numbers from 1 to 1000.

- **Efficiency:** This solution is straightforward and highly readable. The `num2words` library handles all edge cases correctly, including British usage of "and". Performance is excellent for 1000 numbers, completing in milliseconds. However, this approach requires an external dependency.

---

## Solution 2: Explicit Loop-Based Calculation

### Approach

- Manually store the letter counts for basic number words (ones, teens, tens).
- Generate the total for 1-99 using explicit loops.
- Calculate the hundreds contributions separately for each digit using a loop.
- Add "one thousand" at the end.
- This approach is more verbose but easier to verify step-by-step.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Base Letter Counts**
  - Same as Solution 1: ones, teens, and tens arrays store letter counts.
  - **Ones (1-9):** `[3, 3, 5, 4, 4, 3, 5, 5, 4]`
  - **Teens (10-19):** `[3, 6, 6, 8, 8, 7, 7, 9, 8, 8]`
  - **Tens (20-90):** `[6, 6, 5, 5, 5, 7, 6, 6]`

- **Step 2: Calculate 1-99 with Explicit Loop**
  - Start with `total = sum(ones) + sum(teens)` (covers 1-19)
  - Loop through each tens place (`t` from 0 to 7, representing 20-90):
    ```python
    for t in range(8):
        total += 10 * tens[t] + sum(ones)
    ```
  - For each tens place (e.g., 20-29):
    - The tens word appears 10 times: `10 * tens[t]`
    - The ones digits (1-9) appear once each, plus one zero: `sum(ones)`
  - Example for 20-29:
    - "twenty" (6 letters) appears 10 times: 60 letters
    - Plus one(3) through nine(4): 36 letters
    - Total for 20-29: 96 letters
  - Store result: `total_1_99 = total` (should be 854)

- **Step 3: Calculate 100-999 with Explicit Loop**
  - Loop through each digit (1-9) to handle each hundred:
    ```python
    for digit in range(9):
        hundred = ones[digit] + 7  # "X hundred"
        hundred_and = hundred + 3   # "X hundred and"
    ```
  - **For each hundred:**
    - `hundred`: letter count for "one hundred", "two hundred", etc.
    - `hundred_and`: letter count for "one hundred and", etc.
  
  - **Add the round hundred:**
    ```python
    total += hundred  # e.g., "one hundred"
    ```
  
  - **Add all non-round numbers (X01-X99):**
    ```python
    total += 99 * hundred_and + total_1_99
    ```
    - The "X hundred and" part appears 99 times: `99 * hundred_and`
    - The 1-99 pattern appears once: `total_1_99`
  
  - **Example for 100-199:**
    - "one hundred": 10 letters (counted once)
    - "one hundred and": 13 letters (counted 99 times)
    - Total: 10 + 99 * 13 + 854 = 10 + 1287 + 854 = 2151 letters

- **Step 4: Add "one thousand"**
  - `total += 11` adds the 11 letters in "onethousand".

- **Efficiency:** This solution is still very efficient, using two simple loops (8 iterations + 9 iterations = 17 total iterations). It's more explicit than Solution 3, making it easier to understand and verify. Performance is essentially instantaneous.

---

## Solution 3: Compact Mathematical Formula

### Approach

- Manually store the letter counts for basic number words (ones, teens, tens).
- Calculate the total using a compact mathematical formula based on the structure of English number names.
- Exploit the repetitive patterns in how numbers are constructed.
- This approach requires no external libraries and is highly optimized.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Base Letter Counts**
  - **Ones (1-9):** `[3, 3, 5, 4, 4, 3, 5, 5, 4]`
    - one(3), two(3), three(5), four(4), five(4), six(3), seven(5), eight(5), nine(4)
  - **Teens (10-19):** `[3, 6, 6, 8, 8, 7, 7, 9, 8, 8]`
    - ten(3), eleven(6), twelve(6), thirteen(8), fourteen(8), fifteen(7), sixteen(7), seventeen(9), eighteen(8), nineteen(8)
  - **Tens (20-90):** `[6, 6, 5, 5, 5, 7, 6, 6]`
    - twenty(6), thirty(6), forty(5), fifty(5), sixty(5), seventy(7), eighty(6), ninety(6)

- **Step 2: Calculate 1-99 Total**
  - **1-9:** `sum(ones) = 36` letters
  - **10-19:** `sum(teens) = 70` letters
  - **20-99:** Each tens word (twenty through ninety) appears 10 times
    - First appearance: "twenty" alone (when it's 20)
    - Next 9 appearances: "twenty" + one(21), two(22), ..., nine(29)
    - Total for all tens: `10 * sum(tens) = 10 * 46 = 460` letters
    - Plus the ones digits (1-9) appear 8 more times (for 20s, 30s, ..., 90s): `8 * sum(ones) = 8 * 36 = 288` letters
  - **Total 1-99:** Initial 1-9 (36) + 10-19 (70) + tens contributions (460 + 288) = 854 letters
  - Calculation in code: `total_1_99 = 10 * sum(tens) + sum(teens) + 9 * sum(ones)`

- **Step 3: Calculate 1-999 Using Hundreds**
  - For each hundred (100-900), we need:
    - The digit word (one through nine)
    - The word "hundred" (7 letters)
    - The word "and" (3 letters) for non-round hundreds
    - The 1-99 pattern for the last two digits
  
  - **Round hundreds (100, 200, ..., 900):**
    - Pattern: "one hundred", "two hundred", etc.
    - 9 occurrences, each without "and"
    - Total: `9 * (sum(ones) + 7) = 9 * (36 + 7) = 9 * 43 = 387` letters (without "and")

  - **Non-round hundreds (101-199, 201-299, ..., 901-999):**
    - Each hundred has 99 non-round numbers
    - Pattern: "X hundred and Y" where Y is from 1-99
    - For each of 9 hundreds, we add:
      - The digit word + "hundred" + "and": appears 99 times per hundred
      - The 1-99 pattern: appears once per hundred
    - Total: `9 * 99 * (sum(ones)/9 + 7 + 3) + 9 * total_1_99`
    - Simplifies to: `99 * (sum(ones) + 90) + 9 * total_1_99`
    - Calculation: `99 * (36 + 90) + 9 * 854 = 99 * 126 + 7686 = 12474 + 7686 = 20160` letters

  - **Total 1-999:** `387 + 20160 = 20547` letters

- **Step 4: Add "one thousand"**
  - The word "onethousand" (without spaces) has 11 letters.
  - Final total: `20547 + 11 = 20558` letters

- **Step 5: Compact Formula in Code**
  - The code uses a highly compact calculation:
    ```python
    total = 100 * (10 * 9 + sum(ones)) - 9 * 3 + 10 * total_1_99 + 11
    ```
  - **Breaking this down:**
    - `100 * (10 * 9 + sum(ones))`: 
      - `10 * 9 = 90` represents "hundred" (7 letters) + "and" (3 letters) = 10 letters, appearing in 9 sets of 100
      - Plus `sum(ones)` for the digit words
      - This calculates all the "X hundred and" contributions across all 100 numbers in each of 9 hundreds
    - `- 9 * 3`: Subtract "and" (3 letters) for the 9 round hundreds (100, 200, ..., 900)
    - `+ 10 * total_1_99`: The 1-99 pattern appears 10 times (once standalone, 9 times within each hundred)
    - `+ 11`: Add "onethousand"

- **Efficiency:** This solution is extremely efficient, using only a handful of arithmetic operations. It requires no loops and completes instantly. The mathematical approach demonstrates deep understanding of the problem structure.

---

## Mathematical Foundation

### English Number Construction Rules

**1-19 (Unique Names):**
- These numbers have completely unique names and must be memorized.
- Examples: one, two, three, ..., nineteen

**20-99 (Tens + Ones):**
- Pattern: `[tens_word] + [ones_word]`
- Special case: multiples of 10 use only the tens word (e.g., "twenty", not "twenty-zero")
- Examples: twenty-one, thirty-five, ninety-nine

**100-999 (Hundreds Pattern):**
- Pattern: `[ones_word] + "hundred"` for multiples of 100
- Pattern: `[ones_word] + "hundred and" + [1-99_pattern]` for non-multiples
- The word "and" is used in British English (not American English)
- Examples: "one hundred", "one hundred and one", "nine hundred and ninety-nine"

**1000:**
- Special case: "one thousand" (11 letters without spaces)

### Pattern Recognition for Optimization

**Key Insight 1: Repetition of 1-99 Pattern**
- The 1-99 pattern appears 10 times total:
  - Once standalone (1-99)
  - Once in each hundred block (101-199, 201-299, ..., 901-999)
- This repetition allows us to calculate 1-99 once and multiply.

**Key Insight 2: Hundreds Structure**
- Each hundred block has identical structure:
  - 1 round hundred (no "and")
  - 99 non-round numbers (with "and")
- Only the digit word changes (one, two, three, ..., nine).
- Total contribution per hundred: `(digit_letters + 7) + 99 * (digit_letters + 10) + 854`

**Key Insight 3: British vs American English**
- **British:** "one hundred and one" (includes "and")
- **American:** "one hundred one" (no "and")
- This problem uses British usage, adding 3 letters per non-round hundred number.
- Total "and" contribution: `9 * 99 * 3 = 2673` letters

### Verification Examples

**Example 1: 342 = "three hundred and forty-two"**
- three (5) + hundred (7) + and (3) + forty (5) + two (3) = 23 letters ✓

**Example 2: 115 = "one hundred and fifteen"**
- one (3) + hundred (7) + and (3) + fifteen (7) = 20 letters ✓

**Example 3: 100 = "one hundred"**
- one (3) + hundred (7) = 10 letters (no "and") ✓

**Example 4: 1000 = "one thousand"**
- one (3) + thousand (8) = 11 letters ✓

---

## Comparison of Solutions

| Aspect | Solution 1<br>(num2words) | Solution 2<br>(Compact Formula) | Solution 3<br>(Explicit Loop) |
|--------|---------------------------|----------------------------------|-------------------------------|
| **Approach** | External library | Mathematical formula | Explicit calculation |
| **Dependencies** | Requires `num2words` | None | None |
| **Code Length** | 1 line | ~10 lines | ~20 lines |
| **Performance** | Fast | Instant | Instant |
| **Extensibility** | Easy (change range) | Manual formula update | Easy (change loops) |
| **Educational Value** | Low | High | Very High |
| **Maintenance** | Depends on library | Self-contained | Self-contained |
| **Best For** | Quick prototyping | Optimal efficiency | Learning/verification |

---

## Output

```
21124
```

---

## Notes

- The total number of letters used when writing all numbers from 1 to 1000 in words is **21,124**.
- **Solution 1** is the simplest and most practical for real-world use, leveraging a well-tested library.
- **Solution 2** provides the clearest step-by-step calculation, making it ideal for understanding and verification.
- **Solution 3** demonstrates mathematical optimization and is the most efficient in terms of operations.
- The British usage of "and" adds exactly **2,673 letters** to the total (9 hundreds × 99 non-round numbers × 3 letters).
- Without "and" (American English), the total would be **18,451 letters**.
- The problem elegantly demonstrates how pattern recognition and mathematical thinking can replace brute-force iteration.
- All three solutions correctly handle edge cases like round hundreds (100, 200, ..., 900) and the special case of 1000.
- The letter counts for basic words are:
  - Shortest: "six" (3 letters)
  - Longest in ones: "three", "seven", "eight" (5 letters)
  - Longest in teens: "seventeen" (9 letters)
  - Longest in tens: "seventy" (7 letters)
- The repetitive structure of English number names makes this problem ideal for demonstrating the power of mathematical analysis over brute-force computation.
