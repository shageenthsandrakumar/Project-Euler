# Problem 10: Summation of Primes

**Problem source:** [Project Euler Problem 10](https://projecteuler.net/problem=10)

**Problem statement:**

The sum of the primes below $10$ is $2 + 3 + 5 + 7 = 17$.

Find the sum of all the primes below two million.

---

## Solution 1: Standard Sieve of Eratosthenes (Odd Numbers Only)

### Approach

- Use the **Sieve of Eratosthenes** with a **half-sieve optimization** that stores only odd numbers.
- The basic sieve marks multiples of each prime as composite, leaving only primes unmarked.
- The half-sieve recognizes that all primes (except $2$) are odd, so we can skip all even numbers entirely.
- Map array indices to actual numbers using: index $i$ represents number $2i + 1$.
- Extract all primes and compute their sum.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Half-Sieve Initialization**
  - Create a boolean array `is_prime` of size `limit//2` to represent odd numbers from $1$ to $\text{limit}-1$.
  - Index mapping: `is_prime[i]` corresponds to the number $2i + 1$.
    - `is_prime[0]` → $1$ (not prime, set to `False`)
    - `is_prime[1]` → $3$ (prime)
    - `is_prime[2]` → $5$ (prime)
    - `is_prime[3]` → $7$ (prime)
  - For `limit = 2,000,000`: array size is $1,000,000$, covering odd numbers $1$ through $1,999,999$.
  - Initialize all entries to `True` (assume all odd numbers are prime initially).
  - Set `is_prime[0] = False` because $1$ is not prime.

- **Step 2: Sieve Process**
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
      - **Starting point (`i*i//2`):** The index for $i^2$ in the half-sieve is $i^2 // 2$ (integer division).
      - **Step size (`i`):** Consecutive odd multiples of $i$ differ by $2i$ in actual number space. In index space (where each index represents a jump of 2), the step is $2i / 2 = i$.

- **Step 3: Extracting Primes**
  - Use `np.nonzero(is_prime)[0]` to get indices of all `True` entries (odd primes).
  - Convert indices back to actual numbers: $2 \times \text{index} + 1$.
  - Prepend $2$ (the only even prime) using `np.r_[2, 2*np.nonzero(is_prime)[0]+1]`.

- **Step 4: Computing the Sum**
  - Sum all primes using Python's built-in `sum()` function.
  - The result is $142,913,828,922$.

- **Efficiency:** This is a highly efficient solution. The half-sieve uses approximately $1$ MB of memory for the boolean array (storing only odd numbers). The sieving process examines roughly $\sqrt{2{,}000{,}000} \approx 1,414$ candidate primes and marks their multiples. This makes it one of the fastest algorithms for finding all primes below a given limit.

---

## Solution 2: Dual Sieve (6k±1 Optimization)

### Approach

- Exploit the mathematical property that all primes greater than $3$ have the form $6k+1$ or $6k+5$ (equivalently $6k-1$).
- Maintain **two separate sieves**: one for numbers of form $6k+1$ and another for $6k+5$.
- Use an **alternating step pattern** through candidates: $5 \to 7 \to 11 \to 13 \to 17 \to 19 \to \ldots$
- For each prime found, mark its multiples in both sieves using carefully computed starting points.
- This reduces memory usage to approximately $\frac{1}{3}$ of a full sieve.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Mathematical Foundation**
  - Any integer can be written in one of six forms: $6k$, $6k+1$, $6k+2$, $6k+3$, $6k+4$, or $6k+5$.
  - Eliminating multiples of $2$ and $3$:
    - $6k$, $6k+2$, $6k+4$ are divisible by $2$.
    - $6k+3$ is divisible by $3$.
    - Only $6k+1$ and $6k+5$ can be prime (for $k \geq 1$).
  - Therefore, we only need to check numbers of these two forms.

- **Step 2: Dual Sieve Initialization**
  - **Sieve for $6k+1$:**
    - Size: `(limit - 1) // 6 + 1`
    - Index $k$ represents number $6k + 1$.
    - Set `sieve_plus1[0] = False` because $6(0)+1 = 1$ is not prime.
  - **Sieve for $6k+5$:**
    - Size: `(limit - 5) // 6 + 1`
    - Index $k$ represents number $6k + 5$.
  - For `limit = 2,000,000`:
    - `sieve_plus1` has size $333,334$ covering $1, 7, 13, 19, \ldots, 1,999,999$.
    - `sieve_minus1` has size $333,333$ covering $5, 11, 17, 23, \ldots, 1,999,997$.

- **Step 3: Alternating Prime Checking with Step Variable**
  - Start with `p = 5` and `step = 2`.
  - The variable `step` holds the increment to reach the **next** candidate:
    - When `step = 2`, current `p` is of form $6k+5$ (e.g., $5, 11, 17$).
    - When `step = 4`, current `p` is of form $6k+1$ (e.g., $7, 13, 19$).
  - For each candidate `p`:
    - Calculate index: `k = p // 6`
    - Check primality based on `step`:
      - If `step == 2`: check `sieve_minus1[k]`
      - If `step == 4`: check `sieve_plus1[k]`
  - Advance to next candidate: `p += step`
  - Toggle step: `step = 6 - step` (alternates between 2 and 4)

- **Step 4: Marking Composites**
  - When a prime $p$ is found, mark its multiples in both sieves.
  - **Multiples in $6k+1$ sieve:**
    - Start at $p^2$: `start_1 = p**2 // 6`
    - Mark: `sieve_plus1[start_1::p] = False`
    - This works because $p^2$ is always of form $6k+1$ for any $6k \pm 1$ prime.
  - **Multiples in $6k+5$ sieve:**
    - Start at $p \times (p + \text{step})$: `start_2 = p*(p + step) // 6`
    - Mark: `sieve_minus1[start_2::p] = False`
    - **Why this formula works:**
      - When $p \equiv 5 \pmod{6}$ (step=2): $p+2$ gives first $6k+1$ multiplier, so $p(p+2)$ is first $6k+5$ multiple $\geq p^2$.
      - When $p \equiv 1 \pmod{6}$ (step=4): $p+4$ gives first $6k+5$ multiplier, so $p(p+4)$ is first $6k+5$ multiple $\geq p^2$.
    - The elegance: a single formula `p*(p + step)` handles both cases without conditionals.

- **Step 5: Extracting Primes**
  - Start with `answer = 2 + 3` (the primes less than $5$).
  - Extract indices from `sieve_plus1` and convert to primes: $6k + 1$.
  - Extract indices from `sieve_minus1` and convert to primes: $6k + 5$.
  - Sum all primes.

- **Efficiency:** This solution uses approximately **33% less memory** than a full sieve (storing only numbers $\equiv 1, 5 \pmod{6}$). The implementation is **significantly more complex** than the half-sieve, requiring careful index calculations and understanding of modular arithmetic. The sieving process itself has similar performance to the half-sieve, but the added complexity makes it harder to understand and debug. The clever use of the alternating `step` variable to determine both the current prime's form and the sieving start point demonstrates elegant algorithm design.

---

## Solution 3: Sieve of Sundaram

### Approach

- Use the **Sieve of Sundaram**, a lesser-known but mathematically elegant alternative to the Sieve of Eratosthenes.
- The key insight: an odd number $n = 2k+1$ is **composite** if and only if $k$ can be expressed as $k = i + j + 2ij$ for positive integers $i, j$.
- Directly compute all composite indices using this formula, then extract primes.
- This approach demonstrates a fundamentally different method: **direct computation of composites** rather than iterative marking of multiples.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: The Sundaram Formula**
  - **Theorem:** A number $n = 2k+1$ is composite if and only if $k = i + j + 2ij$ for some positive integers $i, j$ with $1 \leq i \leq j$.
  - **Proof of forward direction:**
    - If $k = i + j + 2ij$, then:
      $$2k + 1 = 2(i + j + 2ij) + 1 = 2i + 2j + 4ij + 1 = (2i + 1)(2j + 1)$$
    - This shows $2k+1$ is the product of two odd numbers greater than $1$, making it composite.
  - **Proof of reverse direction:**
    - Any odd composite $n$ can be factored as $n = (2i+1)(2j+1)$ for some $i, j \geq 1$.
    - Expanding: $n = 4ij + 2i + 2j + 1 = 2(2ij + i + j) + 1$.
    - So $k = 2ij + i + j = i + j + 2ij$.

- **Step 2: Index Mapping**
  - Create boolean array `is_prime_k` of size `K_max + 1` where `K_max = (limit - 1) // 2`.
  - Index $k$ represents the odd number $2k + 1$.
  - For `limit = 2,000,000`: `K_max = 999,999`, and array size is $1,000,000$, covering odd numbers $1$ through $1,999,999$.
  - Initialize all to `True` (assume all odd numbers are prime).
  - Set `is_prime_k[0] = False` to mark $1$ as not prime.

- **Step 3: Computing the Upper Bound for $i$**
  - We need the maximum $i$ such that there exists at least one valid $j \geq i$ where $k = i + j + 2ij \leq K_{\max}$.
  - The minimum $j$ is $i$ (to avoid duplicate pairs), so:
    $$i + i + 2i^2 \leq K_{\max}$$
    $$2i^2 + 2i \leq K_{\max}$$
  - Solving this quadratic inequality: $i \leq \frac{-1 + \sqrt{1 + 2K_{\max}}}{2}$.
  - The code uses: `i_max = int((-1 + np.sqrt(1 + 2 * K_max)) / 2)`

- **Step 4: Marking Composites**
  - For each $i$ from $1$ to $i_{\max}$:
    - Compute the range of valid $j$ values:
      - `j_start = i` (ensures $j \geq i$, avoiding duplicates).
      - `j_end = (K_max - i) // (1 + 2 * i)` (ensures $k \leq K_{\max}$).
        - This comes from solving $i + j + 2ij \leq K_{\max}$ for $j$:
        - $j(1 + 2i) \leq K_{\max} - i$
        - $j \leq \frac{K_{\max} - i}{1 + 2i}$
    - If `j_end < j_start`, break (no more valid pairs exist for larger $i$).
    - For all $j$ in `[j_start, j_end]`:
      - Compute $k = i + j + 2ij$ using vectorized NumPy: `k_values = i + J_slice + 2 * i * J_slice`.
      - Mark directly: `is_prime_k[k_values] = False`.

- **Step 5: Extracting Primes and Computing Sum**
  - Use `np.nonzero(is_prime_k)[0]` to find all `True` indices (prime indices).
  - Convert to actual primes and compute sum efficiently:
    - Sum formula: $2 + \sum_{k} (2k + 1) = 2 + 2\sum k + \text{count}(k)$
    - Prepend $2$ using `np.r_[2, 2*np.nonzero(is_prime_k)[0]+1]`
    - Calculate sum: `np.sum(primes)`

- **Efficiency:** The Sieve of Sundaram is **mathematically elegant** but **practically slower** than the Sieve of Eratosthenes. The nested structure over $i$ and $j$ results in more computational work than the simple half-sieve. For each value of $i$ (up to roughly $\sqrt{n/2}$), the algorithm iterates through many valid $j$ values. However, the vectorized NumPy implementation helps mitigate this. Memory usage is similar to the half-sieve (storing only odd numbers). The main advantage of this algorithm is its **pedagogical value**. The algorithm demonstrates a completely different approach to prime identification based on direct algebraic computation rather than iterative sieving.

---

## Solution 4: Incremental Prime Generator

### Approach

- Use an **incremental prime generator** that yields primes one at a time without pre-computing a sieve.
- Maintain a dictionary tracking the next multiple to mark for each prime discovered.
- For each candidate odd number, check if it appears in the dictionary:
  - If not, it's considered a prime number. The generator yields it and adds $p^2$ to the dictionary.
  - If yes, advance the multiple by the prime's step until finding an empty slot.
- Sum primes as they're generated until reaching the threshold.

**Reference:** The full Python implementation is available in [`solution_4.py`](solution_4.py).

### Detailed Explanation

- **Step 1: Generator Design**
  - The function `prime_generator()` is a Python generator that yields primes on demand.
  - Start by yielding $2$ (the only even prime).
  - Initialize empty dictionary `D = {}` to track composite numbers.
  - Use `itertools.count(3, 2)` to generate odd candidates: $3, 5, 7, 9, \ldots$

- **Step 2: Dictionary Structure**
  - **Key:** A composite number $c$ that will be encountered in the future.
  - **Value:** The step size (the prime $p$ whose multiple this is).
  - **Invariant:** For each prime $p$ discovered, the dictionary eventually tracks $p^2$, then $p^2 + 2p$, then $p^2 + 4p$, etc.

- **Step 3: Checking Each Candidate**
  - For each candidate $c$:
    - **If $c$ not in dictionary:** $c$ is prime.
      - Yield $c$ as a prime.
      - Add entry: `D[c * c] = 2 * c`
        - This marks $c^2$ as the first composite multiple.
        - The value $2c$ is the step size (only odd multiples matter).
    - **If $c$ in dictionary:** $c$ is composite.
      - Retrieve the step: `step = D.pop(c)`
      - Find next available multiple: `next_multiple = c + step`
      - While `next_multiple` is already in dictionary:
        - `next_multiple += step` (skip to next odd multiple)
      - Store: `D[next_multiple] = step`

- **Step 4: Collision Handling**
  - The `while next_multiple in D:` loop handles collisions.
  - **Example collision:** When checking $c = 45$:
    - $45 = 3 \times 15$, so dictionary has entry from prime $3$.
    - $45 = 5 \times 9$, so dictionary might also have entry from prime $5$.
    - The loop advances to the first free slot ($45 + 6 = 51$ or higher).

- **Step 5: Summing Primes**
  - Create generator: `prime_gen = prime_generator()`
  - Iterate: `for p in prime_gen:`
  - Accumulate: `prime_sum += p` while `p < threshold`
  - Break when `p >= threshold`

- **Efficiency:** This approach is **memory-efficient** for finding primes up to a moderate limit, using memory proportional to the number of primes found (approximately $\frac{n}{\ln n}$). For $n = 2,000,000$, this is about $150,000$ primes. However, it's **slower than sieve methods** because:
  - Each prime requires dictionary operations (hash table lookups/insertions).
  - Collision handling adds overhead when multiple primes share the same composite.
  - No vectorization benefits like NumPy sieves.
  
  The main advantage is **simplicity and incremental generation**. Primes are produced one at a time without needing to know the limit in advance. This makes it useful for finding the $n$-th prime or generating primes in a stream. For computing the sum below a known limit, sieve methods are faster.

---

## Comparison of Solutions

| Aspect | Solution 1<br>(Half-Sieve) | Solution 2<br>(Dual 6k±1) | Solution 3<br>(Sundaram) | Solution 4<br>(Generator) |
|--------|---------------------------|--------------------------|-------------------------|-------------------------|
| **Memory Usage** | ~1 MB<br>(50% of full) | ~0.67 MB<br>(33% of full) | ~1 MB<br>(50% of full) | ~10 MB<br>(dict overhead) |
| **Sieving Strategy** | Mark multiples of primes | Mark in 2 sieves | Direct composite computation | Incremental generation |
| **Implementation** | Simple and intuitive | Complex dual-sieve logic | Moderate complexity | Simple generator pattern |
| **Mathematical Insight** | Skip even numbers | Skip multiples of 2 and 3 | Algebraic composite formula | Dynamic composite tracking |
| **Speed** | Very fast | Very fast | Slower | Slowest |
| **Code Clarity** | ★★★★★ | ★★ | ★★★ | ★★★★ |
| **Best For** | General use | Memory-constrained | Educational | Streaming/nth prime |

---

## Output

```
142913828922
```

---

## Notes

- The sum of all primes below two million is $142,913,828,922$.
- There are **148,933 primes** below two million.
- **Solution 1** (Half-Sieve) is the optimal practical choice, offering excellent performance with clear, maintainable code.
- **Solution 2** (Dual Sieve) achieves the best memory efficiency but at the cost of significantly increased complexity. The clever use of the alternating `step` variable demonstrates elegant algorithm design, where a single variable serves dual purposes: identifying the current prime's form and determining the sieving start point.
- **Solution 3** (Sieve of Sundaram) is historically significant and mathematically elegant, demonstrating that prime identification can be approached through direct algebraic computation rather than iterative sieving. However, its slower performance makes it primarily valuable for educational purposes.
- The Sieve of Sundaram was discovered in 1934 by **S. P. Sundaram, an Indian student from Sathyamangalam**. It was first published in **"The Mathematics Student" journal, Volume 2, Number 2**, 1934, by V. Ramaswami Aiyar. The algorithm later gained wider attention when it was featured in Scripta Mathematica in 1941 under the title **"Curiosa 81. A New Sieve for Prime Numbers"**.
- Despite its mathematical elegance and being based on simple arithmetic progressions, the Sieve of Sundaram remains less well-known than other prime-finding algorithms. The algorithm appeared more than 2,000 years after Eratosthenes developed his famous sieve (circa 200 BCE).
- **Solution 4** (Incremental Generator) is useful when primes need to be generated one at a time without knowing the limit in advance, but it's not optimal for computing sums below a known threshold.
- All four solutions correctly interpret "below two million" as strictly less than $2,000,000$.
- The problem demonstrates that while there are multiple valid algorithmic approaches to finding primes, the classical Sieve of Eratosthenes (with the half-sieve optimization) remains the gold standard for balancing simplicity, speed, and memory efficiency when the limit is known in advance.
