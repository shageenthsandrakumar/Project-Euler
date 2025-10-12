# Project Euler Solutions

This repository contains my Python solutions to Project Euler problems. Each problem may have multiple solutions exploring different mathematical or algorithmic approaches. The goal is to understand the reasoning behind each method and compare their efficiency and simplicity.

---

# Problem 1: Multiples of 3 and 5

**Problem source:** [Project Euler Problem 1](https://projecteuler.net/problem=1)

**Problem statement:**  
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6, and 9. The sum of these multiples is 23.  

Find the sum of all the multiples of 3 or 5 below 1000.

---

## Solution 1 (`solution_1.py`)

**Approach:**  

- Count the number of multiples of 3, 5, and 15 below the threshold.  
- Use the arithmetic series formula to calculate the sum of each set of multiples.  
- Correct for double-counting by subtracting the sum of multiples of 15.  
- Compute the final sum efficiently.

**Why subtract multiples of 15?**  
Numbers divisible by both 3 and 5 are counted twice when summing multiples of 3 and 5 separately. Subtracting the sum of multiples of 15 ensures each number is counted **exactly once**.

---

### Detailed Explanation of Why This Works

The formula for the sum of an arithmetic series is:  

\[
\text{Sum} = n \cdot \frac{first + last}{2} = \frac{n(n+1)}{2} \cdot step
\]

Where:  

- \(n\) is the number of terms  
- \(step\) is the difference between consecutive terms (3, 5, or 15 here)  

For multiples of 3 below 1000:  

\[
n_3 = \left\lfloor \frac{999}{3} \right\rfloor = 333
\]  
\[
\text{Sum of 3s} = 3 \cdot \frac{333 \cdot 334}{2} = 166833
\]

For multiples of 5 below 1000:  

\[
n_5 = \left\lfloor \frac{999}{5} \right\rfloor = 199
\]  
\[
\text{Sum of 5s} = 5 \cdot \frac{199 \cdot 200}{2} = 99500
\]

For multiples of 15 below 1000 (double-count correction):  

\[
n_{15} = \left\lfloor \frac{999}{15} \right\rfloor = 66
\]  
\[
\text{Sum of 15s} = 15 \cdot \frac{66 \cdot 67}{2} = 33165
\]

Final sum:  

\[
166833 + 99500 - 33165 = 233168
\]

This avoids iterating through all numbers from 1 to 999, making the solution **efficient and elegant**.

---

### Key calculation snippet

```python
# Core calculation
final_sum = sum_of_3s + sum_of_5s - sum_of_15s
