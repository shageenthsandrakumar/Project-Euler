# Problem 7: 10001st Prime

**Problem source:** [Project Euler Problem 7](https://projecteuler.net/problem=7)

**Problem statement:**

By listing the first six prime numbers: $2, 3, 5, 7, 11$, and $13$, we can see that the $6$-th prime is $13$.

What is the $10\,001$st prime number?

---

## Solution 1: Trial Division

### Approach

- Use **trial division** to find prime numbers incrementally.
- Maintain a list of all primes found so far.
- For each candidate number, test divisibility against all previously found primes.
- If the candidate is not divisible by any existing prime, it is prime and added to the list.
- Continue until the 10,001st prime is found.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Initialization**
  - Initialize `primes = []` to store discovered primes.
  - Initialize `n = 1` as the candidate counter.
  - Set `threshold = 10001` as the target number of primes.

- **Step 2: Prime Discovery Loop**
  - The `while len(primes) < threshold:` loop continues until 10,001 primes are found.
  - Increment the candidate: `n += 1`.
  - Check if `n` is prime using trial division: `if not any(n % p == 0 for p in primes)`.
  - **Trial division logic:** A number is prime if it's not divisible by any smaller prime.
  - If `n` is prime, append it to the list: `primes.append(n)`.

- **Step 3: Result**
  - When the loop terminates, `n` holds the value of the 10,001st prime.
  - The algorithm prints `nth_prime = n`.

- **Efficiency:** This is the least efficient solution. For each candidate, it performs divisibility checks against **all** previously found primes without the $\sqrt{n}$ optimization. For the 10,001st prime, the algorithm checks each of 10,000+ primes for divisibility, requiring millions of divisibility tests. This approach is impractical for large $n$ and is included primarily for educational comparison.

---

## Solution 2: Sieve of Eratosthenes with Mathematical Upper Bound

### Approach

- Use a **mathematical upper bound** to determine how high to search for the $n$-th prime.
- Apply the **Rosser-Schoenfeld bound**: For $n \geq 6$, we have $p_n < n(\ln n + \ln \ln n)$.
- Run the **Sieve of Eratosthenes** up to this upper bound to generate all primes in that range.
- Use a **half-sieve optimization** (storing only odd numbers) to reduce memory usage by 50%.
- Extract the list of primes and return the $n$-th one.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Mathematical Foundation - The Prime Number Theorem**
  - The **Prime Number Theorem** (PNT) states that the number of primes less than or equal to $x$ is approximately:
  $$\pi(x) \sim \frac{x}{\ln x}$$
  - This means primes become less dense as numbers grow larger, with an average gap of approximately $\ln x$ between consecutive primes near $x$.
  - However, the PNT is an **asymptotic result** — it describes behavior as $x \to \infty$ but doesn't provide exact bounds for finite values.

- **Step 2: Inverting the PNT to Estimate $p_n$**
  - We need to **invert** $\pi(x)$ to find $p_n$ (the $n$-th prime) given $n$.
  - If $\pi(p_n) = n$ and $\pi(x) \approx \frac{x}{\ln x}$, then:
  $$n \approx \frac{p_n}{\ln p_n}$$
  - Solving for $p_n$: 
  $$p_n \approx n \ln p_n$$
  - Since $p_n \approx n \ln n$ (first-order approximation), we have:
  $$\ln p_n \approx \ln(n \ln n) = \ln n + \ln \ln n$$
  - Substituting back:
  $$p_n \approx n(\ln n + \ln \ln n)$$
  - **Important:** This is an **approximation**, not a rigorous upper bound. It can underestimate $p_n$ for small to medium values of $n$.

- **Step 3: The Rosser-Schoenfeld Upper Bound**
  - In 1962, J. Barkley Rosser and Lowell Schoenfeld **proved** rigorously for all $n \geq 6$:
  $$p_n < n(\ln n + \ln \ln n)$$
    
  - This is a **proven upper bound**, not just an approximation.
  - **Why it works:** The bound comes from the **explicit formula** connecting primes to the Riemann zeta function. By carefully bounding the error terms in the Prime Number Theorem (using zero-free regions of the zeta function), Rosser and Schoenfeld derived this explicit inequality.
  - **Verification for small $n$:**

$$
\begin{array}{|c|c|c|c|}
\hline
n & p_n & n(\ln n + \ln \ln n) & \text{Bound holds?} \\
\hline
6 & 13 & 14.22 & \checkmark \text{ Yes} \\
10 & 29 & 31.81 & \checkmark \text{ Yes} \\
100 & 541 & 565.51 & \checkmark \text{ Yes} \\
1{,}000 & 7{,}919 & 8{,}102 & \checkmark \text{ Yes} \\
\hline
\end{array}
$$

  - The bound consistently provides a safe margin (typically 5-10% above the actual value).

- **Step 4: Why $n \ln n$ Alone is NOT Sufficient**
  - The simpler approximation $p_n \approx n \ln n$ (without the $\ln \ln n$ term) **underestimates** $p_n$ for practical values of $n$.
  - Example for $n = 6$:
    - $n \ln n = 6 \times \ln(6) \approx 6 \times 1.79 \approx 10.75$
    - Actual $p_6 = 13$
    - The approximation is **too small**!
  - Example for $n = 100$:
    - $n \ln n = 100 \times \ln(100) \approx 100 \times 4.61 \approx 461$
    - Actual $p_{100} = 541$
    - The approximation is **too small** by 80!
  - If we used this as our sieve limit, we would **miss the answer entirely**.
  - The $n \ln \ln n$ term is **essential** for the bound to be a true upper bound.

- **Step 5: Computing the Upper Bound**
  - Example for $n = 6$:
    - $\ln(6) \approx 1.79$
    - $\ln(\ln(6)) \approx 0.58$
    - Upper bound: $6 \times (1.79 + 0.58) = 6 \times 2.37 \approx 14.22$
    - Actual $p_6 = 13$, so the bound works with a safety margin of about 9%.
  - Example for $n = 100$:
    - $\ln(100) \approx 4.61$
    - $\ln(\ln(100)) \approx 1.53$
    - Upper bound: $100 \times (4.61 + 1.53) = 100 \times 6.14 \approx 614$
    - Actual $p_{100} = 541$, so the bound works with a safety margin of about 13%.
  - The code uses: 
  $$\text{limit} = \lfloor n(\ln n + \ln \ln n) \rfloor + 1$$
  - The $+1$ provides a small safety margin for floating-point rounding.

- **Step 6: Half-Sieve Optimization**
  - The code implements a **half-sieve** that stores only odd numbers to save memory.
  - **Index mapping:** The array entry at index $i$ represents the number $2i + 1$.
    - Index $0$ represents $1$ (not prime)
    - Index $1$ represents $3$ (prime)
    - Index $2$ represents $5$ (prime)
    - Index $3$ represents $7$ (prime)
  - Array size: $\lfloor (\text{limit}+1)/2 \rfloor$ ensures all odd numbers up to the limit are represented.
  - Initialize all entries to `True` (assume odd numbers are prime), then set the first entry to `False` (since $1$ is not prime).

- **Step 7: Sieve Algorithm**
  - Loop over odd candidates $i$ from $3$ to $\lfloor \sqrt{\text{limit}} \rfloor$ (incrementing by 2):
    - **Why only to $\sqrt{\text{limit}}$:** Any composite number $n$ must have a prime factor $\leq \sqrt{n}$. All larger factors will have been eliminated by marking multiples of smaller primes.
  - For each prime $i$ (where the array entry at index $\lfloor i/2 \rfloor$ is `True`):
    - Mark all odd multiples of $i$ starting from $i^2$ as composite.
    - **Why start at $i^2$:** All smaller odd multiples ($3i, 5i, 7i, \ldots$) have already been marked by smaller primes.
  - Implementation details:
    - Starting index: $\lfloor i^2/2 \rfloor$ (the position of $i^2$ in the half-sieve)
    - Step size: $i$ (each step jumps $2i$ in actual number space, or $i$ in index space)

- **Step 8: Extracting Primes**
  - Find all indices where the array entry is `True`.
  - Convert indices to actual numbers: $2 \times \text{index} + 1$.
  - Prepend $2$ (the only even prime) to the list.
  - This produces an array of all primes up to the limit.

- **Step 9: Accessing the $n$-th Prime**
  - Use zero-based indexing: the element at position $n-1$ gives the $n$-th prime (since arrays are 0-indexed).
  - For $n = 6$, this returns $p_6 = 13$.
  - For $n = 10{,}001$, this returns $104{,}743$.

- **Efficiency:** The Sieve of Eratosthenes is highly efficient for generating all primes up to a given limit. The half-sieve optimization reduces memory usage by 50% and improves cache performance. This solution is **orders of magnitude faster** than trial division.

---

## Output

```
104743
```

---

## Notes

- The 10,001st prime number is $104{,}743$.
- **Solution 2** is the optimal approach, leveraging rigorous mathematical theory (the Rosser-Schoenfeld bound) combined with the efficient Sieve of Eratosthenes algorithm.
- The **Prime Number Theorem** provides the theoretical foundation for understanding prime distribution, while the **Rosser-Schoenfeld bound** gives a practical, provably correct upper limit for computation.
- The upper bound $n(\ln n + \ln \ln n)$ is **essential** — using just $n \ln n$ would fail to find the answer.
- The half-sieve optimization (storing only odd numbers) is a standard technique that reduces memory usage by 50% and improves performance through better cache utilization.
- For larger values of $n$, even tighter bounds exist (such as Dusart's refinements), but the Rosser-Schoenfeld bound is simple, elegant, and sufficient for all practical purposes.
- The problem demonstrates the power of combining **pure mathematics** (analytic number theory) with **efficient algorithms** (sieving) to solve computational problems.
