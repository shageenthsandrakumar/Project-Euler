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

- **Efficiency:** Trial division is straightforward but inefficient for large thresholds. For $\text{nums} = 20$, it performs approximately $20$ iterations with divisibility checks against a growing list of primes.

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
  - Create a boolean array `is_prime` of size `(nums+1)//2` to represent only odd numbers up to and including `nums`.
  - Index mapping: `is_prime[i]` corresponds to the number $2i + 1$.
    - `is_prime[0]` → $1$ (not prime, set to `False`)
    - `is_prime[1]` → $3$ (prime)
    - `is_prime[2]` → $5$ (prime)
    - `is_prime[3]` → $7$ (prime)
  - The array size ensures all odd numbers up to `nums` are included in the sieve.
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
    - Implementation: `is_prime[i*i//2::i] = False`
    - **Understanding the slice `i*i//2::i`:**
      - **Starting point (`i*i//2`):** The index for $i^2$ in the half-sieve is $(i^2 - 1) / 2 = i^2 // 2$ (integer division).
      - **Step size (`i`):** Consecutive odd multiples of $i$ differ by $2i$ in actual number space. In index space (where each index represents a jump of 2), the step is $2i / 2 = i$.

- **Step 3: Extracting Primes**
  - Use `np.nonzero(is_prime)[0]` to get indices of all `True` entries (odd primes).
  - Convert indices back to actual numbers: $2 \times \text{index} + 1$.
  - Prepend $2$ (the only even prime) using `np.r_[2, 2*np.nonzero(is_prime)[0]+1]`.
  - Because the sieve size is `(nums+1)//2`, all primes up to and including `nums` are automatically captured.

- **Step 4: Computing Exponents and LCM**
  - Use the same logarithmic formula as Solution 1:
    - `exponents = np.log(nums) // np.log(primes)`
  - Compute the LCM: `int(np.prod(primes**exponents))`

- **Efficiency:** The half-sieve is approximately **2× faster** than the full sieve and uses **50% less memory**. This is the most efficient method for generating primes up to moderate limits.

---

## Solution 3: Incremental Sieve with Python Generators

### Approach

- Use an **incremental sieve of Eratosthenes** implemented as a Python generator that yields primes one at a time.
- Unlike Solutions 1 and 2, this approach doesn't store all primes in memory—it generates them on-demand as needed.
- The algorithm uses a dictionary to track composite numbers and their step sizes, allowing it to identify primes without pre-computing a full sieve.
- Process each prime as it's generated, computing its exponent and immediately multiplying it into the running product.
- This streaming approach is extremely memory-efficient and well-suited for this problem.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Understanding Python Generators**
  - **Generators** are Python functions that use `yield` instead of `return` to produce values lazily (on-demand).
  - When you call `next()` on a generator, it runs until it hits a `yield` statement, returns that value, then pauses.
  - The next time you call `next()`, it resumes right where it left off with all local variables intact.
  - Benefits for this problem:
    - **Memory efficient:** Only the current prime exists in memory, not an entire list or array.
    - **Lazy evaluation:** Each prime is computed only when needed.
    - **Infinite capability:** The generator can theoretically produce primes forever without running out of memory.

- **Step 2: The Incremental Sieve Algorithm**
  - **Core data structure:** A dictionary `D` that maps composite numbers to their step sizes.
    - **Key:** A composite number that we know about.
    - **Value:** The step size to find the next multiple of the prime that generated this composite.
  - **Algorithm walkthrough:**
    - First, yield $2$ immediately (the only even prime).
    - Start checking odd candidates $c$ beginning at $3$ (incrementing by $2$ each time).
    - For each candidate $c$:
      - **If $c$ is NOT in dictionary `D`:** Then $c$ has never been marked as composite, so $c$ must be prime. Yield $c$ as the next prime. Add a new entry: `D[c*c] = 2*c`. This marks $c^2$ as composite (the first multiple we care about) with step $2c$ (to get subsequent odd multiples).
      - **If $c$ IS in dictionary `D`:** Then $c$ is composite (some prime marked it earlier). Don't yield $c$. Retrieve and remove the step size: `step = D.pop(c)`. Calculate the next odd multiple: `next_multiple = c + step`. If `next_multiple` is already in `D`, keep adding `step` until we find an empty slot. Store the step at the new location: `D[next_multiple] = step`.

