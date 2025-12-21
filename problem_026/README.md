# Problem 26: Reciprocal Cycles

**Problem source:** [Project Euler Problem 26](https://projecteuler.net/problem=26)

**Problem statement:**

A unit fraction contains 1 in the numerator. The decimal representation of the unit fraction with denominators 2 to 10 are given:

- 1/2 = 0.5
- 1/3 = 0.333... (period 1)
- 1/4 = 0.25
- 1/5 = 0.2
- 1/6 = 0.1666... (period 1)
- 1/7 = 0.142857142857... (period 6)
- 1/8 = 0.125
- 1/9 = 0.111... (period 1)
- 1/10 = 0.1

Where 0.1666... means 0.1(6), i.e., 0.1 followed by an infinitely repeating 6. Similarly, 0.142857142857... means 0.(142857).

Find the value of $d < 1000$ for which $1/d$ contains the longest recurring cycle in its decimal fraction part.

---

## Solution 1: Long Division Simulation

### Approach

- Simulate the long division process for computing $1/d$ as a decimal.
- Track remainders at each step; when a remainder repeats, the decimal cycle begins to repeat.
- Remove factors of 2 and 5 from the denominator first, as these create non-repeating digits.
- For each candidate $d$, compute the cycle length by tracking remainders.
- Find the $d$ with the maximum cycle length.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Preprocessing - Removing Factors of 2 and 5**
  - The function `cycle_length(d)` first removes all factors of 2 and 5 from the denominator.
  - **Why?** Factors of 2 and 5 create non-repeating decimal places because 10 = 2 × 5.
  - Example: $1/6 = 1/(2 \times 3)$ → the factor of 2 creates the non-repeating "0.1", and only the 3 creates the repeating "6".
  - Implementation:
    ```python
    while not d%2:
        d //= 2
    while not d%5:
        d //= 5
    ```
  - After removing these factors, we're left with the "pure" repeating part.
  - **Edge case:** If $d = 1$ after removing all factors (like $d = 2, 4, 5, 8, 10$), return 0 (no repeating cycle).

- **Step 2: Long Division Simulation**
  - The decimal expansion of $1/d$ is computed through long division.
  - **The process:**
    - Start with remainder = 1 (from "1 ÷ d")
    - Multiply remainder by 10 (bring down a zero)
    - Divide by $d$ to get the next digit
    - The new remainder becomes the starting point for the next iteration
  - **Example with 1/7:**
    ```
    remainder = 1 → 1×10 = 10 → 10÷7 = 1 remainder 3
    remainder = 3 → 3×10 = 30 → 30÷7 = 4 remainder 2
    remainder = 2 → 2×10 = 20 → 20÷7 = 2 remainder 6
    remainder = 6 → 6×10 = 60 → 60÷7 = 8 remainder 4
    remainder = 4 → 4×10 = 40 → 40÷7 = 5 remainder 5
    remainder = 5 → 5×10 = 50 → 50÷7 = 7 remainder 1
    remainder = 1 → CYCLE! (back to start)
    ```
  - The cycle length is 6 for $1/7$.

- **Step 3: Tracking Remainders**
  - Initialize: `length = 1`, `remainder = 10 % d`
  - The loop continues: `while remainder != 1`
  - In each iteration:
    - Compute new remainder: `remainder = 10*remainder%d`
    - Increment cycle length: `length += 1`
  - **Why check for remainder = 1?**
    - When the remainder returns to 1, we're back to where we started
    - This means the decimal pattern will repeat from here
    - The number of steps taken is the cycle length

- **Step 4: Main Search Loop**
  - Loop through all integers from 1 to 999: `for d in range(threshold)`
  - For each $d$, compute its cycle length
  - Track the maximum: `if length > max_length`
  - Update both the maximum length and the corresponding $d$ value

- **Step 5: Mathematical Insight**
  - This approach directly implements the definition of a repeating decimal
  - A decimal repeats when we encounter the same remainder twice in long division
  - The cycle length is the number of steps between these repeated remainders

- **Efficiency:** This solution is straightforward but requires checking all 1000 values of $d$, and for each, potentially iterating up to $d-1$ times to find the cycle. For the largest primes near 1000, this means up to ~983 iterations per prime. Total operations: approximately 200,000-300,000 iterations.

---

## Solution 2: Multiplicative Order via Exponentiation

### Approach

- Recognize that the cycle length is the **multiplicative order** of 10 modulo $d$.
- The cycle length is the smallest positive integer $k$ such that $10^k \equiv 1 \pmod{d}$.
- Use Python's built-in `pow(10, power, d)` to compute $10^{\text{power}} \bmod d$ efficiently.
- For each candidate $d$, increment `power` until $10^{\text{power}} \equiv 1 \pmod{d}$.
- Remove factors of 2 and 5 as in Solution 1.
- Find the $d$ with the maximum cycle length.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Mathematical Foundation**
  - When computing $1/d$ as a decimal through long division, we compute successive powers of 10 modulo $d$:
    - First digit: depends on $10^1 \bmod d$
    - Second digit: depends on $10^2 \bmod d$
    - Third digit: depends on $10^3 \bmod d$
  - The decimal repeats when we encounter $10^k \equiv 1 \pmod{d}$ for some $k$
  - This $k$ is called the **multiplicative order** of 10 modulo $d$
  
- **Step 2: Connection to Repeating Decimals**
  - Consider $1/7 = 0.\overline{142857}$ with period 6
  - We can verify: $10^6 - 1 = 999999 = 7 \times 142857$
  - Therefore: $10^6 \equiv 1 \pmod{7}$
  - The general principle: if $1/d$ has period $k$, then $10^k \equiv 1 \pmod{d}$
  - **Proof sketch:**
    - If period is $k$, we can write: $\frac{1}{d} = \frac{r}{10^k - 1}$ for some integer $r$
    - This means: $10^k - 1 = r \cdot d$
    - Therefore: $10^k \equiv 1 \pmod{d}$

- **Step 3: Preprocessing**
  - Same as Solution 1: remove all factors of 2 and 5
  - These factors don't contribute to the repeating cycle
  
- **Step 4: Computing Multiplicative Order**
  - Start with `power = 1`
  - Loop: `while pow(10, power, d) != 1`
  - Increment: `power += 1`
  - Return `power` when condition is met
  - **Example with d = 7:**
    ```python
    pow(10, 1, 7) = 3  ≠ 1
    pow(10, 2, 7) = 2  ≠ 1
    pow(10, 3, 7) = 6  ≠ 1
    pow(10, 4, 7) = 4  ≠ 1
    pow(10, 5, 7) = 5  ≠ 1
    pow(10, 6, 7) = 1  ✓
    ```
  - Period is 6

- **Step 5: Main Search**
  - Same structure as Solution 1
  - Loop through all $d$ from 0 to 999
  - Track maximum cycle length and corresponding $d$

- **Step 6: Comparison to Solution 1**
  - **Solution 1:** Simulates long division by tracking remainders explicitly
  - **Solution 2:** Uses the mathematical formulation directly via exponentiation
  - Both compute the same quantity (multiplicative order)
  - Solution 2 is more declarative and mathematically explicit
  - Python's `pow(base, exp, mod)` is highly optimized using modular exponentiation

- **Efficiency:** Similar to Solution 1, this checks all 1000 values of $d$, computing up to $d-1$ exponentiations for each. The three-argument `pow()` uses fast modular exponentiation internally, but still computes each power independently. Total operations: approximately 200,000-300,000 modular exponentiations.

---

## Solution 3: Prime Sieve with Full Reptend Prime Testing

### Approach

**This is the recommended solution** as it combines deep mathematical insights with computational efficiency.

The solution exploits several key mathematical facts:
1. Only **primes** can achieve the maximum cycle length of $p-1$
2. Composite numbers always have cycle length strictly less than $d-1$
3. The cycle length must divide **Euler's totient function** $\phi(d)$
4. For primes, $\phi(p) = p-1$, so the maximum possible period is $p-1$
5. A prime $p$ achieves period $p-1$ if and only if 10 is a **primitive root** modulo $p$

**Algorithm:**
- Generate all primes up to 1000 using the **Sieve of Eratosthenes** (half-sieve optimization)
- Check primes in **descending order** (largest first)
- For each prime $p$, test if it's a **full reptend prime** by checking if 10 is a primitive root
- To test primitive root: verify $10^{(p-1)/q} \not\equiv 1 \pmod{p}$ for all prime divisors $q$ of $p-1$
- Return the first (largest) full reptend prime found

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Half-Sieve Prime Generation**
  - Create boolean array `is_prime` of size `(threshold+1)//2` to represent odd numbers only
  - **Index mapping:** `is_prime[i]` represents the number $2i + 1$
    - `is_prime[0]` → 1 (not prime, set False)
    - `is_prime[1]` → 3 (prime)
    - `is_prime[2]` → 5 (prime)
  - **Sieve process:**
    - For each odd number $i$ from 3 to $\sqrt{1000}$, step by 2
    - If $i$ is prime, mark all odd multiples starting from $i^2$ as composite
    - Implementation: `is_prime[i*i//2::i] = False`
    - **Why start at $i^2$?** All smaller multiples already marked by smaller primes
  - Extract primes: `primes = np.r_[2, 2*np.nonzero(is_prime)[0]+1]`
  - This efficiently generates all 168 primes below 1000

- **Step 2: Prime Factorization Function**
  - The function `is_full_reptend(p)` needs to factor $n = p-1$
  - Uses trial division with the pre-generated prime list
  - **Process:**
    - Set `n = p - 1`
    - Initialize empty list `prime_factors = []`
    - For each prime $f$ in the list (while $f^2 \leq n$):
      - If $f$ divides $n$, add $f$ to `prime_factors` list
      - Divide out all powers of $f$: `while not n%f: n //= f`
    - If $n > 1$ after all divisions, then $n$ itself is a prime factor
  - **Example:** For $p = 13$, we have $p-1 = 12 = 2^2 \times 3$
    - Prime factors: [2, 3]

- **Step 3: Full Reptend Prime Test**
  - A prime $p$ is a **full reptend prime** if the multiplicative order of 10 modulo $p$ equals $p-1$
  - **Theorem:** The order equals $p-1$ if and only if $10^{(p-1)/q} \not\equiv 1 \pmod{p}$ for all prime divisors $q$ of $p-1$
  - **Implementation:**
    ```python
    for q in prime_factors:
        exp = int((p - 1)/q)
        if pow(10, exp, p) == 1:
            return False
    return True
    ```
  - **Why this works:** (See Mathematical Foundation for full proof)
    - If the order is less than $p-1$, it must divide some proper divisor of $p-1$
    - All proper divisors of $p-1$ have the form $(p-1)/q$ for some prime $q$ dividing $p-1$
    - If $10^{(p-1)/q} \equiv 1 \pmod{p}$ for any prime $q$, then the order divides $(p-1)/q < p-1$
    - Therefore, checking prime divisors is sufficient

- **Step 4: Example - Testing p = 7**
  - $p - 1 = 6 = 2 \times 3$
  - Prime factors of 6: [2, 3]
  - Check $10^{6/2} = 10^3 \bmod 7$:
    - $10^3 = 1000 = 142 \times 7 + 6 \equiv 6 \pmod{7}$
    - $6 \not\equiv 1 \pmod{7}$ ✓
  - Check $10^{6/3} = 10^2 \bmod 7$:
    - $10^2 = 100 = 14 \times 7 + 2 \equiv 2 \pmod{7}$
    - $2 \not\equiv 1 \pmod{7}$ ✓
  - Both checks pass → 7 is a full reptend prime

- **Step 5: Example - Testing p = 11 (not full reptend)**
  - $p - 1 = 10 = 2 \times 5$
  - Prime factors of 10: [2, 5]
  - Check $10^{10/2} = 10^5 \bmod 11$:
    - $10^5 = 100000 \equiv 1 \pmod{11}$ ✗
  - First check fails → 11 is not a full reptend prime
  - Indeed, $1/11 = 0.\overline{09}$ has period 2, not 10

- **Step 6: Descending Search**
  - Loop through primes in reverse order: `for prime in reversed(primes)`
  - Start from 997 (largest prime < 1000) and work downward
  - Test each prime: `if is_full_reptend(int(prime))`
  - **Early termination:** Stop at the first full reptend prime found
  - This is guaranteed to be the largest, and therefore gives the longest period

- **Step 7: Why This is Optimal**
  - **Mathematical insight:** Only primes can achieve period $p-1$
  - **Composite limitation:** For composite $d$, $\phi(d) < d-1$, so period $< d-1$
  - **Search space reduction:** Only 168 primes to check (not 1000 numbers)
  - **Efficient testing:** For each prime $p$, check only $O(\log p)$ prime factors
    - Most numbers have few prime factors
    - For $p \approx 1000$: $p-1$ typically has 2-4 prime factors
    - Each check is a single modular exponentiation
  - **Example efficiency:** For $p = 983$:
    - $p - 1 = 982 = 2 \times 491$
    - Only 2 checks needed (not 982 iterations)

- **Efficiency:** This solution is dramatically more efficient than Solutions 1 and 2. Instead of checking 1000 numbers with up to 1000 iterations each, it checks 168 primes with typically 2-4 checks each. Total operations: approximately 500-700 modular exponentiations, compared to 200,000-300,000 in previous solutions. This is a **400× speedup**.

---

## Mathematical Foundation

### Repeating Decimals and Long Division

When computing $1/d$ as a decimal, we perform long division:
- Start with remainder 1
- Multiply by 10, divide by $d$, get quotient (next digit) and new remainder
- Continue until remainder repeats

**Key insight:** The remainders form a sequence that must eventually repeat because there are only $d-1$ possible non-zero remainders.

**Example with 1/7:**
```
1 → 10÷7 = 1 remainder 3
3 → 30÷7 = 4 remainder 2  
2 → 20÷7 = 2 remainder 6
6 → 60÷7 = 8 remainder 4
4 → 40÷7 = 5 remainder 5
5 → 50÷7 = 7 remainder 1 ← back to start!
```
Decimal: 0.142857142857... (period 6)

### Multiplicative Order

**Definition:** The **multiplicative order** of $a$ modulo $n$ ($\text{ord}_n(a)$ ) is the smallest positive integer $k$ such that $a^k \equiv 1 \pmod{n}$.

**For our problem:** The cycle length of $1/d$ equals $\text{ord}_d(10)$ (after removing factors of 2 and 5).

**Connection to remainders:**
- After $k$ steps of long division, the remainder is $10^k \bmod d$
- The cycle repeats when remainder returns to 1
- This occurs when $10^k \equiv 1 \pmod{d}$
- The smallest such $k$ is the multiplicative order

### Euler's Totient Function

**Definition:** Euler's totient function $\phi(n)$ counts the number of integers from 1 to $n$ that are coprime to $n$ (share no common factors except 1).

**Examples:**
- $\phi(6) = 2$ because only 1 and 5 are coprime to 6
- $\phi(7) = 6$ because 1, 2, 3, 4, 5, 6 are all coprime to 7
- $\phi(12) = 4$ because 1, 5, 7, 11 are coprime to 12

**For prime p:** $\phi(p) = p - 1$ (all numbers from 1 to $p-1$ are coprime to $p$)

**For prime powers:** $\phi(p^k) = p^{k-1}(p-1)$

**Multiplicative property:** If $\gcd(m,n) = 1$, then $\phi(mn) = \phi(m) \cdot \phi(n)$

### Euler's Theorem

**Theorem:** If $\gcd(a, n) = 1$, then $a^{\phi(n)} \equiv 1 \pmod{n}$.

**Proof:**

Let $r_1, r_2, \ldots, r_{\phi(n)}$ be all the positive integers less than $n$ that are coprime to $n$.

**Step 1:** Multiply each $r_i$ by $a$ to get: $ar_1, ar_2, \ldots, ar_{\phi(n)}$

**Step 2:** The set $\{ar_1 \bmod n, ar_2 \bmod n, \ldots, ar_{\phi(n)} \bmod n\}$ equals $\{r_1, r_2, \ldots, r_{\phi(n)}\}$ (same set, possibly reordered).

**Why?**
- **(a)** Each $ar_i$ is coprime to $n$: If $\gcd(a, n) = 1$ and $\gcd(r_i, n) = 1$, then $\gcd(ar_i, n) = 1$
- **(b)** All $ar_i$ are distinct modulo $n$: If $ar_i \equiv ar_j \pmod{n}$, then since $\gcd(a,n)=1$, we can cancel $a$ to get $r_i \equiv r_j \pmod{n}$, so $r_i = r_j$
- **(c)** We have $\phi(n)$ distinct values, all coprime to $n$ → must be exactly the same set

**Step 3:** Multiply all elements together:
$$\prod_{i=1}^{\phi(n)} (ar_i) = a^{\phi(n)} \prod_{i=1}^{\phi(n)} r_i$$

**Step 4:** Since both products equal the same set modulo $n$:
$$a^{\phi(n)} \prod_{i=1}^{\phi(n)} r_i \equiv \prod_{i=1}^{\phi(n)} r_i \pmod{n}$$

**Step 5:** Let $P = \prod_{i=1}^{\phi(n)} r_i$. Since each $r_i$ is coprime to $n$, their product $P$ is also coprime to $n$. We can divide both sides by $P$:
$$a^{\phi(n)} \equiv 1 \pmod{n}$$ 

**Example:** For $n = 7$, $a = 10$:
- $\phi(7) = 6$
- Coprime numbers: {1, 2, 3, 4, 5, 6}
- Product: $1 \times 2 \times 3 \times 4 \times 5 \times 6 = 720 \equiv 6 \pmod{7}$
- Multiply by 10: $\{10, 20, 30, 40, 50, 60\} \equiv \{3, 6, 2, 5, 1, 4\} \pmod{7}$
- Same set! Product: $3 \times 6 \times 2 \times 5 \times 1 \times 4 = 720 \equiv 6 \pmod{7}$
- Therefore: $10^6 \times 6 \equiv 6 \pmod{7}$
- Dividing by 6: $10^6 \equiv 1 \pmod{7}$ ✓

### Order Divides Euler's Totient

**Theorem:** If $\gcd(a, n) = 1$, then $\text{ord}_n(a)$ divides $\phi(n)$.

**Proof:**

Let $d = \text{ord}_n(a)$ (the multiplicative order). By definition, $a^d \equiv 1 \pmod{n}$ and $d$ is the smallest positive integer with this property.

From Euler's Theorem, we know $a^{\phi(n)} \equiv 1 \pmod{n}$.

Use the division algorithm: write $\phi(n) = qd + r$ where $0 \leq r < d$.

Then:
$$a^{\phi(n)} = a^{qd + r} = (a^d)^q \cdot a^r \equiv 1^q \cdot a^r \equiv a^r \pmod{n}$$

Since $a^{\phi(n)} \equiv 1 \pmod{n}$, we have $a^r \equiv 1 \pmod{n}$.

But $d$ is the **smallest** positive integer where $a^d \equiv 1 \pmod{n}$, and we have $0 \leq r < d$.

The only way $a^r \equiv 1 \pmod{n}$ with $0 \leq r < d$ is if $r = 0$.

Therefore, $\phi(n) = qd$, which means $d$ divides $\phi(n)$. ∎

**Consequence:** The period of $1/d$ must divide $\phi(d)$. For primes, $\phi(p) = p-1$, so the period divides $p-1$.

### Why Only Primes Can Achieve Maximum Period

**Theorem:** If the period of $1/d$ equals $d-1$, then $d$ must be prime.

**Proof:**

The period equals $\text{ord}_d(10)$.

From the previous theorem, $\text{ord}_d(10)$ must divide $\phi(d)$.

If the period equals $d-1$, then $(d-1)$ divides $\phi(d)$.

For any $n > 1$, we have $\phi(n) \leq n-1$, with equality only when $n$ is prime.

**Why?** 
- If $n$ is composite, it has at least one proper divisor $k$ with $1 < k < n$
- Then $\gcd(k, n) = k > 1$, so $k$ is not coprime to $n$
- Therefore, $\phi(n) < n-1$

If $(d-1)$ divides $\phi(d)$ and $(d-1) \leq \phi(d)$, then $\phi(d) = d-1$ (since $\phi(d) \leq d-1$ always).

This implies $d$ is prime. ∎

**Consequence:** To find the largest period, we only need to check primes!

### Full Reptend Primes and Primitive Roots

**Definition:** A prime $p$ is a **full reptend prime** if $1/p$ has period exactly $p-1$.

**Equivalent definition:** A prime $p$ is full reptend if $\text{ord}_p(10) = p-1$.

**Primitive root definition:** An integer $g$ is a **primitive root modulo $n$** if $\text{ord}_n(g) = \phi(n)$.

**For primes:** 10 is a primitive root modulo $p$ if and only if $\text{ord}_p(10) = p-1$.

**Therefore:** A prime $p$ is full reptend if and only if 10 is a primitive root modulo $p$.

**Examples of full reptend primes:** 7, 17, 19, 23, 29, 47, 59, 61, 97, 109, 113, ...

**Examples of non-full-reptend primes:** 3 (period 1), 11 (period 2), 13 (period 6), 31 (period 15)

### Testing for Primitive Roots via Prime Divisors

**Theorem:** Let $p$ be prime and $g$ be coprime to $p$. Then $\text{ord}_p(g) = p-1$ if and only if $g^{(p-1)/q} \not\equiv 1 \pmod{p}$ for all prime divisors $q$ of $p-1$.

**Proof:**

**Direction 1 (⇒):** If $\text{ord}_p(g) = p-1$, then $g^{(p-1)/q} \not\equiv 1 \pmod{p}$ for any prime $q$ dividing $p-1$.

- Proof by contradiction: Suppose $g^{(p-1)/q} \equiv 1 \pmod{p}$ for some prime $q$ dividing $p-1$.
- Then the order of $g$ divides $(p-1)/q$, which is less than $p-1$.
- This contradicts $\text{ord}_p(g) = p-1$. ∎

**Direction 2 (⇐):** If $g^{(p-1)/q} \not\equiv 1 \pmod{p}$ for all prime divisors $q$ of $p-1$, then $\text{ord}_p(g) = p-1$.

- Let $d = \text{ord}_p(g)$. We know $d$ divides $p-1$.
- Proof by contradiction: Suppose $d < p-1$.
- Then $(p-1)/d$ is an integer greater than 1.
- Let $q$ be a prime divisor of $(p-1)/d$.
- Then $(p-1)/d = q \cdot m$ for some integer $m \geq 1$.
- Therefore: $p-1 = d \cdot q \cdot m$, so $(p-1)/q = d \cdot m$.
- Since $d$ is the order: $g^d \equiv 1 \pmod{p}$.
- Therefore: $g^{(p-1)/q} = g^{d \cdot m} = (g^d)^m \equiv 1^m \equiv 1 \pmod{p}$.
- This contradicts our assumption that $g^{(p-1)/q} \not\equiv 1 \pmod{p}$ for all prime divisors $q$.
- Therefore, $d = p-1$. ∎

**Why We Only Check Prime Divisors:**

Suppose $p-1$ has the prime factorization $p-1 = q_1^{a_1} q_2^{a_2} \cdots q_k^{a_k}$.

The divisors of $p-1$ are products of these prime powers. If $g^{(p-1)/q_i} \not\equiv 1 \pmod{p}$ for each prime $q_i$, then the order cannot divide any $(p-1)/q_i$.

Since any proper divisor of $p-1$ has the form $d = (p-1)/m$ where $m > 1$ is some divisor of $p-1$, and $m$ must have at least one prime factor $q_i$, we have:
- $d = (p-1)/m < (p-1)/q_i$
- If $\text{ord}_p(g)$ divided $d$, then $g^d \equiv 1$, which implies $g^{(p-1)/q_i} \equiv 1$ (since $d$ divides $(p-1)/q_i$)
- But we checked that $g^{(p-1)/q_i} \not\equiv 1$, so the order cannot divide $d$

Therefore, the order cannot divide any proper divisor of $p-1$, so it must equal $p-1$.

**Practical Application:**

To test if a prime $p$ is full reptend:
1. Factor $p-1$ into prime factors: $p-1 = q_1 \times q_2 \times \cdots \times q_k$
2. For each prime $q_i$, check if $10^{(p-1)/q_i} \not\equiv 1 \pmod{p}$
3. If all checks pass, $p$ is full reptend
4. If any check fails, $p$ is not full reptend

**Efficiency gain:** Instead of checking all divisors of $p-1$ (potentially dozens), we only check the prime divisors (typically 2-4).

### Example: Testing Prime 17

**Setup:** $p = 17$, so $p-1 = 16 = 2^4$

**Prime factorization of 16:** Only one prime factor: 2

**Test:** Check if $10^{16/2} = 10^8 \not\equiv 1 \pmod{17}$

**Computation:**
- $10^2 = 100 = 5 \times 17 + 15 \equiv 15 \pmod{17}$
- $10^4 = (10^2)^2 \equiv 15^2 = 225 = 13 \times 17 + 4 \equiv 4 \pmod{17}$
- $10^8 = (10^4)^2 \equiv 4^2 = 16 \equiv -1 \pmod{17}$

Since $10^8 \equiv -1 \not\equiv 1 \pmod{17}$, the test passes!

**Conclusion:** 17 is a full reptend prime with period 16.

**Verification:** $1/17 = 0.\overline{0588235294117647}$ (period 16) ✓

### Example: Testing Prime 13 (Not Full Reptend)

**Setup:** $p = 13$, so $p-1 = 12 = 2^2 \times 3$

**Prime factorization of 12:** Prime factors are 2 and 3

**Test 1:** Check if $10^{12/2} = 10^6 \not\equiv 1 \pmod{13}$
- $10^2 = 100 = 7 \times 13 + 9 \equiv 9 \pmod{13}$
- $10^3 = 10 \times 10^2 \equiv 10 \times 9 = 90 = 6 \times 13 + 12 \equiv -1 \pmod{13}$
- $10^6 = (10^3)^2 \equiv (-1)^2 = 1 \pmod{13}$ ✗

**Test fails!** Since $10^{12/2} \equiv 1 \pmod{13}$, the order of 10 divides 6, which is less than 12.

**Conclusion:** 13 is not a full reptend prime.

**Verification:** $1/13 = 0.\overline{076923}$ (period 6, not 12) ✓

### The Role of Fermat's Little Theorem

**Fermat's Little Theorem** (special case of Euler's Theorem): If $p$ is prime and $\gcd(a, p) = 1$, then:
$a^{p-1} \equiv 1 \pmod{p}$

