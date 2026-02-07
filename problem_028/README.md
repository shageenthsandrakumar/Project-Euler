# Problem 28: Number Spiral Diagonals

**Problem source:** [Project Euler Problem 28](https://projecteuler.net/problem=28)

**Problem statement:**

Starting with the number 1 and moving to the right in a clockwise direction, a 5×5 spiral is formed as follows:

```
21 22 23 24 25
20  7  8  9 10
19  6  1  2 11
18  5  4  3 12
17 16 15 14 13
```

It can be verified that the sum of the numbers on the diagonals is $21 + 7 + 1 + 3 + 13 + 9 + 5 + 17 + 25 = 101$.

What is the sum of the numbers on the diagonals in a 1001×1001 spiral formed in the same way?

---

## Solution 1: Recursive Ring Construction

### Approach

- Build the spiral **recursively** from the inside out, processing one ring at a time.
- Observe that each ring consists of four corners that follow a predictable pattern.
- For a ring with side length $s$, the top-right corner is $s^2$ and the other three corners are evenly spaced by $(s-1)$.
- Use **recursion** to compute the diagonal sum for the inner $(s-2) \times (s-2)$ spiral, then add the four corners of the current ring.
- The base case is the $1 \times 1$ spiral, which has only the center value of 1.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Base Case**
  - When `n == 1`, the spiral consists only of the center value 1.
  - Return 1 immediately.
  - This terminates the recursion.

- **Step 2: Input Validation**
  - The condition `elif n%2 and n>1:` checks if $n$ is both odd and greater than 1.
  - `n%2` returns 1 for odd numbers, 0 for even numbers.
  - Combined with `n>1`, this ensures we only process valid odd spirals larger than the base case.
  - The `else:` clause catches all invalid inputs (even numbers, zero, or negative numbers) and prints an error message.

- **Step 3: Recursive Structure**
  - For any valid spiral of size $n > 1$, it consists of:
    - An inner $(n-2) \times (n-2)$ spiral.
    - An outer ring with four corners.
  - The recursive call `diagonal_sum(n-2)` computes the sum for the inner spiral.
  - We then add the four corners of the current ring to this sum.

- **Step 4: Corner Calculation**
  - The **top-right corner** of an $n \times n$ spiral is always $n^2$.
  - Starting from this corner and moving counterclockwise, each subsequent corner is $(n-1)$ less than the previous:
    - **Top-right:** $n^2$
    - **Top-left:** $n^2 - (n-1)$
    - **Bottom-left:** $n^2 - 2(n-1)$
    - **Bottom-right:** $n^2 - 3(n-1)$
  - The code implements this by starting with `corner = n**2` and repeatedly subtracting `n-1`.

- **Step 5: Loop Through Corners**
  - The loop `for corners in range(4):` iterates exactly four times.
  - In each iteration:
    - Add the current `corner` value to `answer`.
    - Subtract `n-1` to get the next corner: `corner -= n-1`.
  - This efficiently computes all four corner values without explicitly calculating each formula.

- **Step 5: Input Validation**
  - The condition `elif n%2==1 and n>1:` checks if $n$ is both odd and greater than 1.
  - This is the valid recursive case: odd spirals larger than the base case.
  - The `else:` clause catches all invalid inputs (even numbers, zero, or negative numbers).
  - An error message is printed for invalid inputs.

- **Step 6: Example Walkthrough (n=5)**
  - `diagonal_sum(5)` calls:
    - `diagonal_sum(3)` which calls:
      - `diagonal_sum(1)` → returns `1`
    - `diagonal_sum(3)`:
      - Starts with `answer = 1` (from inner spiral)
      - Corners: $9, 7, 5, 3$
      - Sum: $1 + 9 + 7 + 5 + 3 = 25$
  - `diagonal_sum(5)`:
    - Starts with `answer = 25` (from inner spiral)
    - Corners: $25, 21, 17, 13$
    - Sum: $25 + 25 + 21 + 17 + 13 = 101$

- **Efficiency:** This solution has time complexity $O(n)$, as it makes approximately $n/2$ recursive calls. Each call performs constant-time operations (four additions and subtractions). The recursion depth is $n/2$, which is well within Python's default recursion limit for $n = 1001$.

---

## Solution 2: Closed-Form Formula

### Approach

- Derive a **closed-form mathematical formula** by recognizing a geometric pattern in the spiral structure.
- Observe that for each odd spiral of side length $s$ (from 3 to 1001), there's a cumulative contribution of $4(s-2)^2 + 6(s-1)$.
- Sum this expression across all odd values from 3 to 1001, then add the final outermost corner $1001^2$.
- Simplify this summation algebraically to derive the closed-form formula:
  $$\text{Sum} = \frac{4s^3 + 3s^2 + 8s - 9}{6}$$
- Use **integer division** to compute the result directly.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: The Geometric Pattern**
  - Through careful observation of the spiral, we discover that each ring contributes a specific amount to the total diagonal sum.
  - For a ring with side length $s$, the pattern involves the expression $4(s-2)^2 + 6(s-1)$.
  - This captures the cumulative structure of how diagonal values build up across rings.

- **Step 2: The Summation Formula**
  - The total diagonal sum can be expressed as:
    $$\sum_{\substack{s=3,5,7,\ldots}}^{n} [4(s-2)^2 + 6(s-1)] + n^2$$
  - Where $n = 1001$ for this problem.
  - The final $n^2$ accounts for the outermost corner.

- **Step 3: Expanding the Terms**
  - Expand $4(s-2)^2 + 6(s-1)$:
    $$4(s^2 - 4s + 4) + 6s - 6 = 4s^2 - 16s + 16 + 6s - 6 = 4s^2 - 10s + 10$$
  - So we need to sum $(4s^2 - 10s + 10)$ over all odd $s$ from 3 to $n$, then add $n^2$.

- **Step 4: Converting to Standard Summation**
  - Odd values $s = 3, 5, 7, \ldots, n$ can be parameterized as $s = 2k + 1$ where $k$ ranges from $1$ to $(n-1)/2$.
  - Substituting into $4s^2 - 10s + 10$:
    $$4(2k+1)^2 - 10(2k+1) + 10$$
    $$= 4(4k^2 + 4k + 1) - 20k - 10 + 10$$
    $$= 16k^2 + 16k + 4 - 20k = 16k^2 - 4k + 4$$

- **Step 5: Applying Summation Formulas**
  - Let $m = (n-1)/2$. The sum becomes:
    $$\sum_{k=1}^{m} (16k^2 - 4k + 4) + n^2$$
  - Using standard formulas:
    - $\sum_{k=1}^{m} k^2 = \frac{m(m+1)(2m+1)}{6}$
    - $\sum_{k=1}^{m} k = \frac{m(m+1)}{2}$
    - $\sum_{k=1}^{m} 1 = m$
  - We get:
    $$16 \cdot \frac{m(m+1)(2m+1)}{6} - 4 \cdot \frac{m(m+1)}{2} + 4m + n^2$$

- **Step 6: Simplifying to Closed Form**
  - Substituting $m = (n-1)/2$ and performing algebraic manipulation:
    $$\frac{2n^3}{3} - \frac{n^2}{2} + \frac{4n}{3} - \frac{3}{2} + n^2 = \frac{2n^3}{3} + \frac{n^2}{2} + \frac{4n}{3} - \frac{3}{2}$$
  - Multiplying by 6 to clear denominators:
    $$4n^3 + 3n^2 + 8n - 9$$
  - Therefore, the closed-form formula is:
    $$\frac{4n^3 + 3n^2 + 8n - 9}{6}$$

- **Step 7: Integer Division**
  - The implementation uses `//` (integer division) rather than `/` (float division).
  - This produces an exact integer result without floating-point representation.
  - The numerator $4n^3 + 3n^2 + 8n - 9$ is **always divisible by 6** for odd $n$ (see **Mathematical Foundation** for proof).
  - This guarantees no information loss when using integer division.

- **Efficiency:** This solution has time complexity $O(1)$, requiring only a handful of arithmetic operations regardless of the spiral size. This is the most efficient possible approach.

---

## Mathematical Foundation

### Why the Formula is Always Divisible by 6

For the closed-form formula to work correctly with integer division, we must prove that $4s^3 + 3s^2 + 8s - 9$ is always divisible by $6$ for odd values of $s$.

Since $6 = 2 \times 3$, we need to prove divisibility by both $2$ and $3$.

---

**Theorem:** For odd $s$, the expression $4s^3 + 3s^2 + 8s - 9$ is divisible by $6$.

**Proof:**

**Part 1: Divisibility by 2**

Since $s$ is odd, we can write $s = 2k + 1$ for some integer $k \geq 0$.

Substituting into the numerator:
$$4s^3 + 3s^2 + 8s - 9 = 4(2k+1)^3 + 3(2k+1)^2 + 8(2k+1) - 9$$

Expanding:
$$= 4(8k^3 + 12k^2 + 6k + 1) + 3(4k^2 + 4k + 1) + 16k + 8 - 9$$
$$= 32k^3 + 48k^2 + 24k + 4 + 12k^2 + 12k + 3 + 16k + 8 - 9$$
$$= 32k^3 + 60k^2 + 52k + 6$$

Factoring out 2:
$$= 2(16k^3 + 30k^2 + 26k + 3)$$

Therefore, the numerator is always even (divisible by 2). ✓

**Part 2: Divisibility by 3**

We need to show that $16k^3 + 30k^2 + 26k + 3 \equiv 0 \pmod{3}$.

Reducing coefficients modulo 3:
- $16 \equiv 1 \pmod{3}$
- $30 \equiv 0 \pmod{3}$
- $26 \equiv 2 \pmod{3}$
- $3 \equiv 0 \pmod{3}$

So:
$$16k^3 + 30k^2 + 26k + 3 \equiv k^3 + 2k \pmod{3}$$

Now we check all possible values of $k \pmod{3}$:

- If $k \equiv 0 \pmod{3}$: $k^3 + 2k \equiv 0 + 0 \equiv 0 \pmod{3}$ ✓
- If $k \equiv 1 \pmod{3}$: $k^3 + 2k \equiv 1 + 2 \equiv 0 \pmod{3}$ ✓
- If $k \equiv 2 \pmod{3}$: $k^3 + 2k \equiv 8 + 4 \equiv 2 + 1 \equiv 0 \pmod{3}$ ✓

Therefore, $16k^3 + 30k^2 + 26k + 3$ is always divisible by 3.

**Conclusion:**

Since $4s^3 + 3s^2 + 8s - 9 = 2(16k^3 + 30k^2 + 26k + 3)$ and we've shown that $16k^3 + 30k^2 + 26k + 3$ is divisible by 3, the entire numerator is divisible by $2 \times 3 = 6$. ∎

This proof guarantees that using integer division (`//6`) produces exact results with no information loss.

---

### The Recursive Structure of Spirals

The recursive solution exploits a fundamental property of number spirals: **each spiral is composed of a smaller spiral surrounded by a ring**.

For an $n \times n$ spiral:
- The inner $(n-2) \times (n-2)$ spiral contains all the same diagonal values it would have if constructed independently.
- The outer ring adds exactly four new diagonal values (the corners).
- This nested structure naturally lends itself to recursive computation.

This property means:
$$\text{DiagonalSum}(n) = \text{DiagonalSum}(n-2) + \text{CornerSum}(n)$$

where $\text{CornerSum}(n) = n^2 + [n^2-(n-1)] + [n^2-2(n-1)] + [n^2-3(n-1)]$.

The base case $\text{DiagonalSum}(1) = 1$ terminates the recursion.

---

## Comparison of Solutions

| Aspect | Solution 1 (Recursive) | Solution 2 (Closed-Form) |
|--------|------------------------|--------------------------|
| **Approach** | Recursive ring-by-ring construction | Direct mathematical formula |
| **Recursion** | Yes (depth ~500 for n=1001) | No |
| **Iterations** | ~500 recursive calls | 0 |
| **Operations per step** | 4 additions, 1 subtraction | 4 operations total |
| **Time Complexity** | O(n) | O(1) |
| **Space Complexity** | O(n) call stack | O(1) |
| **Code Clarity** | ★★★★★ | ★★★★☆ |
| **Mathematical Insight** | Nested spiral structure | Polynomial summation |
| **Best For** | Understanding the problem | Maximum efficiency |

---

## Output

```
669171001
```

---

## Notes

- The sum of the diagonals in a 1001×1001 spiral is **669,171,001**.
- **Solution 1** beautifully demonstrates the recursive structure of spirals, making the logic transparent and easy to verify.
- **Solution 2** showcases the power of mathematical analysis, reducing a seemingly computational problem to a single formula.
- The closed-form formula $\frac{4s^3 + 3s^2 + 8s - 9}{6}$ is guaranteed to produce exact integer results for all odd $s$, as proven by the divisibility theorem.
- The recursive solution is elegant and intuitive, building the answer by adding one ring at a time—mirroring how the spiral itself is constructed.
- For the 1001×1001 spiral, the recursive solution makes approximately 500 function calls, while the closed-form solution requires only constant time regardless of spiral size.
- The problem demonstrates that sometimes the most efficient solution isn't to compute the answer step-by-step, but to **derive a mathematical formula** that captures the entire computation.
- Both solutions correctly handle the constraint that spiral dimensions must be odd (to ensure a center point exists).
- The corner pattern $(n^2, n^2-(n-1), n^2-2(n-1), n^2-3(n-1))$ emerges naturally from the spiral's construction and is key to both solutions.
