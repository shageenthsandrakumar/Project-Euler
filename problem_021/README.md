# Problem 21: Amicable Numbers

**Problem source:** [Project Euler Problem 21](https://projecteuler.net/problem=21)

**Problem statement:**

Let $d(n)$ be defined as the sum of proper divisors of $n$ (numbers less than $n$ which divide evenly into $n$).

If $d(a) = b$ and $d(b) = a$, where $a \neq b$, then $a$ and $b$ are called an **amicable pair** and each of $a$ and $b$ are called **amicable numbers**.

For example, the proper divisors of $220$ are $1, 2, 4, 5, 10, 11, 20, 22, 44, 55$ and $110$; therefore $d(220) = 284$. The proper divisors of $284$ are $1, 2, 4, 71$ and $142$; so $d(284) = 220$.

Evaluate the sum of all the amicable numbers under $10000$.

---

## Solution 1: Dictionary-Based Pair Tracking

### Approach

- Compute $d(n)$ for each number from $0$ to $9999$ using an efficient factorization algorithm with wheel factorization.
- Use a **dictionary** to track computed values and identify amicable pairs.
- For each number $a$, compute $d(a)$ and check if we've already seen a number $b$ where $d(b) = a$.
- If such a pair exists and $a \neq b$, we've found an amicable pair. Add both numbers to the sum.
- Store $d(a)$ in the dictionary for future lookups.
- This approach identifies each amicable pair exactly once by checking if the "reverse direction" has already been computed.

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
  - Loop through all numbers from $0$ to $9999$: `for a in range(threshold):`.
  - Compute `d_value = d(a)`.
  - **Check for amicable pair:**
    - Look up `d_values.get(d_value)`.
    - If this returns $a$ and $d\_value \neq a$, we've found an amicable pair.
    - **Why this works:** We previously computed `d(d_value) = a`, stored it in the dictionary, and now we've found `d(a) = d_value`.
    - This confirms that `d(a) = d_value` and `d(d_value) = a` with $a \neq d\_value$.
  - **Add both numbers:** When a pair is found, add `d_value + a` to the running sum.
    - This adds both members of the pair in a single operation.
  - **Store the current value:** If no pair is found, store `d_values[a] = d_value` for future lookups.

- **Step 4: Why This Avoids Double-Counting**
  - Each amicable pair $(a, b)$ with $a < b$ is counted exactly once:
    - When we process $a$: We compute $d(a) = b$, but $b$ hasn't been processed yet (since $a < b$), so `d_values.get(b)` returns `None`. We store `d_values[a] = b`.
    - When we process $b$: We compute $d(b) = a$. Now `d_values.get(a)` returns $b$ (which we stored earlier). Since $d(a) = b$ and $d(b) = a$ with $a \neq b$, we add both to the sum.
  - The pair is only counted when we reach the larger element $b$.

- **Step 5: Example Walkthrough (220, 284)**
  - When `a = 220`: Compute $d(220) = 284$. Check `d_values.get(284)` → not found (284 hasn't been processed). Store `d_values[220] = 284`.
  - When `a = 284`: Compute $d(284) = 220$. Check `d_values.get(220)` → returns $284$. Since $284 = 220$? No, but $d(220) = 284$ and $d(284) = 220$ with $220 \neq 284$, add $220 + 284 = 504$ to the sum.

- **Efficiency:** This solution processes each number from $0$ to $9999$ exactly once, computing its proper divisor sum using optimized factorization. The dictionary lookup is $O(1)$, making pair detection very fast. The wheel factorization reduces the number of trial divisions significantly compared to naive approaches.

---

## Solution 2: Memoized Function with Inequality Check

### Approach

- Use **memoization** to cache the results of $d(n)$ computations, avoiding redundant calculations.
- Apply the `@lru_cache` decorator to automatically store and retrieve previously computed values.
- For each number $a < 10000$, compute $d(a)$.
- **Optimization:** Only check for amicable pairs when $d(a) < a$.
  - This ensures each pair is counted exactly once when we reach the larger number.
- When $d(a) < a$, verify if $d(d(a)) = a$ (the defining property of amicable numbers).
- If verified, add both $a$ and $d(a)$ to the running sum.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Memoization with LRU Cache**
  - The `@lru_cache(maxsize=threshold+1)` decorator automatically caches function results.
  - **Cache size:** Set to `threshold + 1` (10,001) to store all possible values from $0$ to $10000$.
  - **How it works:** When `d(n)` is called:
    - If the result for $n$ is already cached, return it immediately (O(1) lookup).
    - Otherwise, compute the result, store it in the cache, and return it.
  - This is particularly beneficial because we call `d(d(a))` in the verification step, and `d(a)` was already computed and cached.

- **Step 2: The Divisor Sum Function**
  - Same implementation as Solution 1, using wheel factorization for efficiency.
  - Returns $\sigma(n) - n$, the sum of proper divisors.

- **Step 3: Main Loop with Inequality Optimization**
  - Loop through all numbers: `for a in range(threshold):`.
  - Compute `d_value = d(a)`.
  - **Key optimization:** `if d_value < a:`.
  - **Why this condition?**
    - For an amicable pair $(x, y)$ with $x < y$, we have two cases:
      - When processing $x$: $d(x) = y$ where $y > x$, so the condition fails and we skip the pair.
      - When processing $y$: $d(y) = x$ where $x < y$, so the condition passes and we check the pair.
    - This ensures each pair is examined exactly once, when we reach the larger element.
  - **Verification:** `if d(d_value) == a:`.
    - This checks if $d(d(a)) = a$, confirming the amicable relationship.
    - Thanks to memoization, `d(d_value)` is typically a cache hit, making this check very fast.
  - **Accumulate sum:** Use a clever multiplication trick: `amicable_sum += (d_value + a) * int(d(d_value) == a)`.
    - The expression `int(d(d_value) == a)` evaluates to $1$ if true, $0$ if false.
    - This avoids an explicit `if` statement, adding `d_value+a` only when the condition is met.
    - Multiplying by the boolean-as-integer is a compact way to conditionally add values.

- **Step 4: Why Memoization and Inequality Work Together**
  - **Cache hits maximize efficiency:**
    - When we process $a$ and compute $d(a)$, the result is cached.
    - When we later process $d(a)$ and need to compute $d(d(a))$, it's a cache hit.
    - This synergy is particularly powerful because $d(a) < a$ means we've already processed $d(a)$ earlier in the loop.
  - **Inequality prevents double-counting:**
    - By only acting when $d(a) < a$, we defer the check until we reach the larger number in the pair.
    - At that point, the smaller number's $d$ value is guaranteed to be cached.

- **Step 5: Example Walkthrough (220, 284)**
  - When `a = 220`: Compute $d(220) = 284$ (cached). Since $284 > 220$, condition fails.
  - When `a = 284`: Compute $d(284) = 220$ (cached). Since $220 < 284$, condition passes. Check $d(220)$ → cache hit returns $284$. Since $d(220) = 284 = a$, we add $220 + 284 = 504$.

- **Step 6: The Boolean Multiplication Trick**
  - Instead of writing:
    ```python
    if d(d_value) == a:
        amicable_sum += d_value + a
    ```
  - We write:
    ```python
    amicable_sum += (d_value + a) * int(d(d_value) == a)
    ```
  - This is more compact and eliminates a branch in the code, which can be marginally faster.
  - The expression `int(True)` evaluates to $1$, and `int(False)` evaluates to $0$.

- **Efficiency:** Memoization ensures that each unique value of $d(n)$ is computed at most once. The inequality check reduces the number of verification steps by half, and ensures that `d(d_value)` is almost always a cache hit. The combination makes this solution very fast in practice.

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

### Wheel Factorization (6k±1 Pattern)

After removing all factors of $2$ and $3$, any remaining prime must be of the form $6k \pm 1$.

**Proof:**
Any integer can be written as one of: $6k$, $6k+1$, $6k+2$, $6k+3$, $6k+4$, $6k+5$.
- $6k$, $6k+2$, $6k+4$ are divisible by $2$.
- $6k+3$ is divisible by $3$.
- Only $6k+1$ and $6k+5$ (i.e., $6k-1$) can be prime (for $k \geq 1$).

The alternating step pattern (2, 4, 2, 4, ...) efficiently generates all numbers of this form:
- Start at $5 = 6(1) - 1$, add $2$ → $7 = 6(1) + 1$
- Add $4$ → $11 = 6(2) - 1$, add $2$ → $13 = 6(2) + 1$
- Add $4$ → $17 = 6(3) - 1$, and so on...

This reduces the search space by approximately $66\%$ compared to checking all numbers.

---

## Comparison of Solutions

| Aspect | Solution 1 (Dictionary) | Solution 2 (Memoization + Inequality) |
|--------|-------------------------|---------------------------------------|
| **Approach** | Track pairs with dictionary | Cache with inequality optimization |
| **Caching** | Manual dictionary storage | Automatic with `@lru_cache` |
| **Pair Detection** | Check if reverse exists in dict | Check $d(a) < a$ then verify |
| **Cache Efficiency** | Stores only processed values | Stores all computed values |
| **Double-Counting Prevention** | Dictionary lookup logic | Inequality condition |
| **Code Clarity** | ★★★★☆ | ★★★★★ |
| **Speed** | Very fast | Very fast |
| **Best For** | Explicit pair tracking | Clean, Pythonic solution |

---

## Output

```
31626
```

---

## Notes

- The sum of all amicable numbers under 10,000 is **31,626**.
- There are exactly **10 amicable numbers** below 10,000, forming **5 amicable pairs**:
  - $(220, 284)$ → sum: $504$
  - $(1184, 1210)$ → sum: $2394$
  - $(2620, 2924)$ → sum: $5544$
  - $(5020, 5564)$ → sum: $10584$
  - $(6232, 6368)$ → sum: $12600$
  - **Total:** $504 + 2394 + 5544 + 10584 + 12600 = 31626$
- **Solution 2** is the more elegant approach, using Python's built-in memoization and a clean inequality check.
- **Solution 1** provides more explicit control over pair tracking and may be easier to understand for those unfamiliar with decorators.
- The wheel factorization optimization (checking only $6k \pm 1$ candidates) provides significant speedup over naive trial division.
- Both solutions correctly handle the edge case of $n = 0$ by returning `float('inf')`, though this doesn't affect the problem since we only check $n \geq 1$.
- The inequality optimization ($d(a) < a$) is mathematically elegant: it ensures each pair is counted exactly once by deferring the check until we reach the larger element, at which point the smaller element's value is guaranteed to be cached.
- Perfect numbers (where $d(n) = n$) are automatically excluded by the condition $a \neq b$ (or $d\_value \neq a$).
- The problem demonstrates the power of combining efficient algorithms (wheel factorization), mathematical properties (multiplicativity of $\sigma$), and programming techniques (memoization, dictionary lookups) to solve number theory problems efficiently.
