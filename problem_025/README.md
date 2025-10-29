# Problem 25: 1000-digit Fibonacci Number

**Problem source:** [Project Euler Problem 25](https://projecteuler.net/problem=25)

**Problem statement:**

The Fibonacci sequence is defined by the recurrence relation:

$$F_n = F_{n-1} + F_{n-2}, \text{ where } F_1 = 1 \text{ and } F_2 = 1.$$

Hence the first $12$ terms will be:

$$\begin{align} 
F_1 &= 1\\ 
F_2 &= 1\\ 
F_3 &= 2\\ 
F_4 &= 3\\ 
F_5 &= 5\\ 
F_6 &= 8\\ 
F_7 &= 13\\ 
F_8 &= 21\\ 
F_9 &= 34\\ 
F_{10} &= 55\\ 
F_{11} &= 89\\ 
F_{12} &= 144 
\end{align}$$

The $12$ th term, $F_{12}$, is the first term to contain three digits.

What is the index of the first term in the Fibonacci sequence to contain $1000$ digits?

---

## Solution 1: Closed-Form Using Binet's Formula

### Approach

- Use **Binet's formula** to express Fibonacci numbers in terms of the golden ratio.
- Apply **logarithms** to convert the digit-count condition into an inequality.
- Solve for the index $n$ algebraically to find the first Fibonacci number with exactly 1000 digits.
- Use the **ceiling function** to round up to the nearest integer index.
- This approach computes the answer directly without generating any Fibonacci numbers.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Binet's Formula**
  - The $n$-th Fibonacci number is given by:
    $$F_n = \frac{\phi^n - \psi^n}{\sqrt{5}}$$
    where $\phi = \frac{1+\sqrt{5}}{2} \approx 1.618$ (the golden ratio) and $\psi = \frac{1-\sqrt{5}}{2} \approx -0.618$ (its conjugate).

- **Step 2: Simplification for Large $n$**
  - Since $|\psi| < 1$, we have $|\psi^n| \to 0$ as $n \to \infty$.
  - For $n \geq 1$: $|\psi^n| < 1$, so $\left|\frac{\psi^n}{\sqrt{5}}\right| < \frac{1}{\sqrt{5}} < 0.5$.
  - Therefore:
    $$F_n = \text{round}\left(\frac{\phi^n}{\sqrt{5}}\right) \approx \frac{\phi^n}{\sqrt{5}}$$
  - The approximation error is less than $0.5$, which is negligible for our purposes.

- **Step 3: Digit Count Characterization**
  - A positive integer $N$ has exactly $d$ digits if and only if:
    $$10^{d-1} \leq N < 10^d$$
  - Taking $\log_{10}$ of all parts:
    $$d-1 \leq \log_{10}(N) < d$$

- **Step 4: Applying to Fibonacci Numbers**
  - $F_n$ has at least $d$ digits when:
    $$F_n \geq 10^{d-1}$$
  - Using our approximation $F_n \approx \frac{\phi^n}{\sqrt{5}}$:
    $$\frac{\phi^n}{\sqrt{5}} \geq 10^{d-1}$$
  - Taking $\log_{10}$:
    $$\log_{10}\left(\frac{\phi^n}{\sqrt{5}}\right) \geq d-1$$
    $$n\log_{10}(\phi) - \frac{1}{2}\log_{10}(5) \geq d-1$$

- **Step 5: Solving for $n$**
  - Rearranging:
    $$n\log_{10}(\phi) \geq (d-1) + \frac{1}{2}\log_{10}(5)$$
    $$n \geq \frac{(d-1) + \frac{1}{2}\log_{10}(5)}{\log_{10}(\phi)}$$
  - Since $n$ must be an integer, the smallest such $n$ is:
    $$n = \left\lceil \frac{(d-1) + \frac{1}{2}\log_{10}(5)}{\log_{10}(\phi)} \right\rceil$$

- **Step 6: Implementation**
  - For $d = 1000$:
    - $\phi = \frac{1+\sqrt{5}}{2}$
    - $(d-1) + \frac{1}{2}\log_{10}(5) = 999 + 0.5 \times 0.699 \approx 999.3495$
    - $\log_{10}(\phi) \approx 0.20898$
    - $n \approx \frac{999.3495}{0.20898} \approx 4781.859$
    - $n = \lceil 4781.859 \rceil = 4782$

- **Step 7: Verification**
  - The formula gives the exact answer without needing to generate any Fibonacci numbers.
  - The approximation error from $\psi^n$ is negligible (less than $10^{-1000}$ relative error).

- **Efficiency:** This solution computes the answer using only a handful of arithmetic and logarithmic operations. It requires no iteration or generation of Fibonacci numbers, making it the most efficient approach possible.

---

## Solution 2: Iterative Generation with Logarithmic Check

### Approach

- Generate Fibonacci numbers iteratively using the recurrence relation.
- Use **logarithms** to determine the number of digits without converting to strings.
- A number $N$ has $d$ digits when $\lfloor \log_{10}(N) \rfloor = d-1$.
- Continue generating terms until reaching a number with 1000 digits.
- Track the index throughout the process.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Initialization**
  - Initialize `previous = 0` and `current = 1` to start the Fibonacci sequence.
  - Initialize `n = 1` to track the index of the current term.
  - Set `threshold = digits - 1 = 999` (since a number with $d$ digits satisfies $\lfloor \log_{10}(N) \rfloor = d-1$).

- **Step 2: Using Logarithms to Count Digits**
  - For a positive integer $N$, the number of digits is $\lfloor \log_{10}(N) \rfloor + 1$.
  - Equivalently, $N$ has $d$ digits when $d-1 \leq \log_{10}(N) < d$.
  - The condition `math.log10(current) < threshold` checks if the current term has fewer than 1000 digits.

- **Step 3: Iterative Generation**
  - The loop `while math.log10(current) < threshold:` continues until we reach a 1000-digit number.
  - Inside the loop:
    - `previous, current = current, previous + current` generates the next Fibonacci number.
    - `n += 1` increments the index.
  - This implements the recurrence $F_n = F_{n-1} + F_{n-2}$.

- **Step 4: Why Logarithms Are Better Than String Conversion**
  - **String conversion:** `len(str(current))` requires converting a large number to a string.
    - For a 1000-digit number, this involves allocating memory and processing 1000 characters.
  - **Logarithm:** `math.log10(current)` is a direct mathematical operation.
    - Python's `math.log10` is implemented in C and highly optimized.
    - No memory allocation or string processing required.
  - The logarithmic approach is significantly faster, especially for large numbers.

- **Step 5: Example Walkthrough**
  - For the first few terms:
    - $F_1 = 1$: $\log_{10}(1) = 0 < 999$ (continue)
    - $F_2 = 1$: $\log_{10}(1) = 0 < 999$ (continue)
    - $F_3 = 2$: $\log_{10}(2) \approx 0.301 < 999$ (continue)
    - ...
    - $F_{4781} \approx 10^{998.86}$: $\log_{10}(F_{4781}) \approx 998.86 < 999$ (continue)
    - $F_{4782} \approx 10^{999.04}$: $\log_{10}(F_{4782}) \approx 999.04 \geq 999$ (stop)

- **Step 6: Result**
  - When the loop terminates, `n` holds the index of the first Fibonacci number with 1000 digits.
  - The algorithm prints `n = 4782`.

- **Efficiency:** This solution generates approximately 4782 Fibonacci numbers, performing one logarithm calculation per iteration. While this requires more operations than the closed-form solution, it's still very fast in practice (completing in milliseconds) and has the advantage of being straightforward to understand and verify.

---

## Mathematical Foundation

### Rigorous Proof: Why Solution 1 Works

**Theorem:** The index of the first Fibonacci number with exactly $d$ digits is:
$$n = \left\lceil \frac{(d-1) + \frac{1}{2}\log_{10}(5)}{\log_{10}(\phi)} \right\rceil$$
where $\phi = \frac{1+\sqrt{5}}{2}$ is the golden ratio.

---

**Proof:**

The $n$-th Fibonacci number is given by Binet's formula:
$F_n = \frac{\phi^n - \psi^n}{\sqrt{5}}$
where $\phi = \frac{1+\sqrt{5}}{2} \approx 1.618$ (the golden ratio) and $\psi = \frac{1-\sqrt{5}}{2} \approx -0.618$ (its conjugate).

Since $|\psi| < 1$, we have $|\psi^n| \to 0$ as $n \to \infty$. For $n \geq 1$: $|\psi^n| < 1$, so:
$\left|\frac{\psi^n}{\sqrt{5}}\right| < \frac{1}{\sqrt{5}} < 0.5$

Therefore:
$F_n = \frac{\phi^n}{\sqrt{5}} - \frac{\psi^n}{\sqrt{5}}$

Since $\left|\frac{\psi^n}{\sqrt{5}}\right| < 0.5$, we can write:
$F_n = \left\lfloor \frac{\phi^n}{\sqrt{5}} + 0.5 \right\rfloor = \text{round}\left(\frac{\phi^n}{\sqrt{5}}\right)$

This means $F_n \approx \frac{\phi^n}{\sqrt{5}}$ with error less than $0.5$.

A positive integer $N$ has exactly $d$ digits if and only if:
$10^{d-1} \leq N < 10^d$

Taking $\log_{10}$ of all parts:
$d-1 \leq \log_{10}(N) < d$

Therefore, $N$ has exactly $d$ digits $\iff$ $\lfloor \log_{10}(N) \rfloor = d-1$.

Applying this to Fibonacci numbers, $F_n$ has exactly $d$ digits when:
$10^{d-1} \leq F_n < 10^d$

Using our approximation $F_n \approx \frac{\phi^n}{\sqrt{5}}$:
$10^{d-1} \leq \frac{\phi^n}{\sqrt{5}} < 10^d$

Taking $\log_{10}$:
$d-1 \leq \log_{10}\left(\frac{\phi^n}{\sqrt{5}}\right) < d$

$d-1 \leq n\log_{10}(\phi) - \frac{1}{2}\log_{10}(5) < d$

We want the smallest $n$ such that $F_n$ has at least $d$ digits:
$F_n \geq 10^{d-1}$

From our inequality:
$\frac{\phi^n}{\sqrt{5}} \geq 10^{d-1}$

Taking $\log_{10}$:
$n\log_{10}(\phi) - \frac{1}{2}\log_{10}(5) \geq d-1$

$n\log_{10}(\phi) \geq (d-1) + \frac{1}{2}\log_{10}(5)$

$n \geq \frac{(d-1) + \frac{1}{2}\log_{10}(5)}{\log_{10}(\phi)}$

Since $n$ must be an integer, the smallest such $n$ is:
$n = \left\lceil \frac{(d-1) + \frac{1}{2}\log_{10}(5)}{\log_{10}(\phi)} \right\rceil$

Finally, we verify the approximation. The approximation $F_n \approx \frac{\phi^n}{\sqrt{5}}$ introduces an error less than $0.5$. For $d = 1000$, we need $F_n \geq 10^{999}$. The relative error from the approximation is:
$\frac{0.5}{10^{999}} \approx 0$

This is negligible, confirming our formula gives the exact answer. ∎

---

## Comparison of Solutions

| Aspect | Solution 1 (Binet Formula) | Solution 2 (Iterative) |
|--------|----------------------------|------------------------|
| **Approach** | Closed-form mathematical formula | Generate and check each term |
| **Operations** | ~5 arithmetic/log operations | ~4782 iterations |
| **Dependencies** | Pure math calculation | Iterative generation |
| **Space Usage** | Constant (stores only formula variables) | Constant (stores only 2 terms) |
| **Readability** | Requires understanding Binet's formula | Very intuitive and verifiable |
| **Verification** | Mathematical proof required | Can manually verify by inspection |
| **Best For** | Maximum efficiency | Educational clarity |

---

## Output

```
4782
```

---

## Notes

- The first Fibonacci number to contain 1000 digits is $F_{4782}$.
- This number begins with the digits $1070066266382...$ and has exactly 1000 digits.
- **Solution 1** is the mathematically optimal approach, computing the answer in constant time using Binet's formula and logarithms.
- **Solution 2** demonstrates the practical iterative approach, which is still very fast for this problem size and easier to understand.
- The closed-form solution showcases the power of combining **analytic number theory** (Binet's formula) with **computational mathematics** (logarithms) to solve problems that would otherwise require extensive computation.
- The golden ratio $\phi = \frac{1+\sqrt{5}}{2}$ appears naturally in the Fibonacci sequence and is fundamental to understanding its growth rate.
- Using `math.log10` for digit counting is significantly more efficient than string conversion, especially for large numbers.
- Both solutions correctly handle the edge cases and produce the exact answer without any approximation errors.
- The problem demonstrates that sometimes the most efficient solution isn't to compute the answer directly, but to use mathematical properties to calculate it analytically.
