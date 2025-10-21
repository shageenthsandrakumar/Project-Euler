# Problem 6: Sum Square Difference

**Problem source:** [Project Euler Problem 6](https://projecteuler.net/problem=6)

**Problem statement:**

The sum of the squares of the first ten natural numbers is:
$$1^2 + 2^2 + 3^2 + \cdots + 10^2 = 385$$

The square of the sum of the first ten natural numbers is:
$$(1 + 2 + 3 + \cdots + 10)^2 = 55^2 = 3025$$

Hence the difference between the sum of the squares and the square of the sum is:
$$3025 - 385 = 2640$$

Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.

---

## Solution 1: Direct Computation

### Approach

- Generate a list of numbers from $0$ to $n$.
- Compute the sum of all numbers, then square it to get the square of the sum.
- Compute the sum of squares by squaring each number and summing the results.
- Calculate the difference between these two values.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Generate Numbers**
  - Create a list: `nums = list(range(n+1))` containing $[0, 1, 2, 3, \dots, n]$.
  - Including $0$ doesn't affect the result since $0^2 = 0$ and adding $0$ to a sum has no effect.

- **Step 2: Square of the Sum**
  - Calculate the sum of all numbers: `sum(nums)`.
  - Square the result: `sum(nums)**2`.
  - This gives $(0 + 1 + 2 + \cdots + n)^2$.

- **Step 3: Sum of Squares**
  - Use a list comprehension to square each number: `[num**2 for num in nums]`.
  - Sum the squared values: `sum([num**2 for num in nums])`.
  - This gives $0^2 + 1^2 + 2^2 + \cdots + n^2$.

- **Step 4: Calculate Difference**
  - Subtract the sum of squares from the square of the sum: `sum(nums)**2 - sum([num**2 for num in nums])`.
  - Store the result in `answer`.

- **Efficiency:** This solution is straightforward and easy to understand. It iterates through all numbers twice: once to compute the sum and once to compute the sum of squares. For $n = 100$, this involves $200$ iterations total, which is negligible.

---

## Solution 2: Closed-Form Formula

### Approach

- Use mathematical formulas to directly compute the result without iteration.
- The **sum of the first $n$ natural numbers**: $\frac{n(n+1)}{2}$.
- The **sum of squares of the first $n$ natural numbers**: $\frac{n(n+1)(2n+1)}{6}$.
- Apply algebraic simplification to derive a closed-form expression for the difference.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Mathematical Foundation**
  - **Sum formula:** $S = 1 + 2 + 3 + \cdots + n = \frac{n(n+1)}{2}$
  - **Sum of squares formula:** $S_2 = 1^2 + 2^2 + 3^2 + \cdots + n^2 = \frac{n(n+1)(2n+1)}{6}$
  - **Square of the sum:** $S^2 = \left(\frac{n(n+1)}{2}\right)^2 = \frac{n^2(n+1)^2}{4}$

- **Step 2: Algebraic Simplification**
  - The difference we seek is: $S^2 - S_2$
  - Substituting the formulas:
    $$\frac{n^2(n+1)^2}{4} - \frac{n(n+1)(2n+1)}{6}$$
  - Factor out $n(n+1)$:
    $$n(n+1) \left[\frac{n(n+1)}{4} - \frac{2n+1}{6}\right]$$
  - Find common denominator (12):
    $$n(n+1) \left[\frac{3n(n+1) - 2(2n+1)}{12}\right]$$
  - Expand the numerator:
    $$3n(n+1) - 2(2n+1) = 3n^2 + 3n - 4n - 2 = 3n^2 - n - 2$$
  - Factor $3n^2 - n - 2$:
    $$3n^2 - n - 2 = (3n + 2)(n - 1)$$
  - Final simplified form:
    $$\frac{n(n+1)(3n+2)(n-1)}{12}$$

- **Step 3: Further Simplification**
  - Rearrange factors: $\frac{1}{12}*n(n-1)(n+1)(3n+2)$
  - Notice that $n(n-1)$ and $(n+1)$ can be regrouped:
    $$\frac{n}{2} \cdot (n-1)(n+1) \cdot (3n+2)$$
  - Recognize $(n-1)(n+1) = n^2 - 1$:
    $$\frac{n(n^2-1)(3n+2)}{2}$$
  - Alternative grouping using $a = \frac{n}{2}$:
    $$a(4a^2 - 1)\left(a + \frac{1}{3}\right)$$
    where $a = \frac{n}{2}$, $4a^2 - 1 = (2a-1)(2a+1) = (n-1)(n+1)$, and $a + \frac{1}{3} = \frac{3n+2}{6}$.

- **Step 4: Implementation Using Fractions**
  - To avoid floating-point precision issues, use Python's `Fraction` class.
  - Set $a = \frac{n}{2}$ as a `Fraction`.
  - Compute: $a \cdot (4a^2 - 1) \cdot \left(a + \frac{1}{3}\right)$
  - Extract the numerator (which is the final integer answer).

- **Efficiency:** This solution uses only a constant number of arithmetic operations regardless of $n$. No loops or list generation required. This is the most efficient approach.

---

## Output

```
25164150
```

---

## Notes

- The difference between the sum of the squares and the square of the sum for the first $100$ natural numbers is $25{,}164{,}150$.
- **Solution 2** is the optimal approach, using closed-form mathematical formulas to compute the result in constant time.
- The problem exploits the difference between two quadratic expressions, which simplifies to a quartic polynomial in $n$.
- The algebraic manipulation reveals the elegant structure: $\frac{n(n+1)(n-1)(3n+2)}{12}$ or equivalently $\frac{n(n^2-1)(3n+2)}{12}$.
- Using the `Fraction` class in Solution 2 ensures exact arithmetic without floating-point rounding errors.
- For large values of $n$, Solution 2's constant-time computation becomes increasingly advantageous over Solution 1's linear-time approach.
