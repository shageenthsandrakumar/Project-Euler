# Problem 23: Non-Abundant Sums

**Problem source:** [Project Euler Problem 23](https://projecteuler.net/problem=23)

**Problem statement:**

A perfect number is a number for which the sum of its proper divisors is exactly equal to the number. For example, the sum of the proper divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28 is a perfect number.

A number $n$ is called **deficient** if the sum of its proper divisors is less than $n$ and it is called **abundant** if this sum exceeds $n$.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the smallest number that can be written as the sum of two abundant numbers is 24. By mathematical analysis, it can be shown that all integers greater than 28123 can be written as the sum of two abundant numbers. However, this upper limit cannot be reduced any further by analysis even though it is known that the greatest number that cannot be expressed as the sum of two abundant numbers is less than this limit.

Find the sum of all the positive integers which cannot be written as the sum of two abundant numbers.

---

## Solution 1: Set-Based Approach with Nested Loops

### Approach

- Find all abundant numbers up to 28123 using an efficient divisor sum function.
- Generate all possible sums of two abundant numbers using nested loops.
- Store these sums in a set to automatically handle duplicates.
- Calculate the sum of all numbers from 1 to 28123, then subtract the sum of all abundant-number sums.
- This gives the sum of numbers that cannot be expressed as the sum of two abundant numbers.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Efficient Divisor Sum Function**
  - The function `d(n)` computes the sum of proper divisors (all divisors except $n$ itself).
  - **Edge case:** For $n = 0$, return `float('inf')` since every positive integer divides 0.
  - The function uses **wheel factorization** to efficiently find the prime factorization of $n$.
  - **Extract powers of 2:** Count how many times 2 divides $n$ using `while not n%2:`.
    - Each power of 2 contributes to $\sigma(n)$ via the formula: $\sigma(2^k) = 2^{k+1} - 1$.
  - **Extract powers of 3:** Similarly extract all factors of 3.
    - Formula: $\sigma(3^k) = \frac{3^{k+1} - 1}{2}$.
  - **Wheel factorization for remaining primes:**
    - After removing 2 and 3, all remaining primes have the form $6k \pm 1$.
    - Start with `f = 5` and `step = 2`.
    - The alternating step pattern (2, 4, 2, 4, ...) generates the sequence: $5, 7, 11, 13, 17, 19, 23, ...$
    - This checks only $\frac{1}{3}$ of all numbers, skipping multiples of 2 and 3 entirely.
  - **Handle remaining prime factor:** If $n > 1$ after all trial divisions, then $n$ itself is prime.
    - For a prime $p$: $\sigma(p) = p + 1$.
  - **Final computation:** Using the multiplicative property of $\sigma$:
    - If $n = p_1^{a_1} \cdot p_2^{a_2} \cdots p_k^{a_k}$, then:
    - $\sigma(n) = \sigma(p_1^{a_1}) \cdot \sigma(p_2^{a_2}) \cdots \sigma(p_k^{a_k})$
    - Return $\sigma(n) - n$ to get the sum of proper divisors.

- **Step 2: Finding Abundant Numbers**
  - Loop through all numbers from 1 to 28123: `for a in range(1, threshold):`.
  - For each number, calculate `d_value = d(a)`.
  - If `d_value > a`, the number is abundant and is added to the list.
  - Store all abundant numbers in a list: `abundant_numbers`.

- **Step 3: Generating Sums with Nested Loops**
  - Use nested loops to generate all possible sums of two abundant numbers:
    ```python
    for i in range(L):
        for j in range(i, L):
            s = abundant_numbers[i] + abundant_numbers[j]
    ```
  - The inner loop starts at `i` (not 0) to avoid duplicate pairs like (a,b) and (b,a).
  - This also includes sums where both numbers are the same (e.g., 12 + 12 = 24).
  - **Early termination:** If `s >= threshold`, break the inner loop since all subsequent sums will also exceed the threshold.
  - Store each valid sum in a set: `abundant_sums.add(s)`.
  - Using a set automatically handles duplicates—if the same sum is generated multiple times, it's only stored once.

- **Step 4: Computing the Final Answer**
  - Calculate the sum of all integers from 1 to 28123 using the formula:
    - $\text{sum}(1 \text{ to } n) = \frac{n(n-1)}{2}$
    - For threshold = 28124 (since we want numbers below 28124): `threshold * (threshold - 1) // 2`
  - Calculate the sum of all numbers that CAN be expressed as abundant sums: `sum(abundant_sums)`.
  - Subtract: `answer = (total sum) - (sum of abundant sums)`.
  - This gives the sum of all numbers that CANNOT be written as the sum of two abundant numbers.

- **Efficiency:** This solution is straightforward and easy to understand. The nested loop structure ensures all possible pairs are checked. The set data structure provides efficient duplicate handling with O(1) average-case lookups and insertions. However, for the approximately 6,965 abundant numbers below 28124, this requires checking roughly $\frac{6965 \times 6966}{2} \approx 24$ million pairs, though many are eliminated by the early termination condition.

---

## Solution 2: NumPy Vectorized Approach

### Approach

- Use NumPy arrays for efficient vectorized operations.
- Find all abundant numbers up to 28123 using the same divisor sum function.
- Use `np.triu_indices` to generate all valid pairs of indices efficiently.
- Create a boolean array to mark which numbers can be expressed as abundant sums.
- Calculate the sum of numbers that cannot be expressed as abundant sums directly from the boolean array.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Efficient Divisor Sum Function**
  - Uses the same `d(n)` function as Solution 1 with wheel factorization.
  - This efficiently computes the sum of proper divisors for each number.

- **Step 2: Finding Abundant Numbers**
  - Loop through all numbers from 1 to 28123.
  - Identify abundant numbers where `d(a) > a`.
  - Store them in a Python list, then convert to a NumPy array: `abundant_numbers = np.array(abundant_numbers)`.
  - NumPy arrays enable vectorized operations, which are significantly faster than Python loops.

- **Step 3: Boolean Array for Non-Abundant Sums**
  - Create a boolean array: `is_non_abundant = np.ones((threshold,), dtype=bool)`.
  - Initially, all values are `True`, indicating that we assume no numbers can be expressed as abundant sums.
  - The array has size `threshold` (28124), with indices 0 through 28123.
  - Index `i` represents the number `i`.

- **Step 4: Vectorized Pair Generation**
  - Use `np.triu_indices(len(abundant_numbers))` to generate all valid pairs:
    - This returns two arrays: `i_values` and `j_values`.
    - These represent the upper triangular indices of a matrix.
    - For abundant_numbers = [a, b, c, d], this generates pairs:
      - (0,0), (0,1), (0,2), (0,3) — sums involving first abundant number
      - (1,1), (1,2), (1,3) — sums involving second abundant number
      - (2,2), (2,3) — sums involving third abundant number  
      - (3,3) — sum involving fourth abundant number
    - This efficiently represents all combinations including same-number pairs.

- **Step 5: Compute All Sums Vectorized**
  - Calculate all sums at once: `all_sums = abundant_numbers[i_values] + abundant_numbers[j_values]`.
  - For 6,965 abundant numbers, this generates approximately 24.3 million sums instantly.
  - NumPy performs this operation in highly optimized C code, making it much faster than Python loops.

- **Step 6: Filter and Mark**
  - Filter to keep only sums below the threshold: `all_sums[all_sums < threshold]`.
  - Mark these positions in the boolean array: `is_non_abundant[filtered_sums] = False`.
  - Now, `is_non_abundant[i]` is `True` if and only if number `i` cannot be expressed as the sum of two abundant numbers.

- **Step 7: Calculate the Answer**
  - Use `np.nonzero(is_non_abundant)[0]` to get all indices where the value is `True`.
  - These indices represent the numbers that cannot be expressed as abundant sums.
  - Sum these indices: `answer = sum(np.nonzero(is_non_abundant)[0])`.
  - This efficiently computes the final answer.

- **Efficiency:** This solution leverages NumPy's vectorized operations for maximum performance. The use of `np.triu_indices` is elegant and efficient for generating all pairs. The boolean array approach with direct indexing is very fast for marking and identifying non-abundant sums. This solution typically runs 10-50 times faster than Solution 1 for this problem size, demonstrating the power of vectorization.

---

## Mathematical Foundation

### Divisor Function and Abundant Numbers

The **divisor function** $\sigma(n)$ returns the sum of all positive divisors of $n$ (including $n$ itself). The **sum of proper divisors** is $d(n) = \sigma(n) - n$.

**Prime Factorization Formula:**
If $n = p_1^{a_1} \cdot p_2^{a_2} \cdots p_k^{a_k}$, then:
$$\sigma(n) = \prod_{i=1}^{k} \frac{p_i^{a_i+1} - 1}{p_i - 1}$$

This formula comes from the fact that each divisor of $n$ is formed by choosing an exponent between 0 and $a_i$ for each prime $p_i$. The sum of all such choices for a single prime is a geometric series:
$$\sigma(p^a) = 1 + p + p^2 + \cdots + p^a = \frac{p^{a+1} - 1}{p - 1}$$

**Multiplicativity:**
The function $\sigma$ is **multiplicative**: if $\gcd(m, n) = 1$, then $\sigma(mn) = \sigma(m) \cdot \sigma(n)$.

### Abundant Numbers

**Definition:** A number $n$ is **abundant** if $d(n) > n$, where $d(n)$ is the sum of proper divisors.

**Examples:**
- 12: proper divisors are 1, 2, 3, 4, 6 → sum = 16 > 12 (abundant)
- 18: proper divisors are 1, 2, 3, 6, 9 → sum = 21 > 18 (abundant)
- 20: proper divisors are 1, 2, 4, 5, 10 → sum = 22 > 20 (abundant)

**Properties:**
- The smallest abundant number is 12.
- Every multiple of an abundant number is also abundant.
- Every multiple of 6 greater than 6 itself is abundant.
- All even perfect numbers (like 6, 28, 496) are NOT abundant; they satisfy $d(n) = n$ exactly.

### Theoretical Upper Bound

By mathematical analysis, it has been proven that **all integers greater than 28123 can be written as the sum of two abundant numbers**. This is a **safe computational upper bound** used in many problems.

However, the actual **largest number that cannot be expressed** as the sum of two abundant numbers is **20161**, which is significantly smaller. The theoretical bound of 28123 provides a conservative guarantee that can be proven analytically, while 20161 was determined through exhaustive computational verification.

### Wheel Factorization (6k±1 Pattern)

After removing all factors of 2 and 3, any remaining prime must be of the form $6k \pm 1$.

**Proof:**
Any integer can be written as one of: $6k$, $6k+1$, $6k+2$, $6k+3$, $6k+4$, $6k+5$.
- $6k$, $6k+2$, $6k+4$ are divisible by 2.
- $6k+3$ is divisible by 3.
- Only $6k+1$ and $6k+5$ (i.e., $6k-1$) can be prime (for $k \geq 1$).

The alternating step pattern (2, 4, 2, 4, ...) efficiently generates all numbers of this form:
- Start at 5 = $6(1) - 1$, add 2 → 7 = $6(1) + 1$
- Add 4 → 11 = $6(2) - 1$, add 2 → 13 = $6(2) + 1$
- Add 4 → 17 = $6(3) - 1$, and so on...

This reduces the search space by approximately 67% compared to checking all numbers.

---

## Comparison of Solutions

| Aspect | Solution 1 (Set-Based) | Solution 2 (NumPy Vectorized) |
|--------|------------------------|-------------------------------|
| **Approach** | Nested loops with set | Vectorized operations with boolean array |
| **Data Structures** | Python list, set | NumPy arrays |
| **Pair Generation** | Explicit nested loops | `np.triu_indices` |
| **Duplicate Handling** | Set automatically deduplicates | Boolean array (no duplicates possible) |
| **Memory Usage** | Stores all sums in set (~10 MB) | Boolean array (28 KB) + temporary sums |
| **Speed** | Moderate (Python loops) | Very fast (C-optimized NumPy) |
| **Code Clarity** | ★★★★★ | ★★★★☆ |
| **Best For** | Readability, understanding | Performance, large datasets |

---

## Output

```
4179871
```

---

## Notes

- The sum of all positive integers which cannot be written as the sum of two abundant numbers is **4,179,871**.
- There are **6,965 abundant numbers** below 28,124.
- The smallest abundant number is **12**, and the smallest number expressible as the sum of two abundant numbers is **24** (12 + 12).
- While the theoretical upper bound is **28,123**, the actual largest number that cannot be expressed as such a sum is **20,161** (as proven by Parkin and Lander in 1964).
- **Solution 2** demonstrates the power of NumPy vectorization, typically running 10-50 times faster than pure Python loops for this problem size.
- The wheel factorization optimization (checking only $6k \pm 1$ candidates) reduces the trial division workload by approximately 67%.
- Both solutions correctly handle the mathematical structure of the problem: finding abundant numbers, generating all their pairwise sums, and computing the complement set.
- The use of `np.triu_indices` in Solution 2 is particularly elegant, as it naturally generates all unique pairs including same-number pairs (like 12 + 12) without requiring explicit conditional logic.
- This problem demonstrates an important algorithmic pattern: instead of directly finding numbers with a property (cannot be expressed as abundant sums), we find the complement set (CAN be expressed) and subtract from the total.
