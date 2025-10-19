# Problem 4: Largest Palindrome Product

**Problem source:** [Project Euler Problem 4](https://projecteuler.net/problem=4)

**Problem statement:**

A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is $9009 = 91 * 99$.

Find the **largest palindrome** made from the product of two 3-digit numbers.

---

## Solution 1: Brute-Force Iteration

### Approach

- Iterate through all pairs of 3-digit numbers $(i, j)$ where $100 \leq i \leq j < 1000$.
- Calculate the product $i \times j$ for each pair.
- Check if the product is a palindrome.
- Track the largest palindromic product found.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Palindrome Check Function**
  - Convert the number to a string.
  - Compare characters from both ends moving toward the center.
  - If any pair doesn't match, the number is not a palindrome.

- **Step 2: Nested Loop Structure**
  - Outer loop: `for i in range(100, 1000)` iterates through all 3-digit numbers.
  - Inner loop: `for j in range(i, 1000)` ensures we only check each pair once (avoiding duplicate pairs like $(i,j)$ and $(j,i)$).
  - This structure checks all $\frac{900 * 901}{2} = 405{,}450$ unique pairs.

- **Step 3: Product Evaluation**
  - For each pair, calculate `product = i * j`.
  - Check if the product is a palindrome using `ispalindrome(product)`.
  - If it is a palindrome and larger than the current maximum, update `largest = (product, i, j)`.

- **Step 4: Result**
  - After all iterations, `largest` contains the maximum palindromic product and its factors.

- **Efficiency:** This is the least efficient solution, checking all possible pairs without any optimization. It performs approximately 405,450 multiplications and palindrome checks.

---

## Solution 2: Ascending Search with Divisibility Optimization

### Approach

- Exploit the mathematical property that a 6-digit palindrome must be divisible by 11.
- Ensure at least one factor in each pair is divisible by 11 by stepping through multiples of 11.
- Search in ascending order from 100 to 999.
- Include a fallback loop to handle potential 5-digit palindromes.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Mathematical Foundation**
  - A 6-digit palindrome has the form $\overline{abccba} = 100001a + 10010b + 1100c$.
  - Factor: $100001a + 10010b + 1100c = 11(9091a + 910b + 100c)$.
  - Therefore, every 6-digit palindrome is divisible by 11.
  - For a product $i * j$ to be divisible by 11, at least one factor must be divisible by 11.

- **Step 2: Optimized Inner Loop**
  - Calculate `j_start`: the smallest value of $j \geq 100$ that ensures a 6-digit product.
    - Formula: `j_start = max((100000 + i - 1) // i, 100)`
    - **Breakdown:** This is a clever way of computing $\lceil \frac{100000}{i} \rceil$ (ceiling division).
      - We need $i * j \geq 100000$ (the smallest 6-digit number).
      - Solving for $j$: $j \geq \frac{100000}{i}$.
      - The expression `(100000 + i - 1) // i` implements ceiling division using only integer arithmetic.
      - Adding $(i-1)$ before integer division ensures we round up: $\lceil \frac{a}{b} \rceil = \lfloor \frac{a + b - 1}{b} \rfloor$.
      - The `max(..., 100)` ensures $j$ remains a valid 3-digit number.
  - Adjust to the nearest multiple of 11: `j_start_11 = ((j_start + 10) // 11) * 11`
  - Step through multiples of 11: `for j in range(j_start_11, 1000, 11)`

- **Step 3: Fallback for 5-Digit Products**
  - If no palindrome is found in the 6-digit search (checked via `if not sum(largest)`), execute a comprehensive search for 5-digit palindromes.
  - **Important:** The fallback loop does **not** use the divisibility-by-11 optimization.
    - **Why?** Only 6-digit palindromes are guaranteed to be divisible by 11.
    - 5-digit palindromes have the form $\overline{abcba} = 10001a + 1010b + 100c$.
    - This expression is **not** divisible by 11 in general.
    - Therefore, we must check **all** possible $j$ values: `for j in range(100, j_end + 1)`.
  - This fallback ensures correctness even in edge cases.

- **Step 4: Result**
  - The largest palindrome found is $906{,}609 = 993 \times 913$.

- **Efficiency:** Reduces the number of checks by approximately 67% (testing only multiples of 11). However, the ascending order limits the effectiveness of early termination.

---

## Solution 3: Descending Search with Early Exit

### Approach

- Search in **descending order** from 999 to 100 to find the largest product first.
- Implement **dual early exit conditions**:
  - **Outer loop exit:** Stop when the maximum possible product for remaining factors is too small.
  - **Inner loop exit:** Skip remaining $j$ values when products become too small for the current $i$.
- Maintain the divisibility-by-11 optimization.
- Include a fallback loop for 5-digit palindromes (though rarely needed).

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Descending Outer Loop**
  - `for i in range(999, 99, -1)` iterates from largest to smallest 3-digit numbers.
  - This ensures larger products are tested first.

- **Step 2: Outer Loop Early Exit**
  - **Condition:** `if i * 990 < largest[0]: break`
  - **Rationale:** $990$ is the largest 3-digit multiple of 11. The product $i * 990$ represents the maximum possible palindromic product for the current $i$ (given the divisibility constraint).
  - Once this maximum is smaller than the current best palindrome, no future iterations can yield a larger result.
  - This optimization dramatically reduces the search space.

- **Step 3: Inner Loop Optimization**
  - Start $j$ at the largest multiple of 11 that is $\leq i$: `j_start_11 = i - (i % 11)` (capped at 990).
  - Calculate the minimum $j$ needed for a 6-digit product using ceiling division:
    - `j_small = max((100000 + i - 1) // i, 100)` computes $\lceil \frac{100000}{i} \rceil$.
    - This ensures $i * j \geq 100000$ (the smallest 6-digit number).
    - `j_small_11 = ((j_small + 10) // 11) * 11` rounds up to the nearest multiple of 11.
  - Iterate: `for j in range(990, j_small_11 - 1, -11)`

- **Step 4: Inner Loop Early Exit**
  - **Condition:** `if product <= largest[0]: break` (in the `else` clause)
  - Since $j$ is decreasing, once a product is too small, all subsequent products for this $i$ will also be too small.

- **Step 5: Fallback Loop**
  - Checks for 5-digit palindromes if the main loop fails to find any result.
  - **Important:** Cannot use the divisibility-by-11 optimization here.
    - 5-digit palindromes ($\overline{abcba} = 10001a + 1010b + 100c$) are **not** guaranteed to be divisible by 11.
    - Must check all $j$ values: `for j in range(j_end, 99, -1)`.
  - Includes its own outer loop early exit: `if i * j_end < largest[0]: break`

- **Step 6: Result**
  - The algorithm finds $906{,}609 = 993 * 913$ efficiently.
  - The outer loop breaks at approximately $i = 907$ due to the early exit condition.

- **Efficiency:** This is the most efficient solution. The combination of descending search, divisibility optimization, and dual early exits minimizes the number of products checked. In practice, it evaluates fewer than 10,000 products compared to the 405,450 in Solution 1.

---

## Output

```
The largest palindrome product of two 3-digit numbers is: 906609
It is the product of 993 × 913
```

---

## Notes

- The largest palindromic product of two 3-digit numbers is $906{,}609 = 993 * 913$.
- The divisibility-by-11 property is crucial for optimization: all 6-digit palindromes are divisible by 11.
- **Solution 3** is the optimal approach, leveraging descending search order and early exit strategies to achieve maximum efficiency.
- The early exit condition $i * 990 < \text{largest}$ (or $i * 999$ for a looser bound) is mathematically sound and dramatically reduces computational overhead.
- While Solution 2 includes structural separation between 6-digit and 5-digit searches, Solution 3's descending approach makes the fallback loop rarely necessary in practice.
