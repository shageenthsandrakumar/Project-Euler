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
- Use the arithmetic series formula to calculate the sum of each set of multiples:  
  - sum_of_multiples = step * n * (n + 1) / 2  
  - Here, `step` is 3, 5, or 15, and `n` is the number of terms.  
- Correct for double-counting by subtracting the sum of multiples of 15.  
- Compute the final sum efficiently:

```python
final_sum = sum_of_3s + sum_of_5s - sum_of_15s
