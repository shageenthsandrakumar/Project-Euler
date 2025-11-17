# Problem 22: Names Scores

**Problem source:** [Project Euler Problem 22](https://projecteuler.net/problem=22)

**Problem statement:**

Using a text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth $3 + 15 + 12 + 9 + 14 = 53$, is the 938th name in the list. So, COLIN would obtain a score of $938 \times 53 = 49714$.

What is the total of all the name scores in the file?

**NOTE:** The alphabetical value of a name is the sum of the values of its letters, where A=1, B=2, C=3, ..., Z=26.

---

## Solution 1: Sort-Based Approach

### Approach

- Read the names from the input file and parse them into a list.
- Sort the list of names alphabetically using Python's built-in `sort()` method.
- For each name, calculate its alphabetical value by summing the values of its letters.
- Multiply each name's alphabetical value by its position (1-indexed) in the sorted list.
- Sum all the individual name scores to get the total.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Parse Input File**
  - Read the file content: `file.read()`.
  - The file contains names in the format: `"NAME1","NAME2","NAME3",...`.
  - Split by comma: `text.split(",")`.
  - Remove quotes from each name: `name.replace('"', '')`.
  - Result: a list of clean name strings: `['MARY', 'PATRICIA', 'LINDA', ...]`.

- **Step 2: Sort Names Alphabetically**
  - Use `names.sort()` to sort the list in place.
  - Python's `sort()` uses the Timsort algorithm, which efficiently handles the sorting.
  - After sorting, the first name alphabetically is at index 0, the second at index 1, etc.

- **Step 3: Calculate Name Value**
  - For each character in a name, convert it to its alphabetical value:
    - `ord(n.lower()) - 96` converts a lowercase letter to its position (a=1, b=2, ..., z=26).
    - **Why `ord(n.lower())`?** The `ord()` function returns the Unicode code point of a character.
      - For lowercase letters: a=97, b=98, c=99, ..., z=122.
      - Subtracting 96 gives: a=1, b=2, c=3, ..., z=26.
    - The `.lower()` ensures the calculation works regardless of the original case.
  - Sum all letter values: `sum(ord(n.lower()) - 96 for n in names[i])`.

- **Step 4: Calculate Name Score**
  - The position of a name in the sorted list is `i + 1` (since list indices start at 0).
  - Name score = position × alphabetical value = `(i+1) * sum(ord(n.lower()) - 96 for n in names[i])`.

- **Step 5: Calculate Total Score**
  - Use a generator expression within `sum()` to compute all name scores:
    ```python
    sum((i+1)*sum(ord(n.lower()) - 96 for n in names[i]) for i in range(len(names)))
    ```
  - This iterates through all indices, calculates each name's score, and sums them.

- **Step 6: Example Walkthrough (COLIN)**
  - Alphabetical value:
    - C = 3, O = 15, L = 12, I = 9, N = 14
    - Sum = 3 + 15 + 12 + 9 + 14 = 53
  - After sorting, COLIN is at position 938.
  - Name score = 938 × 53 = 49,714

- **Efficiency:** This solution is clean and straightforward. The sorting operation dominates the runtime, and calculating the alphabetical values is done efficiently using generator expressions. For the given input of ~5,000 names, this completes in milliseconds.

---

## Solution 2: Counting-Based Approach (No Explicit Sorting)

### Approach

- Instead of explicitly sorting the names, determine each name's position by counting how many names come before it alphabetically.
- For each name, calculate its alphabetical value.
- Multiply the alphabetical value by the position (determined by counting).
- Sum all the individual name scores to get the total.
- This approach avoids explicit sorting by using comparison operations instead.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Parse Input File**
  - Same as Solution 1: read the file, split by comma, and remove quotes.
  - Result: a list of names without any sorting.

- **Step 2: Calculate Name Value Function**
  - Define `name_value(name)` to compute the alphabetical value:
    ```python
    def name_value(name):
        return sum(ord(char) - 64 for char in name)
    ```
  - **Why `ord(char) - 64`?** 
    - For uppercase letters: A=65, B=66, C=67, ..., Z=90.
    - Subtracting 64 gives: A=1, B=2, C=3, ..., Z=26.
  - This function works directly with uppercase letters (as they appear in the input file).

- **Step 3: Count Names Before (Position Calculation)**
  - Define `count_names_before(target, names)` to count how many names come alphabetically before `target`:
    ```python
    def count_names_before(target, names):
        return sum(1 for name in names if name < target)
    ```
  - Python's string comparison is lexicographic (dictionary order).
  - For example: `'ALICE' < 'BOB'` is `True` because 'ALICE' comes before 'BOB' alphabetically.
  - The position of `target` in a sorted list = `count_names_before(target, names) + 1`.

- **Step 4: Calculate Total Score**
  - For each name, compute:
    - Position = `count_names_before(name, names) + 1`
    - Alphabetical value = `name_value(name)`
    - Name score = position × alphabetical value
  - Use a generator expression to sum all scores:
    ```python
    sum((count_names_before(name, names) + 1) * name_value(name) for name in names)
    ```

- **Step 5: Example Walkthrough (COLIN)**
  - Alphabetical value using `name_value('COLIN')`:
    - C=3, O=15, L=12, I=9, N=14 → 53
  - Count names before 'COLIN': 937 names come alphabetically before it.
  - Position = 937 + 1 = 938
  - Name score = 938 × 53 = 49,714

- **Why This Works Without Explicit Sorting:**
  - The key insight is that **a name's position in a sorted list equals the count of names before it plus one**.
  - String comparison in Python naturally gives lexicographic ordering.
  - We simulate the sorting process by comparing each name against all others.

- **Efficiency:** This solution is less efficient than Solution 1 because counting names before each name requires comparing it against all other names. For ~5,000 names, this means roughly 5,000 × 5,000 = 25 million comparisons, whereas sorting requires roughly 5,000 × log(5,000) ≈ 44,000 comparisons. However, it demonstrates an interesting alternative approach that avoids explicit sorting.

---

## Mathematical Foundation

### Alphabetical Value Calculation

For a name consisting of letters, the alphabetical value is the sum of the positions of its letters in the alphabet:

$$\text{Value}(\text{name}) = \sum_{i=1}^{n} \text{position}(\text{letter}_i)$$

where $\text{position}(A) = 1, \text{position}(B) = 2, \ldots, \text{position}(Z) = 26$.

**Implementation using ASCII:**
- Uppercase: `ord('A') = 65`, so `position = ord(char) - 64`
- Lowercase: `ord('a') = 97`, so `position = ord(char) - 96`

### Name Score Calculation

For a name at position $p$ in the sorted list with alphabetical value $v$:

$$\text{Score}(\text{name}) = p \times v$$

### Total Score

The total score for all names is:

$$\text{Total} = \sum_{i=1}^{n} i \times \text{Value}(\text{name}_i)$$

where names are indexed in sorted order.

### Lexicographic Ordering

Python's string comparison uses **lexicographic (dictionary) ordering**:
- Compare characters from left to right.
- The first differing character determines the order.
- Shorter strings come before longer strings if all compared characters are equal.

**Examples:**
- `'ALICE' < 'BOB'` because 'A' < 'B'
- `'ALICE' < 'ALICIA'` because 'ALICE' is a prefix of 'ALICIA'
- `'ZEBRA' > 'APPLE'` because 'Z' > 'A'

---

## Comparison of Solutions

| Aspect | Solution 1 (Sort-Based) | Solution 2 (Counting-Based) |
|--------|-------------------------|------------------------------|
| **Approach** | Explicit sorting then indexing | Count comparisons for position |
| **Sorting** | Uses `sort()` method | No explicit sorting |
| **Position Calculation** | Direct indexing | Count names before each name |
| **Operations** | ~44,000 comparisons (sort) | ~25,000,000 comparisons |
| **Code Clarity** | ★★★★★ | ★★★★ |
| **Speed** | Very fast | Slower for large inputs |
| **Best For** | Production code | Demonstrating alternative approach |

---

## Output

```
871198282
```

---

## Notes

- The total score for all names in the file is **871,198,282**.
- **Solution 1** is the recommended approach for production code, leveraging Python's highly optimized sorting algorithm.
- **Solution 2** demonstrates an interesting conceptual approach: determining positions without explicit sorting by counting comparisons. While less efficient, it shows how sorting can be simulated through counting.
- The example name COLIN has an alphabetical value of 53 and appears at position 938, giving a score of 49,714.
- Python's lexicographic string comparison makes it easy to work with alphabetical ordering without manual character-by-character comparison.
- The problem elegantly combines sorting, character encoding, and arithmetic to create a unique scoring system.
- For Solution 1, using `ord(char.lower()) - 96` vs. `ord(char) - 64` (for uppercase) are equivalent approaches, depending on whether you choose to work with lowercase or uppercase letters.
- Both solutions correctly handle the input file format with quoted, comma-separated names.
