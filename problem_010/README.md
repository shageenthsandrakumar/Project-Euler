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
  - Create a boolean array `is_prime` of size `(limit-1)//2` to represent odd numbers from $1$ to $\text{limit}-1$.
  - Index mapping: `is_prime[i]` corresponds to the number $2i + 1$.
    - `is_prime[0]` → $1$ (not prime, set to `False`)
    - `is_prime[1]` → $3$ (prime)
    - `is_prime[2]` → $5$ (prime)
    - `is_prime[3]` → $7$ (prime)
  - For `limit = 2,000,000`: array size is $999,999$, covering odd numbers $1$ through $1,999,999$.
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
- Use an **interleaved iteration** through candidates: $5 \to 7 \to 11 \to 13 \to 17 \to 19 \to \ldots$
- For each prime found, mark its multiples in both sieves using carefully computed starting points.
- This reduces memory usage to approximately $\frac{2}{3}$ of the half-sieve approach (33% of full sieve).

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
    - Size: `K_max_plus = (limit - 2) // 6 + 1`
    - Index $k$ represents number $6k + 1$.
    - Set `sieve_plus1[0] = False` because $6(0)+1 = 1$ is not prime.
  - **Sieve for $6k+5$:**
    - Size: `K_max_minus = (limit - 6) // 6 + 1`
    - Index $k$ represents number $6k + 5$.
  - For `limit = 2,000,000`:
    - `K_max_plus = 333,334` covering $1$ through $1,999,999$.
    - `K_max_minus = 333,333` covering $5$ through $1,999,997$.

- **Step 3: Interleaved Prime Checking**
  - Start with `p = 5` and iterate up to $\sqrt{\text{limit}}$.
  - For each candidate $p$, determine its form:
    - If $p \equiv 1 \pmod{6}$: Check `sieve_plus1[(p-1)//6]`.
    - If $p \equiv 5 \pmod{6}$: Check `sieve_minus1[(p-5)//6]`.
  - Advance to the next candidate:
    - If $p \equiv 1 \pmod{6}$: increment by $4$ to get the next $6k+5$ form.
    - If $p \equiv 5 \pmod{6}$: increment by $2$ to get the next $6k+1$ form.
  - This creates the pattern: $5, 7, 11, 13, 17, 19, 23, 25, \ldots$ (alternating between the two forms).

- **Step 4: Marking Composites**
  - When a prime $p$ is found, mark its multiples in both sieves.
  - **For $p \equiv 1 \pmod{6}$ (e.g., $p = 7$):**
    - Multiples of form $6k+1$: Start at $p^2$ and step by $p$ indices.
      - Starting index: `(p*p - 1) // 6`
      - Mark: `sieve_plus1[start_k_1::p] = False`
    - Multiples of form $6k+5$: Start at $p(p+4)$ and step by $p$ indices.
      - Starting index: `(p*(p+4) - 5) // 6`
      - Mark: `sieve_minus1[start_k_2::p] = False`
  - **For $p \equiv 5 \pmod{6}$ (e.g., $p = 5$):**
    - Multiples of form $6k+1$: Start at $p^2$ and step by $p$ indices.
      - Starting index: `(p*p - 1) // 6`
      - Mark: `sieve_plus1[start_k_1::p] = False`
    - Multiples of form $6k+5$: Start at $p(p+2)$ and step by $p$ indices.
      - Starting index: `(p*(p+2) - 5) // 6`
      - Mark: `sieve_minus1[start_k_2::p] = False`
  - **Why these starting points work:**
    - For a prime $p = 6j+1$, the first unmarked odd multiple of form $6k+1$ is $p^2 = (6j+1)^2 = 36j^2 + 12j + 1 \equiv 1 \pmod{6}$.
    - The first unmarked multiple of form $6k+5$ is $p(p+4) = (6j+1)(6j+5) = 36j^2 + 36j + 5 \equiv 5 \pmod{6}$.
    - Similar reasoning applies for $p = 6j+5$.

- **Step 5: Extracting Primes**
  - Start with `answer = 2 + 3` (the primes less than $5$).
  - Extract indices from `sieve_plus1` and convert to primes: $6k + 1$.
  - Extract indices from `sieve_minus1` and convert to primes: $6k + 5$.
  - Sum all primes.

- **Efficiency:** This solution uses approximately **67% less memory** than a full sieve (storing only numbers $\not\equiv 0, 2, 3, 4 \pmod{6}$). However, the implementation is **significantly more complex** than the half-sieve. The interleaved iteration and dual starting-point calculations require careful mathematical reasoning. The sieving process itself has similar performance to the half-sieve, but the added complexity makes it harder to understand and debug.

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
  - Create boolean array `is_prime_k` of size `K_max = (limit - 1) // 2`.
  - Index $k$ represents the odd number $2k + 1$.
  - For `limit = 2,000,000`: `K_max = 999,999`, covering odd numbers $1$ through $1,999,997$.
  - Initialize all to `True` (assume all odd numbers are prime).