This is why we're guaranteed that $10^{p-1} \equiv 1 \pmod{p}$ for any prime $p > 5$.

The question is whether there's a smaller exponent $k < p-1$ where $10^k \equiv 1 \pmod{p}$. If not, then $p$ is full reptend.

---

## Comparison of Solutions

| Aspect | Solution 1<br>(Long Division) | Solution 2<br>(Exponentiation) | Solution 3<br>(Prime Sieve) |
|--------|------------------------------|--------------------------------|----------------------------|
| **Approach** | Simulate division process | Compute multiplicative order | Test full reptend primes |
| **Numbers Checked** | All 1000 values | All 1000 values | 168 primes only |
| **Iterations per Number** | Up to $d-1$ | Up to $d-1$ | 2-4 (prime factors) |
| **Mathematical Insight** | ★★★☆☆ | ★★★★☆ | ★★★★★ |
| **Dependencies** | None | None | NumPy |
| **Total Operations** | ~200,000-300,000 | ~200,000-300,000 | ~500-700 |
| **Speed (relative)** | 1× (baseline) | 1× (similar) | **400× faster** |
| **Code Clarity** | ★★★★★ | ★★★★★ | ★★★★☆ |
| **Best For** | Learning concepts | Understanding theory | Production code |

---

## Output

