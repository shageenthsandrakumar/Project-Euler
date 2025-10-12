# Project Euler Solutions

This repository contains my Python solutions to Project Euler problems. Each problem may have multiple solutions exploring different mathematical or algorithmic approaches. The goal is to understand the reasoning behind each method and compare efficiency and simplicity.

---

## Problem 1: Multiples of 3 and 5

**Problem statement:**  
Find the sum of all multiples of 3 or 5 below a given threshold (default 1000).

---

### Solution 1 (`Problem1_solution_1.py`)

**Approach:**  

1. Count the number of multiples below the threshold for 3, 5, and 15.  
2. Use the formula for the sum of an arithmetic series to calculate:  
   - Sum of multiples of 3  
   - Sum of multiples of 5  
   - Sum of multiples of 15 (to correct for double-counting)  
3. Calculate the final sum as:

```python
final_sum = sum_of_3s + sum_of_5s - sum_of_15s
