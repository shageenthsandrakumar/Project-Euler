# Problem 21: Amicable Numbers

**Problem source:** [Project Euler Problem 21](https://projecteuler.net/problem=21)

**Problem statement:**

Let $d(n)$ be defined as the sum of proper divisors of $n$ (numbers less than $n$ which divide evenly into $n$).

If $d(a) = b$ and $d(b) = a$, where $a \neq b$, then $a$ and $b$ are called an **amicable pair** and each of $a$ and $b$ are called **amicable numbers**.

For example, the proper divisors of $220$ are $1, 2, 4, 5, 10, 11, 20, 22, 44, 55$ and $110$; therefore $d(220) = 284$. The proper divisors of $284$ are $1, 2, 4, 71$ and $142$; so $d(284) = 220$.

Evaluate the sum of all the amicable numbers under $10000$.

---

## Solution 1: Dictionary-Based Pair Tracking with Edge Case Handling

### Approach

- Compute $d(n)$ for each number from $1$ to `threshold - 1` using an efficient factorization algorithm with wheel factorization.
- Use a **dictionary** to track computed values and identify amicable pairs.
- For each number $a$, compute $d(a)$ and check if we've already seen a number $b$ where $d(b) = a$.
- If such a pair exists and $a \neq b$, we've found an amicable pair. Add both numbers to the sum.
- Store $d(a)$ in the dictionary for future lookups.
- **Edge case handling:** After the main loop, check for pairs where one number is below the threshold but its amicable partner is above it.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Efficient Divisor Sum Function**
  - The function `d(n)` computes the sum of proper divisors (all divisors except $n$ itself).
  - **Edge case:** For $n = 0$, return `float('inf')` since every positive integer divides $0$.
  - The function uses **wheel factorization** to efficiently find the prime factorization of $n$.
  - **Extract powers of 2:** Count how many times $2$ divides $n$ using `while not n%2:`.
    - Each power of $2$ contributes to $\sigma(n)$ via the formula: $\sigma(2^k) = 2^{k+1} - 1$.
  - **Extract powers of 3:** Similarly extract all factors of $3$.
    - Formula: $\sigma(3^k) = \frac{3^{k+1} - 1}{2}$.
  - **Wheel factorization for remaining primes:**
    - After removing $2$ and $3$, all remaining primes have the form $6k \pm 1$.
    - Start with `f = 5` and `step = 2`.
    - The alternating step pattern (2, 4, 2, 4, ...) generates the sequence: $5, 7, 11, 13, 17, 19, 23, ...$
    - This checks only $\frac{1}{3}$ of all numbers, skipping multiples of $2$ and $3$ entirely.
  - **Handle remaining prime factor:** If $n > 1$ after all trial divisions, then $n$ itself is prime.
    - For a prime $p$: $\sigma(p) = p + 1$.
  - **Final computation:** Using the multiplicative property of $\sigma$:
    - If $n = p_1^{a_1} \cdot p_2^{a_2} \cdots p_k^{a_k}$, then:
    - $\sigma(n) = \sigma(p_1^{a_1}) \cdot \sigma(p_2^{a_2}) \cdots \sigma(p_k^{a_k})$
    - Return $\sigma(n) - n$ to get the sum of proper divisors.

- **Step 2: Dictionary for Pair Detection**
  - Initialize an empty dictionary `d_values = {}` to store computed values.
  - This dictionary maps each number to its proper divisor sum: `d_values[a] = d(a)`.
  - **Key insight:** By the time we compute $d(a)$, if $b = d(a)$ has already been processed and $d(b) = a$, then $(a, b)$ form an amicable pair.

- **Step 3: Main Loop and Pair Identification**
  - Loop through all numbers from $1$ to `threshold`: `for a in range(threshold):`.
  - Compute `d_value = d(a)`.
  - **Check for amicable pair:**
    - Look up `d_values.get(d_value)`.
    - If this returns $a$ and `d_value` $\neq a$, we've found an amicable pair.
    - **Why this works:** We previously computed `d(d_value) = a`, stored it in the dictionary, and now we've found `d(a) = d_value`.
    - This confirms that `d(a) = d_value` and `d(d_value) = a` with $a \neq$ `d_value`.
  - **Add both numbers:** When a pair is found, add `d_value + a` to the running sum.
    - This adds both members of the pair in a single operation.
  - **Store the current value:** If no pair is found, store `d_values[a] = d_value` for future lookups.

- **Step 4: Why This Avoids Double-Counting**
  - Each amicable pair $(a, b)$ with $a < b$ is counted exactly once:
    - When we process $a$: We compute $d(a) = b$, but $b$ hasn't been processed yet (since $a < b$), so `d_values.get(b)` returns `None`. We store `d_values[a] = b`.
    - When we process $b$: We compute $d(b) = a$. Now `d_values.get(a)` returns $b$ (which we stored earlier). Since $d(a) = b$ and $d(b) = a$ with $a \neq b$, we add both to the sum.
  - The pair is only counted when we reach the larger element $b$.

- **Step 5: Edge Case Handling - Cross-Threshold Pairs**
  - **The problem:** What if there's an amicable pair like $(9500, 12000)$ where one number is below the threshold but its partner is above?
  - After the main loop completes, we have stored all $d(a)$ values for $a <$ threshold in the dictionary.
  - **Second loop:** Iterate through all keys in the dictionary.
    - For each `a` in `d_values`, check if `d_value = d_values[a]` is >= threshold.
    - If `d_value >= threshold` and `d_value != a`, verify if `d(d_value) = a`.
    - **Optimization trick:** Use `amicable_sum += a*int(d(d_value)==a)` to avoid nested if statements.
    - The expression `int(d(d_value)==a)` evaluates to $1$ if true, $0$ if false.
    - This adds $a$ only when the amicable relationship is confirmed.
  - **Why this is necessary:** Without this check, a number like $9500$ would never be counted even though it has an amicable partner.
  - **Efficiency consideration:** The condition `threshold <= d_value < float('inf')` ensures we skip $n = 0$ (which returns infinity) and only check relevant candidates.

- **Step 6: Example Walkthrough (220, 284)**
  - When `a = 220`: Compute $d(220) = 284$ (cached). Check `d_values.get(284)` = not found (284 hasn't been processed). Store `d_values[220] = 284`.
  - When `a = 284`: Compute $d(284) = 220$ (cached). Check `d_values.get(220)` = returns $284$. Since $d(220) = 284$ and $d(284) = 220$ with $220 \neq 284$, add $220 + 284 = 504$ to the sum.

- **Step 7: Example Walkthrough for Edge Case (9500, 12000 - Hypothetical)**
  - When `a = 9500`: Compute $d(9500) = 12000$ (cached). Check `d_values.get(12000)` = not found. Store `d_values[9500] = 12000`.
  - Main loop ends at `threshold - 1`.
  - Second loop: When checking `a = 9500`, find `d_value = 12000 >= threshold`. Compute $d(12000) = 9500$. Since this equals $a$, add $9500$ to the sum.

- **Efficiency:** This solution processes each number from $1$ to `threshold - 1` exactly once, computing its proper divisor sum using optimized factorization. The dictionary lookup is $O(1)$, making pair detection very fast. The second loop only checks numbers below the threshold, and computes $d(n)$ for numbers above the threshold only when necessary. The wheel factorization reduces the number of trial divisions significantly compared to naive approaches.

---

## Solution 2: Memoized Function with Inequality Check and Edge Case Handling

### Approach

- Use **memoization** to cache the results of $d(n)$ computations, avoiding redundant calculations.
- Apply the `@lru_cache` decorator to automatically store and retrieve previously computed values.
- For each number $a <$ threshold, compute $d(a)$.
- **Optimization:** Check for amicable pairs using two conditions:
  - When $d(a) < a$: Both numbers are below threshold, verify and add both.
  - When $d(a) \geq$ threshold: One number is above threshold, verify and add only $a$.
- This dual-condition approach handles all cases elegantly in a single loop.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Memoization with LRU Cache**
  - The `@lru_cache(maxsize=threshold+1)` decorator automatically caches function results.
  - **Cache size:** Set to `threshold + 1` to store all possible values from $0$ to `threshold`.
  - **How it works:** When `d(n)` is called:
    - If the result for $n$ is already cached, return it immediately (O(1) lookup).
    - Otherwise, compute the result, store it in the cache, and return it.
  - This is particularly beneficial because we call `d(d(a))` in the verification step, and `d(a)` was already computed and cached.

- **Step 2: The Divisor Sum Function**
  - Same implementation as Solution 1, using wheel factorization for efficiency.
  - Returns $\sigma(n) - n$, the sum of proper divisors.

- **Step 3: Main Loop with Dual-Condition Logic**
  - Loop through all numbers: `for a in range(threshold):`.
  - Compute `d_value = d(a)`.
  - **Condition 1:** `if d_value < a:`.
    - **Why this condition?**
      - For an amicable pair $(x, y)$ with $x < y <$ threshold, we have:
        - When processing $x$: $d(x) = y$ where $y > x$, so the condition fails and we skip.
        - When processing $y$: $d(y) = x$ where $x < y$, so the condition passes and we check the pair.
      - This ensures each pair where both numbers are below threshold is examined exactly once.
    - **Verification:** Check if `d(d_value) = a`.
    - **Accumulate sum:** `amicable_sum += (d_value+a)*int(d(d_value) == a)`.
      - The expression `int(d(d_value) == a)` evaluates to $1$ if true, $0$ if false.
      - This adds `d_value+a` (both numbers) only when the amicable relationship is confirmed.
  - **Condition 2:** `elif threshold <= d_value < float('inf'):`.
    - **Edge case handling:** This catches pairs where $a <$ threshold but $d(a) \geq$ threshold.
    - For example, if $d(9500) = 12000$, this condition triggers when processing $a = 9500$.
    - **Verification:** Check if `d(d_value) = a`.
    - **Accumulate sum:** `amicable_sum += a*int(d(d_value) == a)`.
      - Add only $a$ (the number below threshold), not $d\_value$.
    - **Why check `< float('inf')`?** To exclude the edge case where $d(0) = \infty$.

- **Step 4: Why Memoization and Dual Conditions Work Together**
  - **Cache hits maximize efficiency:**
    - When we process $a$ and compute $d(a)$, the result is cached.
    - When we check $d(d(a))$ for verification, it's almost always a cache hit.
    - For Condition 1: $d(a) < a$ means we've already processed $d(a)$ earlier, so its value is definitely cached.
    - For Condition 2: Even though $d(a) \geq$ threshold (potentially uncached), computing it once and caching ensures subsequent accesses are fast.
  - **Dual conditions prevent double-counting:**
    - Condition 1 handles pairs where both numbers are below threshold, counting each pair once when we reach the larger number.
    - Condition 2 handles cross-threshold pairs, ensuring the number below threshold is counted.
    - Together, they cover all possible amicable relationships involving at least one number below threshold.

- **Step 5: Example Walkthrough (220, 284)**
  - When `a = 220`: Compute $d(220) = 284$ (cached). Since $284 > 220$ and $284 <$ threshold, neither condition triggers.
  - When `a = 284`: Compute $d(284) = 220$ (cached). Since $220 < 284$, Condition 1 passes. Check $d(220)$ = cache hit returns $284$. Since $d(220) = 284 = a$, we add $220 + 284 = 504$.

- **Step 6: Example Walkthrough for Edge Case (9500, 12000 - Hypothetical)**
  - When `a = 9500`: Compute $d(9500) = 12000$ (cached). Since $12000 \geq$ threshold, Condition 2 passes. Compute $d(12000) = 9500$ (newly cached). Since $d(12000) = 9500 = a$, we add $9500$.

- **Step 7: The Boolean Multiplication Trick**
  - Instead of writing nested if statements:
    ```python
    if d(d_value) == a:
        amicable_sum += ...
    ```
  - We write:
    ```python
    amicable_sum += ... * int(d(d_value) == a)
    ```
  - This is more compact and eliminates a branch in the code.
  - The expression `int(True)` evaluates to $1$, and `int(False)` evaluates to $0$.

- **Efficiency:** Memoization ensures that each unique value of $d(n)$ is computed at most once. The dual-condition approach elegantly handles both standard pairs and edge cases in a single pass. The inequality check in Condition 1 ensures that `d(d_value)` is almost always a cache hit. The combination makes this solution very fast and remarkably concise.

---

## Solution 3: Half-Sieve with Prime-Based Divisor Function

### Approach

**This is the recommended solution** as it combines mathematical insight with computational efficiency. The key innovations are:

1. **Half-Sieve for prime generation:** An optimized variant of the Sieve of Eratosthenes that stores only odd numbers, reducing memory usage by approximately 50%.
2. **Prime-based divisor function:** Leverages the precomputed primes list to perform trial division only on actual primes, avoiding checks on composite numbers.
3. **Intelligent filtering:** Skips categories that are mathematically proven to never be amicable:
   - All odd prime numbers
   - The prime 2
   - All perfect numbers (only 4 below 10,000: 6, 28, 496, 8128)

By eliminating these categories before computation, we avoid wasteful divisor sum calculations on numbers that cannot possibly be amicable.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Half-Sieve Prime Generation**
  - Standard Sieve of Eratosthenes is optimized by observing that all primes (except 2) are odd.
  - **Memory optimization:** Store only odd numbers in a boolean array to reduce memory by ~50%.
  - **Index mapping:** Index $i$ in the array represents the number $2i + 1$.
    - Index 0 = number 1 (marked false, not prime)
    - Index 1 = number 3
    - Index 2 = number 5
    - Index 3 = number 7, and so on...
  - **Sieve process:** For each prime $p$ in the sequence, mark all multiples of $p$ starting from $p^2$ as composite.
    - Use array slicing `is_prime[i*i//2::i] = False` to mark multiples efficiently.
  - **Extract primes:** Convert the boolean array back to actual prime numbers using `2*np.nonzero(is_prime)[0]+1`, then prepend 2 to get the complete prime list.

- **Step 2: Prime-Based Divisor Sum Function**
  - This is the key innovation: instead of checking divisibility by all candidates, we only trial divide by actual primes.
  - **Edge case:** For $n = 0$, return `float('inf')`.
  - **Prime factorization:** Iterate through the precomputed `primes` list and extract each prime factor:
    ```python
    index = 0
    f = primes[index]
    while f*f <= n:
        count = 0
        while not n%f:
            n //= f
            count += 1
        if count:
            answer *= (f**(count+1)-1)//(f-1)
        index += 1
        f = primes[index]
    ```
  - **Why only check primes?**
    - If $n$ is divisible by a composite number, it's already divisible by that composite's prime factors.
    - By only checking primes, we extract the prime factorization directly.
    - This eliminates redundant checks on composite numbers like 4, 6, 8, 9, 10, etc.
  - **Early termination:** Stop when $f^2 > n$ because any remaining $n > 1$ must be prime.
  - **Handle remaining prime:** If $n > 1$ after all trial divisions, then $n$ itself is a prime factor with exponent 1.
    - For a prime $p$: $\sigma(p) = p + 1$.
  - **Divisor formula:** Use $\sigma(n) = \prod_{i=1}^{k} \frac{p_i^{a_i+1} - 1}{p_i - 1}$ to compute the sum of all divisors.
  - **Return proper divisors:** Return $\sigma(n) - n$ to get the sum of proper divisors.
  - **Advantages over Solution 2's divisor function:**
    - Solution 2 explicitly handles 2 and 3, then uses wheel factorization for remaining candidates.
    - Solution 3 skips this entirely by only checking primes from the precomputed list.
    - Checking only primes is much faster than checking all candidates, especially for large numbers.

- **Step 3: Exclude Non-Amicable Numbers**
  - **Why exclude primes?** As proven rigorously in the Mathematical Foundation, no prime number can be amicable.
  - **Why exclude perfect numbers?** By definition, amicable pairs require two *distinct* numbers. Perfect numbers satisfy $d(n) = n$, making them incompatible with the amicable condition.
  - **The exclusion set:**
    ```python
    PN = [6, 28, 496, 8128]
    exclusion = set(PN)
    exclusion.add(2)
    ```
  - **Perfect numbers below 10,000:** There are exactly four: 6, 28, 496, and 8128. These are extraordinarily rare; as of 2024, only 51 perfect numbers are known, with the largest containing over 49 million digits.
  - **Why hardcode?** Rather than computing whether a number is perfect (which is non-trivial), we simply list the four known perfect numbers below our threshold. This is far more efficient than checking the mathematical condition $\sigma(n) = 2n$.
  - **Historical context:** Perfect numbers were studied by ancient mathematicians including Euclid. The known perfect numbers follow the Euclid-Euler form $2^{p-1}(2^p - 1)$ where $2^p - 1$ is a Mersenne prime. It remains an open question whether any odd perfect numbers exist.

- **Step 4: Main Loop with Intelligent Filtering**
  - Iterate through all numbers below threshold:
    ```python
    for a in range(threshold):
        if (a%2 and is_prime[a//2]) or a in exclusion:
            continue
    ```
  - **Condition breakdown:**
    - `a%2 and is_prime[a//2]`: Skip odd primes
      - `a%2` is true if $a$ is odd.
      - If odd and `is_prime[a//2]` is true, then $a$ is an odd prime => skip.
    - `a in exclusion`: Skip 2 and all perfect numbers.
  - **What passes through:**
    - All even numbers (including even composites like 220, 284, which form the smallest amicable pair)
    - All odd composite numbers
  - **Efficiency gain:** By skipping all primes and perfect numbers, we avoid computing $d(n)$ for numbers that mathematically cannot be amicable.

- **Step 5: Amicable Pair Detection**
  - For each number that passes the filter, compute `d_value = d(a)`.
  - **Condition 1:** `if d_value < a:`.
    - Ensure we count each pair exactly once by deferring to the larger element.
    - When the condition passes, both numbers are below threshold, so add both.
    - Verify with `d(d_value) == a` before adding.
  - **Condition 2:** `elif threshold <= d_value < float('inf'):`.
    - Handle cross-threshold pairs where one number exceeds the threshold.
    - Add only the number below threshold.
    - Verify with `d(d_value) == a` before adding.
  - **The boolean multiplication trick:** Use `int(condition)` to multiply by 0 or 1, avoiding explicit if statements.

- **Step 6: Why This Is Faster**
  - **Fewer divisor computations:** By skipping all odd primes and perfect numbers, we compute $d(n)$ for fewer candidates.
  - **Faster divisor computation:** Checking only primes is significantly faster than wheel factorization, especially for large numbers.
  - **Memory efficiency:** The half-sieve uses ~50% less memory than a full sieve.
  - **Combined effect:** Solution 3 is typically 2-5x faster than Solution 2, despite Solution 2 already being highly optimized.

- **Step 7: Memoization Cache Size Optimization**
  - The cache is set to `maxsize=threshold` (not `threshold+1`).
  - Since we skip many numbers (all odd primes, all perfect numbers), the actual cache usage is considerably less than the theoretical maximum.
  - This is a minor optimization that reflects the reduced number of unique `d(n)` values computed.

---

## Mathematical Foundation

### Sum of Divisors Function

The **divisor function** $\sigma(n)$ returns the sum of all positive divisors of $n$ (including $n$ itself). The **sum of proper divisors** is $d(n) = \sigma(n) - n$.

**Prime Factorization Formula:**
If $n = p_1^{a_1} \cdot p_2^{a_2} \cdots p_k^{a_k}$, then:
$$\sigma(n) = \prod_{i=1}^{k} \frac{p_i^{a_i+1} - 1}{p_i - 1}$$

This formula comes from the fact that each divisor of $n$ is formed by choosing an exponent between $0$ and $a_i$ for each prime $p_i$. The sum of all such choices for a single prime is a geometric series:
$$\sigma(p^a) = 1 + p + p^2 + \cdots + p^a = \frac{p^{a+1} - 1}{p - 1}$$

**Multiplicativity:**
The function $\sigma$ is **multiplicative**: if $\gcd(m, n) = 1$, then $\sigma(mn) = \sigma(m) \cdot \sigma(n)$.

### Amicable Numbers

**Definition:** Two distinct positive integers $a$ and $b$ form an **amicable pair** if:
- $d(a) = b$ and $d(b) = a$, where $a \neq b$.

**Examples:**
- $(220, 284)$: $d(220) = 284$ and $d(284) = 220$.
- $(1184, 1210)$: $d(1184) = 1210$ and $d(1210) = 1184$.
- $(2620, 2924)$: $d(2620) = 2924$ and $d(2924) = 2620$.
- $(5020, 5564)$: $d(5020) = 5564$ and $d(5564) = 5020$.
- $(6232, 6368)$: $d(6232) = 6368$ and $d(6368) = 6232$.

**Properties:**
- Amicable pairs are relatively rare. Under 10,000, there are only 5 pairs (10 numbers total).
- The smallest amicable pair $(220, 284)$ was known to the ancient Greeks (Pythagoras).
- Perfect numbers (where $d(n) = n$) are excluded from amicable numbers by the condition $a \neq b$.

### Why Prime Numbers Cannot Be Amicable

**Theorem:** No prime number can be part of an amicable pair.

**Proof by contradiction:**

Assume that a prime $p$ is part of an amicable pair with some positive integer $m$.

**Step 1: Determine the proper divisors of $p$**

Let $p$ be prime. By definition of a prime number, its only positive divisors are:
- $1$
- $p$

Therefore, the only *proper* divisor of $p$ is $1$.

**Step 2: Calculate $d(p)$**

The sum of proper divisors of $p$ is:
$$d(p) = 1$$

**Step 3: Apply the amicable condition**

If $p$ is amicable with $m$, then by definition:
$$d(p) = m$$

From Step 2, this means:
$$m = 1$$

**Step 4: Check the reverse condition**

For an amicable pair, we also require:
$$d(m) = p$$

Substituting $m = 1$:
$$d(1) = p$$

**Step 5: Calculate $d(1)$**

The number $1$ has no proper divisors (the only divisor of $1$ is $1$ itself, which is not a proper divisor). Therefore:
$$d(1) = 0$$

**Step 6: Derive the contradiction**

From Step 4, we need $d(1) = p$.

But from Step 5, $d(1) = 0$.

Therefore:
$$p = 0$$

This contradicts the assumption that $p$ is a prime number, since prime numbers are positive integers greater than $1$. QED

**Intuition:** Amicable pairs require a "feedback loop" where each number's divisors sum to the other. A prime is too simple: it has only divisor $1$, which forces its partner to be $1$. But $1$ has no divisors to feed back to the prime. The symmetry requirement cannot be satisfied.

### Why Perfect Numbers Cannot Be Amicable

**Theorem:** No perfect number can be part of an amicable pair.

**Proof by definition:**

**Definition:** A number $n$ is **perfect** if $d(n) = n$, i.e., $\sigma(n) = 2n$.

**Definition:** Two distinct positive integers $a$ and $b$ form an **amicable pair** if $d(a) = b$ and $d(b) = a$ where $a \neq b$.

**Argument:**

Suppose $n$ is perfect and is part of an amicable pair with some number $m$.

Then by the amicable condition:
- $d(n) = m$
- $d(m) = n$

But since $n$ is perfect:
- $d(n) = n$

Therefore:
$$m = n$$

However, the definition of amicable pairs explicitly requires $a \neq b$ (the two numbers must be distinct). Since $m = n$, this violates the definition.

Therefore, no perfect number can be part of an amicable pair. QED

**Consequence:** Perfect numbers are categorically excluded from amicable number problems, not by computational difficulty but by the fundamental definition of what makes a pair amicable.

### Perfect Numbers: Rarity, Structure, and the Hardcoded List

**Definition:** A number $n$ is **perfect** if $d(n) = n$, i.e., $\sigma(n) = 2n$.

**Known Perfect Numbers:**
There are exactly four perfect numbers below 10,000:
- $6 = 2^1(2^2 - 1)$
- $28 = 2^2(2^3 - 1)$
- $496 = 2^4(2^5 - 1)$
- $8128 = 2^6(2^7 - 1)$

**Why Hardcode Rather Than Compute?**

Rather than computing whether a number is perfect (checking if $\sigma(n) = 2n$, which requires computing all divisors), we simply hardcode the known perfect numbers below our threshold. This approach is justified because:

1. **Extreme rarity:** As of 2024, only **51 perfect numbers are known**. The next one after 8128 is 33,550,336, far exceeding typical algorithm thresholds.

2. **Exponential growth:** Known perfect numbers follow the Euclid-Euler form:
   $$P = 2^{p-1}(2^p - 1)$$
   where $2^p - 1$ is a Mersenne prime. The largest known perfect number has exponent $p = 82,589,933$, resulting in a number with over **49 million digits**. The gap between consecutive perfect numbers grows exponentially.

3. **Computational efficiency:** For a typical problem threshold (up to a few million), checking a hardcoded list of 4-5 elements is orders of magnitude faster than computing $\sigma(n)$ for each number.

4. **Mathematical certainty:** These are not estimates or probabilistic results, they are mathematically proven perfect numbers. There is zero ambiguity in using a hardcoded list.

5. **Problem structure:** Many Project Euler problems are designed with specific bounds (like 10,000 in this case) that are carefully chosen to be computationally feasible while still being interesting. With a threshold of 10,000