```
983
```

---

## Notes

- The value of $d < 1000$ with the longest recurring cycle is **983**.
- The decimal expansion $1/983$ has a period of **982** (maximum possible for $d = 983$).
- 983 is a **full reptend prime**, meaning 10 is a primitive root modulo 983.
- **Solution 3** is the optimal approach, achieving approximately **400× speedup** over brute force by exploiting deep number-theoretic properties.
- There are **168 primes** below 1000, but not all are full reptend primes. For example:
  - 7 is full reptend (period 6)
  - 11 is not (period 2, not 10)
  - 13 is not (period 6, not 12)
  - 17 is full reptend (period 16)
- The **prime factorization optimization** is crucial: instead of checking all divisors of $p-1$, we only check prime divisors, reducing checks from potentially dozens to typically 2-4.
- **Euler's Theorem** is the foundation that guarantees the period divides $\phi(d)$, making the mathematical optimization possible.
- The **descending search** in Solution 3 provides early termination: the first full reptend prime found is guaranteed to be the largest.
- For composite numbers, $\phi(d) < d-1$ always, so they can never achieve the maximum period. This is why we focus exclusively on primes.
- The problem beautifully connects **number theory** (Euler's theorem, primitive roots) and **practical computation** (sieve algorithms, modular exponentiation).
- Understanding why we can check only prime divisors requires the deep insight that any proper divisor of $p-1$ must be divisible by some prime factor of $p-1$, making prime checks sufficient to rule out all proper divisors.
- **Historical note:** The study of primitive roots and full reptend primes dates back to Gauss's *Disquisitiones Arithmeticae* (1801), one of the foundational texts of modern number theory.

