# Problem 14: Longest Collatz Sequence

**Problem source:** [Project Euler Problem 14](https://projecteuler.net/problem=14)

**Problem statement:**

The following iterative sequence is defined for the set of positive integers:

- $n \to n/2$ (if $n$ is even)
- $n \to 3n + 1$ (if $n$ is odd)

Using the rule above and starting with 13, we generate the following sequence:

$$13 \to 40 \to 20 \to 10 \to 5 \to 16 \to 8 \to 4 \to 2 \to 1$$

It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (the **Collatz conjecture**), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

**NOTE:** Once the chain starts, the terms are allowed to go above one million.

---

## The Collatz Conjecture: A Brief Digression

Before diving into solutions, it's worth appreciating the mathematical mystery at the heart of this problem.

### Why It's Fascinating

The Collatz conjecture is deceptively simple: take any positive integer, apply the rules above, and you'll eventually reach 1. Yet despite its simplicity, **no one has been able to prove this is true for all numbers**.

- **Tested extensively:** The conjecture has been verified computationally for all starting numbers up to approximately $2^{68}$ (about 295 quintillion).
- **Mathematically elusive:** Paul Erdős famously said, "Mathematics may not be ready for such problems."
- **Chaotic behavior:** Sequences exhibit unpredictable jumps, sometimes shooting far above the starting value before eventually descending.

### Terence Tao's Breakthrough (2019)

In 2019, mathematician Terence Tao made significant progress by proving that for "almost all" starting numbers (in a technical density sense), the Collatz sequence eventually reaches a value arbitrarily close to 1. However, this "almost all" result still leaves open the possibility of rare exceptions, and proving the sequence reaches exactly 1 for every number remains an open problem.

The work demonstrates how mathematicians tackle seemingly impossible problems by proving progressively weaker versions. Each step brings us closer to the full solution.

---

## Solution 1: Naive Recursion

### Approach

- Use **pure recursion** to compute the length of the Collatz sequence for each starting number.
- For each number from 1 to 999,999, calculate its sequence length from scratch.
- Track the starting number that produces the longest sequence.
- This solution directly translates the mathematical definition into code with no optimization.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Recursive Function Design**
  - The function `collatz_length(n)` computes the length of the sequence starting at `n`.
  - **Base case:** If `n == 1`, return `1` (the sequence ends).
  - **Recursive cases:**
    - If `n` is odd: `return 1 + collatz_length(3*n + 1)`
    - If `n` is even: `return 1 + collatz_length(n // 2)`
  - The `1 +` accounts for counting the current term in the sequence.
  - Using `n % 2` to check oddness: `n % 2` equals `1` for odd numbers, `0` for even.

- **Step 2: Exhaustive Search**
  - Loop through all starting numbers: `for i in range(1, 1000000):`
  - For each `i`, compute `c = collatz_length(i)`.
  - Track the maximum: if `max_length < c`, update both `max_length` and `start_number`.

- **Step 3: Why This Is Slow**
  - **Redundant computation:** When calculating the sequence for 100, we might compute: 100 → 50 → 25 → 76 → 38 → 19 → ...
  - Later, when we calculate the sequence for 200, we get: 200 → 100 → 50 → 25 → 76 → ...
  - The entire tail from 100 onward is recomputed unnecessarily.
  - This redundancy multiplies across hundreds of thousands of starting numbers.
  - **Deep recursion:** For long sequences, Python's call stack can grow very deep, though it doesn't exceed the default limit for this problem size.

- **Step 4: Runtime Analysis**
  - This solution is significantly slower than the optimized versions due to massive redundant computation.
  - The time taken grows with the number of starting values and the typical sequence lengths.
  - Most execution time is spent recomputing the same subsequences repeatedly.

- **Efficiency:** This is the least efficient solution but serves as a clear baseline. It demonstrates the problem without any optimization, making it easy to understand but impractical for larger limits.

---

## Solution 2: Memoized Recursion

### Approach

- Enhance Solution 1 by adding **memoization** (caching) to store previously computed sequence lengths.
- Use a dictionary to map each number to its sequence length.
- Before computing recursively, check if the result is already cached.
- This optimization transforms an exponential-time algorithm into one that computes each unique sequence length only once.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Cache Initialization**
  - Create a dictionary: `collatz_lengths = {1: 1}`
  - Pre-populate with the base case: the sequence starting at 1 has length 1.

- **Step 2: Enhanced Recursive Function**
  - Before computing, check the cache: `if n in collatz_lengths: return collatz_lengths[n]`
  - If found, return the cached value immediately (O(1) lookup).
  - If not found, compute recursively:
    - Calculate the next value using a branchless formula (see **Mathematical Foundation** for details).
    - Recursively get the length for that next value: `L = 1 + collatz_length(nxt)`
  - Store the result before returning: `collatz_lengths[n] = L`

- **Step 3: The Clever Math Trick**
  ```python
  nxt, is_odd = divmod(n, 2)
  nxt += is_odd * (5*nxt + 4)
  ```
  - This computes the next Collatz value without using explicit if-else branching.
  - `divmod(n, 2)` returns `(n//2, n%2)` in a single operation.
  - `nxt` initially holds `n//2`.
  - `is_odd` is `1` if n is odd, `0` if even.
  - The expression `is_odd * (5*nxt + 4)` evaluates to `0` for even numbers (no addition) or `5*nxt + 4` for odd numbers.
  - See **Mathematical Foundation** section for the algebraic proof of why this correctly computes both cases.

- **Step 4: Reverse Iteration**
  - The loop iterates backwards: `for i in range(1000000-1, 0, -1):`
  - **Why reverse?** Starting from larger numbers means when they eventually hit smaller numbers, those smaller numbers are likely already cached.
  - However, the performance benefit is marginal since the cache fills quickly regardless of iteration order.

- **Step 5: Cache Growth**
  - As the algorithm runs, the cache grows to contain hundreds of thousands of entries.
  - Each entry represents a unique number encountered during all sequence calculations.
  - Once cached, subsequent lookups are instant.

- **Step 6: Runtime Analysis**
  - This solution is dramatically faster than Solution 1, typically completing in seconds rather than minutes.
  - The speedup comes from eliminating redundant calculations through caching.
  - Each unique number's sequence length is computed exactly once.

- **Efficiency:** This is a dramatic improvement over Solution 1. By caching results, we transform the problem from recomputing overlapping sequences to computing each unique sequence segment once. This is the **dynamic programming** approach in action.

---

## Solution 3: Iterative with Batch Caching

### Approach

- Replace recursion with **iteration** to avoid potential stack overflow issues.
- Build the sequence iteratively until hitting a cached value.
- Store the entire path taken, then **backfill the cache** for all intermediate values.
- This approach is memory-efficient (temporary path storage) and stack-safe (no recursion).

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Iterative Sequence Building**
  - Initialize an empty list: `sequence = []`
  - Loop: `while n not in collatz_lengths:`
    - Append current `n` to the sequence.
    - Compute the next value using the branchless formula (see **Mathematical Foundation**).
    - Update `n` to the next value.
  - Exit the loop when `n` is found in the cache.

- **Step 2: Why This Works**
  - As we build the sequence, we're essentially following the Collatz path forward.
  - The moment we hit a number already in the cache, we know its length to reach 1.
  - We don't need to continue—we can use the cached value as our anchor point.

- **Step 3: Backfilling the Cache**
  - Once we hit a cached value `n`, we know `L = collatz_lengths[n]`.
  - Now traverse the stored `sequence` in reverse: `for num in reversed(sequence):`
    - Increment the length: `L += 1`
    - Cache this value: `collatz_lengths[num] = L`
  - **Example:** If we stored `[10, 5, 16, 8, 4, 2]` and hit cached `n=1` (length 1):
    - `2` gets length `2`
    - `4` gets length `3`
    - `8` gets length `4`
    - `16` gets length `5`
    - `5` gets length `6`
    - `10` gets length `7`

- **Step 4: Memory Efficiency**
  - The `sequence` list is temporary and cleared at the start of each iteration.
  - We only store intermediate values during computation, not permanently.
  - The cache itself grows as needed but stores only unique values encountered.

- **Step 5: Stack Safety**
  - Unlike Solution 2, this approach uses **no recursion**.
  - There's no risk of stack overflow, even for extremely long sequences.
  - For very large starting numbers (well beyond 1 million), this approach remains stable.

- **Step 6: Runtime Analysis**
  - This solution completes quickly, with performance comparable to Solution 2.
  - The iterative approach is slightly more explicit but performs similarly.
  - The main advantage is architectural: no recursion depth concerns.

- **Efficiency:** This solution combines the speed of memoization with the safety of iteration. It's the most robust approach, particularly suitable for scenarios where sequence lengths might be very large or the recursion limit is a concern.

---

## Mathematical Foundation

### The Collatz Sequence

For any positive integer $n$, the Collatz sequence is defined by:

$$
C(n) = \begin{cases}
n/2 & \text{if } n \text{ is even} \\
3n + 1 & \text{if } n \text{ is odd}
\end{cases}
$$

The sequence terminates when it reaches 1.

### Overlapping Subproblems

The key insight for optimization is that **Collatz sequences frequently intersect**.

**Example:**
- Starting at 10: $10 \to 5 \to 16 \to 8 \to 4 \to 2 \to 1$ (length 7)
- Starting at 20: $20 \to 10 \to 5 \to 16 \to 8 \to 4 \to 2 \to 1$ (length 8)

Once we compute the sequence from 10, we can reuse that information when computing from 20. This **overlapping subproblem** structure makes the problem ideal for dynamic programming.

### Why Dynamic Programming Works Here

**Dynamic programming** is applicable when a problem has:
1. **Optimal substructure:** The solution to a problem can be constructed from solutions to subproblems.
2. **Overlapping subproblems:** The same subproblems are solved multiple times.

The Collatz problem satisfies both:
- The length of a sequence starting at $n$ is $1 +$ the length starting at $C(n)$ (optimal substructure).
- Many starting numbers eventually reach the same intermediate values (overlapping subproblems).

By caching (memoizing) the length for each number we encounter, we ensure each sequence length is computed only once.

### The Branchless Computation Optimization

In Solutions 2 and 3, the next Collatz value is computed using:

```python
nxt, is_odd = divmod(n, 2)
nxt += is_odd * (5*nxt + 4)
```

This branchless formula eliminates the need for explicit if-else statements. Here's why it works:

**For even $n$:**
- $n = 2k$ for some integer $k$
- Next value should be: $n/2 = k$
- In code: `nxt = n//2`, `is_odd = 0`
- Addition term: `0 * (5*nxt + 4) = 0`
- Result: `nxt = k` ✓

**For odd $n$:**
- $n = 2k+1$ for some integer $k$ (where $k = \lfloor n/2 \rfloor$ in integer division)
- Next value should be: $3n+1 = 3(2k+1)+1 = 6k+4$
- In code: `nxt = k` initially, `is_odd = 1`
- Addition term: `1 * (5k + 4) = 5k + 4`
- Result: `nxt = k + 5k + 4 = 6k + 4 = 3n + 1$ ✓

**Performance benefit:** Branchless code can be faster than conditional statements, especially in tight loops, as it avoids potential branch misprediction penalties in the CPU pipeline. However, modern compilers and interpreters often optimize simple conditionals effectively, so the actual speedup may be minimal.

---

## Comparison of Solutions

| Aspect | Solution 1<br>(Naive Recursion) | Solution 2<br>(Memoized Recursion) | Solution 3<br>(Iterative Batch) |
|--------|--------------------------------|-----------------------------------|--------------------------------|
| **Approach** | Pure recursive computation | Recursive with caching | Iterative with path storage |
| **Caching** | None | Dictionary memoization | Dictionary + batch backfill |
| **Recursion** | Yes (deep) | Yes (shallow with cache) | No (loop-based) |
| **Runtime** | Very slow | Fast | Fast |
| **Stack Safety** | Limited by recursion depth | Better (cache reduces depth) | Excellent (no recursion) |
| **Memory** | Call stack only | Cache + call stack | Cache + temporary sequence |
| **Code Clarity** | ★★★★★ | ★★★★☆ | ★★★★☆ |
| **Optimization Level** | None | Dynamic programming | Dynamic programming |
| **Best For** | Understanding the problem | Good balance of speed/readability | Maximum robustness |

---

## Output

```
837799
```

---

## Notes

- The starting number under one million that produces the longest Collatz sequence is **837,799**, which generates a sequence of **525 terms**.
- **Solution 3** is the optimal choice for production code, offering excellent performance with guaranteed stack safety.
- **Solution 2** demonstrates the classic dynamic programming technique of memoization and is slightly more concise.
- **Solution 1** serves as an educational baseline, clearly showing the problem's structure before optimization.
- The dramatic performance difference between Solution 1 (very slow) and Solutions 2/3 (fast) illustrates the power of dynamic programming: by caching intermediate results, we reduce redundant computation by orders of magnitude.
- The problem demonstrates a fundamental computer science principle: when subproblems overlap, remember their solutions rather than recomputing them.
- Despite extensive computational verification, the Collatz conjecture remains unproven. This is a humbling reminder that some simple-looking problems can be extraordinarily deep.
- The sequence starting at 837,799 reaches a maximum value of 2,974,984 (well above one million) before eventually descending to 1, demonstrating the chaotic nature of Collatz sequences.
