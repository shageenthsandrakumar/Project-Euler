# Problem 1: Multiples of 3 and 5

**Problem statement:**  
Find the sum of all multiples of 3 or 5 below a given threshold (default 1000).

---

## Solution 1 (`solution1.py`)

**Approach:**  

- Count the number of multiples of 3, 5, and 15 below the threshold.  
- Use the arithmetic series formula to calculate the sum of each set of multiples.  
- Correct for double-counting by subtracting the sum of multiples of 15.  
- Compute the final sum efficiently:

```python
final_sum = sum_of_3s + sum_of_5s - sum_of_15s