- **Step 3: Computing the Upper Bound for $i$**
  - We need the maximum $i$ such that there exists at least one valid $j \geq i$ where $k = i + j + 2ij < K_{\max}$.
  - The minimum $j$ is $i$ (to avoid duplicate pairs), so:
    $$i + i + 2i^2 < K_{\max}$$
    $$2i^2 + 2i < K_{\max}$$
    $$i^2 + i < K_{\max}/2$$
  - Solving this quadratic inequality: $i < \frac{-1 + \sqrt{1 + 2K_{\max}}}{2}$.
  - The code uses: `i_max = int(np.floor((np.sqrt(1 + 8 * K_max - 1) - 1) / 4))`.
  - Due to operator precedence, this evaluates as: `np.sqrt((8 * K_max) - 1 + 1) = np.sqrt(8 * K_max)`.
  - Simplifying: $\frac{\sqrt{8K_{\max}} - 1}{4} = \frac{2\sqrt{2K_{\max}} - 1}{4} \approx \frac{\sqrt{2K_{\max}}}{2}$, which is approximately the correct bound.

- **Step 4: Marking Composites**
  - For each $i$ from $1$ to $i_{\max}$:
    - Compute the range of valid $j$ values:
      - `j_start = i` (ensures $j \geq i$, avoiding duplicates).
      - `j_end = (K_max - i - 1) // (1 + 2 * i)` (ensures $k < K_{\max}$).
    - If `j_end < j_start`, break (no more valid pairs exist for larger $i$).
    - For all $j$ in `[j_start, j_end]`:
      - Compute $k = i + j + 2ij$.
      - Collect all $k$ values in a list.
  - After iterating through all $i$, concatenate all composite indices and mark them as `False` in the sieve.

- **Step 5: Extracting Primes**
  - Use `np.nonzero(is_prime_k)[0]` to find all `True` indices.
  - Filter out $k = 0$ (which represents $1$, not prime): `prime_k_indices = prime_k_indices[prime_k_indices > 0]`.
  - Convert indices to actual numbers: $2k + 1$.
  - Add $2$ (the only even prime) to the sum.

- **Step 6: Computing the Sum**
  - The sum of primes is: $2 + \sum (2k + 1) = 2 + 2 \sum k + \text{count}$.
  - Implementation: `answer = 2 + 2 * np.sum(prime_k_indices) + len(prime_k_indices)`.

- **Efficiency:** The Sieve of Sundaram is **mathematically elegant** but **practically slower** than the Sieve of Eratosthenes. The nested loops over $i$ and $j$ result in significantly more work than the simple half-sieve — for each value of $i$ (up to roughly $\sqrt{n}$), the algorithm iterates through many valid $j$ values. However, the vectorized NumPy implementation helps mitigate this. Memory usage is similar to the half-sieve (storing only odd numbers). The main advantage of this algorithm is its **pedagogical value** — it demonstrates a completely different approach to prime identification based on direct algebraic computation rather than iterative sieving.

---

## Historical Note: The Sieve of Sundaram

The Sieve of Sundaram was discovered in 1934 by S. P. Sundaram, an Indian student from Sathyamangalam. It was first published in "The Mathematics Student" journal, Volume 2, Number 2, 1934, by V. Ramaswami Aiyar. The algorithm later gained wider attention when it was featured in Scripta Mathematica in 1941 under the title "Curiosa 81. A New Sieve for Prime Numbers".

Despite its mathematical elegance and being based on simple arithmetic progressions, the Sieve of Sundaram remains less well-known than other prime-finding algorithms. The algorithm appeared more than 2,000 years after Eratosthenes developed his famous sieve (circa 200 BCE).

The key insight is that Sundaram's method is equivalent to the Sieve of Eratosthenes for odd numbers, with the "crossing out" of multiples of 2 done by the final double-and-increment step (converting index $k$ to number $2k+1$). However, the algorithm performs more culling operations than the Sieve of Eratosthenes because it uses all odd numbers as base values rather than just odd primes.

While the Sieve of Sundaram is slower than Eratosthenes for large limits, it demonstrates that multiple mathematical approaches can solve the same problem, offering both pedagogical value and historical interest in the study of number theory.

---

## Comparison of Solutions

| Aspect | Solution 1<br>(Half-Sieve) | Solution 2<br>(Dual 6k±1) | Solution 3<br>(Sundaram) |
|--------|---------------------------|--------------------------|-------------------------|
| **Memory Usage** | ~1 MB<br>(50% of full) | ~0.67 MB<br>(33% of full) | ~1 MB<br>(50% of full) |
| **Sieving Strategy** | Mark multiples of primes | Mark multiples in 2 sieves | Direct composite computation |
| **Implementation** | Simple and intuitive | Complex dual-sieve logic | Moderate complexity |
| **Mathematical Insight** | Skip even numbers | Skip multiples of 2 and 3 | Algebraic formula for composites |
| **Speed** | Very fast | Very fast | Slower |
| **Code Clarity** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| **Best For** | General use | Memory-constrained systems | Educational purposes |

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
- **Solution 2** (Dual Sieve) achieves the best memory efficiency but at the cost of significantly increased complexity. The 33% memory savings over the half-sieve rarely justify the added complexity in practice.
- **Solution 3** (Sieve of Sundaram) is historically significant and mathematically elegant, demonstrating that prime identification can be approached through direct algebraic computation rather than iterative sieving. However, its slower performance makes it primarily valuable for educational purposes.
- All three solutions correctly interpret "below two million" as strictly less than $2,000,000$.
- The problem demonstrates that while there are multiple valid algorithmic approaches to finding primes, the classical Sieve of Eratosthenes (with the half-sieve optimization) remains the gold standard for balancing simplicity, speed, and memory efficiency.
