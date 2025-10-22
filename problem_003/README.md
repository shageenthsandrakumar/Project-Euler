# Problem 3: Largest Prime Factor

**Problem source:** [Project Euler Problem 3](https://projecteuler.net/problem=3)

**Problem statement:**

The prime factors of $13195$ are $5, 7, 13$ and $29$.

What is the **largest prime factor** of the number $600851475143$?

## Solution 1: Trial Division

### Approach

  - Use **trial division** to find prime factors by testing all integers starting from $2$.
  - Divide $n$ by each candidate factor $f$ as many times as possible.
  - Track the largest factor found during the factorization process.
  - Continue until $f$ exceeds $n$ (which becomes smaller as factors are divided out).

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

  - **Step 1: Initialization**
      - Initialize `n = 600851475143` (the number to factorize).
      - Initialize `f = 2` (the first candidate factor).
      - Initialize `max_factor = 0` (to track the largest prime factor found).
  
  - **Step 2: Trial Division Loop**
      - The `while f <= n:` loop continues as long as the candidate factor doesn't exceed the remaining value of $n$.
      - For each candidate $f$, check if it divides $n$ using `if not n%f:`.
      - If $f$ divides $n$:
          - Update `max_factor = f` (since $f$ is a factor).
          - Divide out the factor: `n //= f`.
          - Continue testing the same $f$ (the loop doesn't increment yet) to remove all instances of this factor.
      - If $f$ does not divide $n$:
          - Increment to the next candidate: `f += 1`.
  
  - **Step 3: Final Result**
      - When the loop terminates, `max_factor` contains the largest prime factor encountered.

  - **Efficiency:** This is the least efficient solution. For the given input ($n \approx 6 \times 10^{11}$), this approach is impractical as it may test billions of candidates.
  
  - **Why it works:** Every composite factor is divided out as soon as it's found, so only prime factors are ever stored in `max_factor`. The algorithm terminates when $f > n$, but since $n$ is reduced with each factorization, this happens much sooner than testing all numbers up to the original value.

-----

## Solution 2: Optimized Trial Division

### Approach

  - Improve upon Solution 1 by **stopping early** when $f^2 > n$.
  - Once $f^2 > n$, if $n > 1$, then $n$ itself must be prime (the largest prime factor).
  - This optimization dramatically reduces the number of iterations needed.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

  - **Step 1: Initialization**
      - Initialize `n = 600851475143`, `f = 2`, and `max_factor = 0` (same as Solution 1).
  
  - **Step 2: Optimized Loop Condition**
      - The loop condition is now `while f*f <= n:` instead of `while f <= n:`.
      - This means we only test candidates up to $\sqrt{n}$.
      - **Why we can stop at $\sqrt{n}$:**
          - Suppose $n$ has a factor $f > \sqrt{n}$. Then $n = f * d$ for some integer $d$.
          - Since $f > \sqrt{n}$, we have $f * d > \sqrt{n} * d$, which means $n > \sqrt{n} * d$.
          - Dividing both sides by $\sqrt{n}$ gives us $\sqrt{n} > d$, so $d < \sqrt{n}$.
          - This means if there's a factor greater than $\sqrt{n}$, there must be a corresponding factor less than $\sqrt{n}$.
          - Therefore, we don't need to search beyond $\sqrt{n}$. All factors larger than $\sqrt{n}$ will have already been revealed by dividing out their smaller counterparts.
      - **Key insight:** Once all factors up to $\sqrt{n}$ are removed, any remaining $n > 1$ must be prime (and is the largest prime factor).
  
  - **Step 3: Factor Removal Strategy**
      - For each candidate $f$:
          - If $f$ divides $n$: divide it out (`n //= f`) and update `max_factor = f`.
          - If $f$ does not divide $n$: increment to the next candidate (`f += 1`).
  
  - **Step 4: Handle Remaining Prime**
      - After the loop, if `n > 1`, then $n$ itself is a prime factor (and the largest one).
      - Update `max_factor = n`.

  - **Efficiency:** This solution is vastly more efficient than Solution 1. For $n = 600851475143$, this means testing roughly $775{,}146$ candidates instead of $600$ billion.

-----

## Solution 3: Wheel Factorization

### Approach

  - Use **wheel factorization** to skip multiples of small primes ($2$ and $3$).
  - After handling $2$ and $3$ separately, only test candidates of the form $6k \pm 1$.
  - This optimization reduces the number of candidates by approximately $66\%$ compared to testing all odd numbers.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

  - **Step 1: Handle Small Primes Separately**
      - **Remove all factors of 2:**
          - `while not n%2:` divides out all factors of $2$.
          - Update `max_factor = 2` each time.
      - **Remove all factors of 3:**
          - `while not n%3:` divides out all factors of $3$.
          - Update `max_factor = 3` each time.
  
  - **Step 2: Wheel Factorization (6k±1 Pattern)**
      - After removing factors of $2$ and $3$, all remaining primes must be of the form $6k + 1$ or $6k - 1$ (i.e., $6k \pm 1$).
      - **Proof:** Any integer can be written as $6k$, $6k+1$, $6k+2$, $6k+3$, $6k+4$, or $6k+5$:
          - $6k$, $6k+2$, $6k+4$ are divisible by $2$.
          - $6k+3$ is divisible by $3$.
          - Only $6k+1$ and $6k+5$ (i.e., $6k-1$) can be prime (for $k \geq 1$).
      - The algorithm starts with `f = 5` and alternates between adding $2$ and $4$:
          - $5 \rightarrow 7$ (add $2$): covers $6(1)-1$ and $6(1)+1$.
          - $7 \rightarrow 11$ (add $4$): covers $6(1)+1$ and $6(2)-1$.
          - $11 \rightarrow 13$ (add $2$): covers $6(2)-1$ and $6(2)+1$.
          - And so on...
      - This pattern is implemented using a boolean toggle:
          - `f += 2+2*int(toggle)` adds $2$ when `toggle=False` and $4$ when `toggle=True`.
          - `toggle = not toggle` flips the toggle after each iteration.
  
  - **Step 3: Loop Termination**
      - The loop continues while `f*f <= n` (same as Solution 2).
      - For each candidate $f$, remove all instances: `while not n%f:`.
      - Update `max_factor = f` for each factor found.
  
  - **Step 4: Handle Remaining Prime**
      - After the loop, if `n > 1`, then $n$ is prime and is the largest factor.
      - Update `max_factor = n`.
    
  - **Efficiency:** This is the most efficient iterative solution. By skipping all multiples of $2$ and $3$, it tests only $\frac{1}{3}$ of the candidates compared to testing all integers, and $\frac{2}{3}$ of the candidates compared to testing all odd numbers.

-----

## Output

```
6857
```

-----

## Notes

  - The number $600851475143$ factors as $71 \times 839 \times 1471 \times 6857$, where all factors are prime.
  - **Solution 3** is the optimal solution among the three, offering the best performance through wheel factorization.
  - All three solutions correctly identify that after factoring out smaller primes, if a number greater than $1$ remains, it must be prime and therefore the largest prime factor.
  - The $\sqrt{n}$ optimization (Solutions 2 and 3) is crucial for making this problem computationally feasible, reducing the search space from $\sim 10^{11}$ to $\sim 10^6$ operations.
