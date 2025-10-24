# Problem 7: 10001st Prime

**Problem source:** [Project Euler Problem 7](https://projecteuler.net/problem=7)

**Problem statement:**

By listing the first six prime numbers: $2, 3, 5, 7, 11$, and $13$, we can see that the $6$-th prime is $13$.

What is the $10001$-st prime number?

---

## Solution 1: Trial Division using Modulo

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
- Apply the **Rosser-Schoenfeld bound**: For $n \geq 6$, we have $p_n < n(\ln(n) + \ln (\ln(n)))$.
- Run the **Sieve of Eratosthenes** up to this upper bound to generate all primes in that range.
- Use a **half-sieve optimization** (storing only odd numbers) to reduce memory usage by 50%.
- Extract the list of primes and return the $n$-th one.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: The Rosser-Schoenfeld Upper Bound**
  - In 1962, J. Barkley Rosser and Lowell Schoenfeld **proved** rigorously for all $n \geq 6$:
  $$p_n < n(\ln(n) + \ln(\ln(n)))$$
    
  - This is a **proven upper bound**, not just an approximation.
  - **Why it works:** The bound comes from the **explicit formula** connecting primes to the Riemann zeta function. By carefully bounding the error terms in the Prime Number Theorem (using zero-free regions of the zeta function), Rosser and Schoenfeld derived this explicit inequality.
  - **Verification for small $n$:**

$$
\begin{array}{|c|c|c|c|}
\hline
n & p_n & n(\ln(n) + \ln(\ln(n))) & \text{Bound holds?} \\
\hline
6 & 13 & 14.22 & \checkmark \text{ Yes} \\
10 & 29 & 31.81 & \checkmark \text{ Yes} \\
100 & 541 & 565.51 & \checkmark \text{ Yes} \\
1{,}000 & 7{,}919 & 8{,}102 & \checkmark \text{ Yes} \\
\hline
\end{array}
$$

  - The bound consistently provides a safe margin (typically 5-10% above the actual value).


- **Step 2: Computing the Upper Bound**
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
  $$\text{limit} = \lfloor n(\ln(n) + \ln(\ln(n))) \rfloor + 1$$
  - The $+1$ provides a small safety margin for floating-point rounding.

- **Step 3: Half-Sieve Initialization**
  - Create a boolean array `is_prime` of size `(limit+1)//2` to represent only odd numbers up to and including `limit`.
  - Index mapping: `is_prime[i]` corresponds to the number $2i + 1$.
    - `is_prime[0]` → $1$ (not prime, set to `False`)
    - `is_prime[1]` → $3$ (prime)
    - `is_prime[2]` → $5$ (prime)
    - `is_prime[3]` → $7$ (prime)
  - The array size ensures all odd numbers up to `limit` are included in the sieve.
  - Initialize all entries to `True` (assume all odd numbers are prime initially).
  - Set `is_prime[0] = False` because $1$ is not prime.

- **Step 4: Sieve Process**
  - Loop over odd candidates $i$ from $3$ to $\sqrt{\text{limit}}$ (step by 2).
  - **Why only up to $\sqrt{\text{limit}}$:**
    - If a composite number $n$ has a factor $f > \sqrt{n}$, it must have a corresponding factor $d < \sqrt{n}$ (since $n = f \times d$).
    - Therefore, all composite numbers will have been marked by their smaller factors before we reach $\sqrt{n}$.
    - Any unmarked number beyond this point must be prime.
  - For each candidate $i$, compute its index in the half-sieve: `i//2`.
  - If `is_prime[i//2]` is `True`, then $i$ is prime:
    - Mark all odd multiples of $i$ starting from $i^2$ as composite.
    - **Why start at $i^2$:**
      - All smaller multiples of $i$ (such as $3i, 5i, 7i, \ldots$) have already been marked by smaller primes.
      - For example, when processing $i = 5$: $5 \times 3 = 15$ was already marked when we processed $3$.
      - The first unmarked multiple is always $i^2$ (the square of the current prime).
    - Implementation: `is_prime[i*i//2::i] = False`
    - **Understanding the slice `i*i//2::i`:**
      - **Starting point (`i*i//2`):** The index for $i^2$ in the half-sieve is $(i^2 - 1) / 2 = int(i^2/2)$ (integer division).
      - **Step size (`i`):** Consecutive odd multiples of $i$ differ by $2i$ in actual number space. In index space (where each index represents a jump of 2), the step is $2i / 2 = i$.

- **Step 5: Extracting Primes**
  - Use `np.nonzero(is_prime)[0]` to get indices of all `True` entries (odd primes).
  - Convert indices back to actual numbers: $2 \times \text{index} + 1$.
  - Prepend $2$ (the only even prime) using `np.r_[2, 2*np.nonzero(is_prime)[0]+1]`.
  - Because the sieve size is `(limit+1)//2`, all primes up to and including `limit` are automatically captured.

- **Step 6: Accessing the $n$-th Prime**
  - Use zero-based indexing: the element at position $n-1$ gives the $n$-th prime (since arrays are 0-indexed).
  - For $n = 6$, this returns $p_6 = 13$.
  - For $n = 10{,}001$, this returns $104{,}743$.

- **Efficiency:** The Sieve of Eratosthenes is highly efficient for generating all primes up to a given limit. The half-sieve optimization reduces memory usage by 50% and improves cache performance. This solution is **orders of magnitude faster** than trial division.

---

## Solution 3: Incremental Sieve of Eratosthenes using Generators

### Approach

- Implement an **incremental sieve** that generates primes on demand without requiring an upper bound.
- Use a Python **generator** with lazy evaluation to produce primes one at a time.
- Maintain a dictionary `D` that tracks the **next composite** to be marked for each prime.
- Only store information about composites that are currently relevant.
- This elegant approach combines memory efficiency with the power of the sieve algorithm.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Generator Initialization**
  - Define `prime_generator()` as a Python generator function that yields primes indefinitely.
  - Special case: `yield 2` immediately, since 2 is the only even prime.
  - Initialize empty dictionary `D = {}` to track composite numbers.
  - Use `itertools.count(3, 2)` to generate candidate numbers: $3, 5, 7, 9, 11, \ldots$ (all odd numbers starting from 3).

- **Step 2: The Dictionary D - The Heart of the Algorithm**
  - **Key concept:** `D` maps composite numbers to their "step size" (the prime that generated them).
  - **Dictionary structure:** `D[composite] = step`
    - `composite`: A composite number that will be encountered in the future.
    - `step`: The amount to add to find the next odd multiple of the generating prime.
  - **Why this works:** Instead of pre-marking all multiples (like classical sieve), we only track the **next** composite for each prime we've discovered.
  - **Memory efficiency:** At any point, `D` contains roughly $\sqrt{n}$ entries (one per prime up to $\sqrt{n}$), not $n$ entries.

- **Step 3: Processing Each Candidate**
  - For each candidate `c` from the sequence $3, 5, 7, 9, 11, \ldots$:
  
  **Case 1: `c not in D` (c is prime)**
  - If `c` is not a key in `D`, then `c` has never been marked as composite, so it must be prime.
  - **Yield the prime:** `yield c`
  - **Schedule future composites:** Store `D[c * c] = 2 * c`
    - `c * c`: The first composite we need to mark is $c^2$ (all smaller multiples have already been handled by smaller primes).
    - `2 * c`: The step size between consecutive odd multiples of `c` (e.g., for $c=3$: $9, 15, 21, 27, \ldots$ differ by $6 = 2 \times 3$).
  - **Example:** When we discover prime $5$:
    - Store `D[25] = 10` (mark $25 = 5^2$ as composite, with step $10 = 2 \times 5$).
    - Future odd multiples: $25, 35, 45, 55, \ldots$ (each differs by 10).

  **Case 2: `c in D` (c is composite)**
  - If `c` is a key in `D`, then `c` was previously marked as composite by some prime.
  - **Retrieve step size:** `step = D.pop(c)` (remove `c` from dictionary and get its step).
  - **Find next unmarked multiple:** Compute `next_multiple = c + step`.
  - **Handle collisions:** While `next_multiple` is already in `D`, keep adding `step` until finding an available slot.
    - This handles the case where multiple primes have the same composite multiple.
    - Example: $15$ is a multiple of both $3$ and $5$, so we need to find the next available slot.
  - **Update dictionary:** Store `D[next_multiple] = step`.
  - **Do not yield:** `c` is composite, so we continue to the next candidate.

- **Step 4: Why Collisions Are Rare but Handled**
  - Collisions occur when multiple primes have the same composite multiple.
  - Example: $15 = 3 \times 5 = 5 \times 3$
  - The `while next_multiple in D` loop ensures we find the next available slot.
  - In practice, collisions are rare, so the loop typically executes once.

- **Step 5: Finding the nth Prime**
  - Create an instance of the generator: `prime_gen = prime_generator()`
  - Iterate through the generator, counting primes: `for prime in prime_gen`
  - Track the count: `primes_found += 1`
  - When `primes_found == nth`, break.
  - Print the last prime found: `print(prime)`

- **Performance Characteristics:**
  - Dictionary operations are very fast on average, making each prime check efficient.
  - Dictionary `D` contains approximately $\sqrt{n}$ entries at any point, making it much more memory-efficient than storing all primes or a large sieve array.

- **Efficiency:** This solution strikes an excellent balance between speed and memory usage. It's significantly faster than trial division and avoids the memory overhead of allocating a large sieve array. The incremental nature makes it ideal for finding specific primes without generating all smaller ones simultaneously.

---

## Output

```
104743
```

---

## Notes

- The 10,001st prime number is $104{,}743$.
- **Solution 2** is optimal when you need all primes up to a limit (batch generation), leveraging the Rosser-Schoenfeld bound with the classical Sieve of Eratosthenes.
- **Solution 3** is optimal when you need a specific nth prime or want to generate primes on demand without knowing an upper bound in advance. The incremental sieve with generators showcases elegant Python programming and efficient algorithm design.
- The inequality $p_n < n(\ln(n) + \ln(\ln(n)))$ for the $n$-th prime, $p_n$, is a key explicit upper bound proven by J. Barkley Rosser and Lowell Schoenfeld in their 1962 paper, "Approximate Formulas for Some Functions of Prime Numbers." It holds true for all integers $n \ge 6$ (and thus for all primes $p_n \ge 13$).
- The incremental sieve algorithm was popularized by Melissa O'Neill in her 2009 paper "The Genuine Sieve of Eratosthenes" and represents a significant improvement over naive implementations.
- For educational purposes, all three solutions demonstrate different algorithmic paradigms:
  - **Solution 1:** Brute force with trial division
  - **Solution 2:** Batch processing with mathematical bounds
  - **Solution 3:** Lazy evaluation with incremental discovery
- The problem beautifully illustrates the progression from naive algorithms to sophisticated, mathematically-grounded solutions.
