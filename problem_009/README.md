# Problem 9: Special Pythagorean Triplet

**Problem source:** [Project Euler Problem 9](https://projecteuler.net/problem=9)

**Problem statement:**

A Pythagorean triplet is a set of three natural numbers, $a < b < c$, for which:
$$a^2 + b^2 = c^2$$

For example, $3^2 + 4^2 = 9 + 16 = 25 = 5^2$.

There exists exactly one Pythagorean triplet for which $a + b + c = 1000$.

Find the product $abc$.

---

## Solution 1: Algebraic Direct Computation

### Approach

- Use the perimeter constraint $a + b + c = P$ to derive a formula for $b$ in terms of $a$.
- For each candidate value of $a$, calculate $b$ using: $b = \frac{P(P - 2a)}{2(P - a)}$.
- Check if $b$ is an integer (using modular arithmetic).
- If $b$ is an integer, compute $c = P - a - b$ and verify the Pythagorean relationship.
- This eliminates one loop entirely, reducing complexity from $O(n^2)$ to $O(n)$.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Mathematical Derivation**
  - Start with two equations:
    - Perimeter constraint: $a + b + c = P$
    - Pythagorean theorem: $a^2 + b^2 = c^2$
  - From the perimeter constraint: $c = P - a - b$
  - Substitute into the Pythagorean theorem:
    $$a^2 + b^2 = (P - a - b)^2$$
  - Expand the right side:
    $$a^2 + b^2 = P^2 - 2P(a + b) + (a + b)^2$$
    $$a^2 + b^2 = P^2 - 2Pa - 2Pb + a^2 + 2ab + b^2$$
  - Simplify by canceling $a^2$ and $b^2$ from both sides:
    $$0 = P^2 - 2Pa - 2Pb + 2ab$$
  - Rearrange to solve for $b$:
    - $$2Pb - 2ab = P^2 - 2Pa$$
    - $$b(2P - 2a) = P^2 - 2Pa$$
    - $$b = \frac{P^2 - 2Pa}{2P - 2a} = \frac{P(P - 2a)}{2(P - a)}$$

- **Step 2: Loop Constraints**
  - **Lower bound for $a$:** $a$ starts at $1$ (smallest natural number).
  - **Upper bound for $a$:** Since $a \leq b < c$ and $a + b + c = P$, we need to find the maximum possible value of $a$.
    - Since $c > b$ and $c$ is an integer, we have $c \geq b + 1$.
    - Since $b \geq a$ (allowing equality in the limiting case), and $c \geq b + 1$, we have $c \geq a + 1$.
    - The minimum perimeter occurs when $b = a$ and $c = a + 1$: $a + a + (a + 1) = 3a + 1 \leq P$.
    - Solving for $a$: $3a \leq P - 1$, so $a \leq \frac{P - 1}{3}$.
    - The upper bound is $(P - 1) // 3$ (using integer division).
  - Example for $P = 1000$: $a$ ranges from $1$ to $333$.

- **Step 3: Integer Check**
  - For $b$ to be a valid integer, the numerator $P(P - 2a)$ must be divisible by the denominator $2(P - a)$.
  - Use modular arithmetic: `if not numerator % denominator`.
  - This check is much faster than computing $b$ and then checking if it's an integer.

- **Step 4: Verification**
  - Once an integer $b$ is found, compute $c = P - a - b$.
  - Verify two conditions:
    - $a \leq b$ (ensures correct ordering)
    - $a^2 + b^2 = c^2$ (verifies Pythagorean relationship)

- **Step 5: Result**
  - For $P = 1000$, the unique solution is $(a, b, c) = (200, 375, 425)$.
  - The product is $abc = 200 \times 375 \times 425 = 31{,}875{,}000$.

- **Efficiency:** This solution is highly efficient. For $P = 1000$, it performs only 333 iterations with simple arithmetic operations. The algebraic approach eliminates the need for a nested loop.

---

## Solution 2: Euclid's Formula with Perimeter Constraint

### Approach

- Use **Euclid's formula** to generate all Pythagorean triples parametrically.
- Euclid's formula states that every Pythagorean triple can be generated using two coprime integers $m$ and $n$ (with $m > n$) and a scaling factor $k$:
  - $a = k(m^2 - n^2)$
  - $b = k(2mn)$
  - $c = k(m^2 + n^2)$
- The perimeter constraint becomes: $P = 2km(m + n)$.
- Iterate through all possible values of $k$ and $m$, then solve for $n$.
- Check if $n$ is a positive integer and if $m > n$.
- Verify the Pythagorean relationship and compute the product.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Euclid's Formula**
  - **Theorem:** Every Pythagorean triple $(a, b, c)$ can be expressed as:
    $$a = k(m^2 - n^2), \quad b = k(2mn), \quad c = k(m^2 + n^2)$$
    where $k$ is a positive integer (scaling factor), and $m, n$ are positive integers with $m > n$.
  - For primitive triples (where $\gcd(a, b, c) = 1$), we have $k = 1$, $\gcd(m, n) = 1$, and $m, n$ have opposite parity.

- **Step 2: Perimeter Simplification**
  - The perimeter is:
    $$P = a + b + c = k(m^2 - n^2) + k(2mn) + k(m^2 + n^2)$$
  - Simplify:
    $$P = k(m^2 - n^2 + 2mn + m^2 + n^2) = k(2m^2 + 2mn) = 2km(m + n)$$
  - Rearranging: $km(m + n) = \frac{P}{2}$

- **Step 3: Iteration Strategy**
  - For $P = 1000$, we have $\frac{P}{2} = 500$, so $km(m + n) = 500$.
  - **Outer loop (scaling factor $k$):** Iterate through all divisors of 500.
    - For each $k$, compute $E = \frac{500}{k} = m(m + n)$.
  - **Middle loop (generator $m$):** Iterate through all divisors of $E$.
    - For each $m$, compute $n = \frac{E}{m} - m$.
  - **Inner check:** Verify that $m > n > 0$.

- **Step 4: Generating the Triple**
  - Once valid $k, m, n$ are found, compute:
    - $a = k(m^2 - n^2)$
    - $b = k(2mn)$
    - $c = k(m^2 + n^2)$
  - Verify the perimeter: $a + b + c = P$.
  - Verify the Pythagorean relationship: $a^2 + b^2 = c^2$.

- **Step 5: Storing Unique Triples**
  - Use a set to store triples: `unique_triplets.add(tuple(sorted((a, b, c))))`.
  - Sorting ensures that $(200, 375, 425)$ and $(375, 200, 425)$ are treated as the same triple.

- **Step 6: Result**
  - For $P = 1000$, the algorithm finds the unique solution: $(200, 375, 425)$.
  - The parameters are $k = 25$, $m = 4$, $n = 1$.
    - $a = 25(4^2 - 1^2) = 25 \times 15 = 375$
    - $b = 25(2 \times 4 \times 1) = 25 \times 8 = 200$
    - $c = 25(4^2 + 1^2) = 25 \times 17 = 425$
  - Product: $200 \times 375 \times 425 = 31{,}875{,}000$.

- **Efficiency:** This solution is less efficient than Solution 1 due to the nested loops over divisors. However, it demonstrates the theoretical foundation of Pythagorean triples using Euclid's formula. The algorithm is still reasonably fast for moderate values of $P$.

---

## Why Perimeters Must Be Even

Before analyzing the solutions, it's important to understand a fundamental property of Pythagorean triples:

**Theorem:** The perimeter of any Pythagorean triple $(a, b, c)$ must be an even number.

**Proof:** We examine all possible parity combinations for the legs $a$ and $b$.

### Case 1: Both legs are ODD

If $a$ is odd and $b$ is odd, then:
- $a^2$ is odd (odd $\times$ odd = odd)
- $b^2$ is odd (odd $\times$ odd = odd)
- $a^2 + b^2 =$ odd + odd = **even**

So $c^2$ must be even, which means $c$ must be even (since only even numbers have even squares).

Perimeter: $P = a + b + c =$ odd + odd + even = even + even = **EVEN** ✓

### Case 2: Both legs are EVEN

If $a$ is even and $b$ is even, then:
- $a^2$ is even (even $\times$ even = even)
- $b^2$ is even (even $\times$ even = even)
- $a^2 + b^2 =$ even + even = **even**

So $c^2$ is even, which means $c$ is even.

Perimeter: $P =$ even + even + even = **EVEN** ✓

### Case 3: One leg is ODD, one leg is EVEN

If $a$ is odd and $b$ is even, then:
- $a^2$ is odd
- $b^2$ is even
- $a^2 + b^2 =$ odd + even = **odd**

So $c^2$ is odd, which means $c$ is odd.

Perimeter: $P =$ odd + even + odd = even + odd = **EVEN** ✓

**Conclusion:** All three possible parity combinations result in an even perimeter. Therefore, any Pythagorean triple must have an even perimeter.

This is why both solutions check `if P % 2 != 0` at the beginning to immediately reject odd perimeters.

---

## Comparison of Solutions

| Aspect | Solution 1<br>(Algebraic) | Solution 2<br>(Euclid's Formula) |
|--------|--------------------------|----------------------------------|
| **Approach** | Direct algebraic computation | Parametric generation |
| **Space Usage** | Minimal (few variables) | Uses set for uniqueness |
| **Loop Structure** | Single loop over $a$ | Nested loops over $k, m$ |
| **Mathematical Insight** | Perimeter constraint | Fundamental theorem |
| **Code Clarity** | ★★★★★ | ★★★ |
| **Speed** | Very fast | Moderate |
| **Best For** | Single perimeter problems | Understanding theory |

---

## Output

```
Found 1 Pythagorean Triplet(s) where a + b + c = 1000:
a, b, c = 200, 375, 425
Therefore product abc is 31875000
```

---

## Notes

- The unique Pythagorean triplet with perimeter 1000 is $(200, 375, 425)$.
- The product is $abc = 31{,}875{,}000$.
- **Solution 1** is the optimal approach for this specific problem, offering the best performance with clear, direct computation.
- **Solution 2** demonstrates the theoretical foundation of Pythagorean triples using Euclid's formula, which is valuable for understanding the mathematical structure.
- The proof that perimeters must be even is based purely on parity analysis and doesn't require advanced number theory.
- While the problem states there exists "exactly one" triplet for $P = 1000$, for other perimeters there may be zero, one, or multiple solutions.
- The algebraic approach in Solution 1 generalizes well to finding all triplets for any given perimeter.
- Both solutions correctly interpret "natural numbers" as positive integers ($a, b, c > 0$).