- **Step 3: Why Start at $c^2$?**
  - When we discover a prime $p$, all of its smaller multiples ($2p, 3p, 4p, \dots, (p-1)p$) have already been marked by smaller primes.
  - For example, when we discover $p = 7$:
    - $7 \times 2 = 14$ was marked when processing $2$.
    - $7 \times 3 = 21$ was marked when processing $3$.
    - $7 \times 5 = 35$ was marked when processing $5$.
  - The first unmarked multiple is always $p \times p = p^2$ (in this case, $49$).
  - This is why we initialize `D[c*c]` rather than `D[c*2]` or `D[c*3]`.

- **Step 4: Example Execution Trace**
  - Start: `D = {}`, yield $2$
  - $c = 3$: Not in `D` → yield $3$, set `D[9] = 6`
  - $c = 5$: Not in `D` → yield $5$, set `D[25] = 10`
  - $c = 7$: Not in `D` → yield $7$, set `D[49] = 14`
  - $c = 9$: In `D`! → composite, `step = 6`, set `D[15] = 6` (next odd multiple of $3$)
  - $c = 11$: Not in `D` → yield $11$, set `D[121] = 22`
  - $c = 13$: Not in `D` → yield $13$, set `D[169] = 26`
  - $c = 15$: In `D`! → composite, `step = 6`, set `D[21] = 6`
  - And so on...

- **Step 5: Memory Efficiency**
  - **Solution 1:** Stores all primes up to $n$ in a list, then converts to a NumPy array. For $n = 20$, this is 8 primes.
  - **Solution 2:** Stores a boolean array of size $(n+1)/2$. For $n = 20$, this is 10 boolean values.
  - **Solution 3:** Stores only dictionary entries for composites near the current candidate. For $n = 20$, the dictionary peaks at about 2-3 entries.
  - **Key difference:** Solution 3 doesn't keep any primes in memory—each prime is generated, used to update the answer, then discarded.
  - **No NumPy overhead:** Solution 3 uses only native Python types, avoiding the memory overhead of NumPy arrays and the import cost.

- **Step 6: Computing the LCM**
  - Initialize `answer = 1` to accumulate the product.
  - Create the generator: `prime_gen = prime_generator()`.
  - Loop through primes using `for p in prime_gen`:
    - **Stopping condition:** If $p > \text{nums}$, break the loop.
    - Compute the exponent: $k = \lfloor \frac{\ln(\text{nums})}{\ln(p)} \rfloor$ using `int(math.log(nums)/math.log(p))`.
    - Multiply the answer: `answer *= p**k`.
  - After the loop, `answer` contains the LCM.

- **Efficiency:** For this specific problem (finding LCM up to 20), Solution 3 is the most memory-efficient. It generates only 9 primes (stopping at 23, which is the first prime > 20) and uses minimal memory. The dictionary never holds more than a handful of entries. For generating all primes up to very large limits, Solution 2's array-based approach is faster due to cache efficiency, but Solution 3 excels when you only need a small number of primes or want to generate primes indefinitely.

---

## Output

```
232792560
```

---

## Notes

- The smallest number divisible by all integers from $1$ to $20$ is $232{,}792{,}560$.
- Prime factorization: $232{,}792{,}560 = 2^4 \times 3^2 \times 5 \times 7 \times 11 \times 13 \times 17 \times 19$.
- **Solution 2** is the optimal approach for generating large batches of primes, leveraging the half-sieve optimization for efficient prime generation.
- **Solution 3** is the most memory-efficient approach and is ideal for this specific problem, using only standard Python libraries and generating primes on-demand.
- This incremental sieve algorithm is sometimes called the **"Postponed Sieve"** or **"Priority Queue Sieve"** and was popularized by Melissa O'Neill in her 2009 paper *"The Genuine Sieve of Eratosthenes"*.
- The problem is equivalent to finding $\text{LCM}(1, 2, 3, \dots, 20)$.
- Simply multiplying all numbers from $1$ to $20$ would produce a much larger number with redundant prime factors. The LCM approach ensures each prime appears with the minimal necessary exponent.
- The logarithmic method for computing exponents avoids iterative division and is highly efficient for vectorized operations.
- Using array size `(nums+1)//2` ensures all odd numbers up to and including `nums` are represented in the sieve.
- The incremental sieve's dictionary size is proportional to the number of primes up to $\sqrt{n}$, which grows much slower than $n$ itself.
