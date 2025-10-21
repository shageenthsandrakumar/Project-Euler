# Problem 5: Smallest Multiple

**Problem source:** [Project Euler Problem 5](https://projecteuler.net/problem=5)

**Problem statement:**

$2520$ is the smallest number that can be divided by each of the numbers from $1$ to $10$ without any remainder.

What is the **smallest positive number** that is evenly divisible by all of the numbers from $1$ to $20$?

---

## Solution 1: Trial Division Prime Generation

### Approach

- Generate all prime numbers up to the threshold using **trial division**.
- For each prime $p$, calculate the maximum exponent $k$ such that $p^k \leq \text{threshold}$.
- Compute the product of all primes raised to their maximum exponents: $\text{LCM} = \prod p^k$.
- This product is the least common multiple (LCM) of all numbers from $1$ to the threshold.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Prime Generation**
  - Initialize `primes = [2]` to start with the first prime.
  - For each candidate number $n$ from $3$ to $\text{nums}$:
    - Check if $n$ is divisible by any existing prime using `not any(n % p == 0 for p in primes)`.
    - If $n$ is not divisible by any prime, it is prime and is appended to the list.
  - Convert the list to a NumPy array for efficient vectorized operations.

- **Step 2: Computing Maximum Exponents**
  - For each prime $p$, we need the largest integer $k$ such that $p^k \leq \text{nums}$.
  - Using logarithms: $k = \lfloor \log_p(\text{nums}) \rfloor = \lfloor \frac{\ln(\text{nums})}{\ln(p)} \rfloor$.
  - The code computes this efficiently using NumPy: `exponents = np.log(nums) // np.log(primes)`.
  - This produces a vectorized array of exponents, one for each prime.

- **Step 3: Computing the LCM**
  - Raise each prime to its corresponding exponent: `primes**exponents`.
  - Compute the product of all these values: `np.prod(primes**exponents)`.
  - Convert to an integer: `int(np.prod(primes**exponents))`.

- **Step 4: Mathematical Foundation**
  - **Why this works:** Every positive integer can be uniquely factorized into primes (Fundamental Theorem of Arithmetic).
  - For a number to be divisible by all integers from $1$ to $\text{nums}$, it must contain all prime factors with sufficient multiplicity.
  - The LCM is obtained by taking each prime to its maximum power that appears in any number $\leq \text{nums}$.

- **Example for nums = 10:**
  - Primes: $[2, 3, 5, 7]$
  - Exponents: $[3, 2, 1, 1]$ because $2^3 = 8 \leq 10$, $3^2 = 9 \leq 10$, $5^1 = 5 \leq 10$, $7^1 = 7 \leq 10$
  - LCM: $2^3 \times 3^2 \times 5 \times 7 = 8 \times 9 \times 5 \times 7 = 2520$

- **Efficiency:** Trial division is straightforward but inefficient for large thresholds. For $\text{nums} = 20$, it performs approximately $20$ iterations with divisibility checks against a growing list of primes. Time complexity: $O(n^2 / \log n)$.

---

## Solution 2: Half-Sieve (Odd-Only Optimization)

### Approach

- Use an **optimized Sieve of Eratosthenes** that stores only odd numbers to reduce memory usage by approximately 50%.
- The **Sieve of Eratosthenes** is an ancient algorithm for finding all primes up to a limit by iteratively marking multiples of each prime as composite.
- The basic sieve marks multiples of $2$, then $3$, then $5$, and so on, leaving only primes unmarked.
- The **half-sieve optimization** recognizes that all primes (except $2$) are odd, so we can skip all even numbers entirely.
- Map array indices to actual numbers using the relation: index $i$ represents number $2i + 1$.
- Mark composite odd numbers by eliminating multiples of each prime.
- Extract primes efficiently and compute maximum exponents using logarithms.
- Calculate the LCM as the product of primes raised to their maximum powers.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Half-Sieve Initialization**
  - Create a boolean array `is_prime` of size `nums//2` to represent only odd numbers.
  - Index mapping: `is_prime[i]` corresponds to the number $2i + 1$.
    - `is_prime[0]` → $1$ (not prime, set to `False`)
    - `is_prime[1]` → $3$ (prime)
    - `is_prime[2]` → $5$ (prime)
    - `is_prime[3]` → $7$ (prime)
  - Initialize all entries to `True` (assume all odd numbers are prime initially).
  - Set `is_prime[0] = False` because $1$ is not prime.

- **Step 2: Sieve Process**
  - Loop over odd candidates $i$ from $3$ to $\sqrt{\text{nums}}$ (step by 2).
  - **Why only up to $\sqrt{\text{nums}}$:**
    - If a composite number $n$ has a factor $f > \sqrt{n}$, it must have a corresponding factor $d < \sqrt{n}$ (since $n = f \times d$).
    - Therefore, all composite numbers will have been marked by their smaller factors before we reach $\sqrt{n}$.
    - Any unmarked number beyond this point must be prime.
  - For each candidate $i$, compute its index in the half-sieve: `i//2`.
  - If `is_prime[i//2]` is `True`, then $i$ is prime:
    - Mark all odd multiples of $i$ starting from $i^2$ as composite.
    - **Why start at $i^2$:**
      - All smaller multiples of $i$ (such as $3i, 5i, 7i, \dots$) have already been marked by smaller primes.
      - For example, when processing $i = 5$: $5 \times 3 = 15$ was already marked when we processed $3$.
      - The first unmarked multiple is always $i^2$ (the square of the current prime).
    - Starting point (in array indices): `i*i//2`
      - This represents the first odd multiple $i^2$ that hasn't been marked by smaller primes.
    - Step size: `i`
      - Represents the gap between consecutive odd multiples of $i$ in the compressed index space.
    - Implementation: `is_prime[i*i//2::i] = False`

- **Step 3: Extracting Primes**
  - Use `np.nonzero(is_prime)[0]` to get indices of all `True` entries (odd primes).
  - Convert indices back to actual numbers: $2 \times \text{index} + 1$.
  - Prepend $2$ (the only even prime) using `np.r_[2, 2*np.nonzero(is_prime)[0]+1]`.

- **Step 4: Computing Exponents and LCM**
  - Use the same logarithmic formula as Solution 1:
    - `exponents = np.log(nums) // np.log(primes)`
  - Compute the LCM: `int(np.prod(primes**exponents))`

- **Step 5: Why `i*i//2::i` Works**
  - **Starting point (`i*i//2`):**
    - We want to start marking from $i^2$ (the first composite that wasn't already marked).
    - The index for $i^2$ in the half-sieve: $(i^2 - 1) / 2 = i^2 // 2$ (integer division).
  - **Step size (`i`):**
    - Consecutive odd multiples of $i$ differ by $2i$ in actual number space.
    - In index space (where each index represents a jump of 2), the step is $2i / 2 = i$.

- **Efficiency:** The half-sieve is approximately **2× faster** than the full sieve and uses **50% less memory**. This is the most efficient method for generating primes up to moderate limits.

---

## Output

```
232792560
```

---

## Notes

- The smallest number divisible by all integers from $1$ to $20$ is $232{,}792{,}560$.
- Prime factorization: $232{,}792{,}560 = 2^4 \times 3^2 \times 5 \times 7 \times 11 \times 13 \times 17 \times 19$.
- **Solution 2** is the optimal approach, leveraging the half-sieve optimization for efficient prime generation.
- The problem is equivalent to finding $\text{LCM}(1, 2, 3, \dots, 20)$.
- Simply multiplying all numbers from $1$ to $20$ would produce a much larger number with redundant prime factors. The LCM approach ensures each prime appears with the minimal necessary exponent.
- The logarithmic method for computing exponents avoids iterative division and is highly efficient for vectorized operations.
