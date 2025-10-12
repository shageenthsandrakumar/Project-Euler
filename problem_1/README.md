# Problem 1: Multiples of 3 and 5

**Problem source:** [Project Euler Problem 1](https://projecteuler.net/problem=1)

**Problem statement:**  
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6, and 9. The sum of these multiples is 23.  

Find the sum of all the multiples of 3 or 5 below 1000.

---

## Solution 1

### Approach

1. **Count the number of multiples below the threshold**  

```
number_of_3s  = (threshold - 1) // 3
number_of_5s  = (threshold - 1) // 5
number_of_15s = (threshold - 1) // 15
```

2. **Compute the sum of each arithmetic series**  

```
sum_of_3s  = 3 * number_of_3s  * (number_of_3s  + 1) // 2
sum_of_5s  = 5 * number_of_5s  * (number_of_5s  + 1) // 2
sum_of_15s = 15 * number_of_15s * (number_of_15s + 1) // 2
```

3. **Calculate the final sum**  

```
final_sum = sum_of_3s + sum_of_5s - sum_of_15s
```

**Why subtract multiples of 15?**  
Multiples of both 3 and 5 (i.e., multiples of 15) are counted twice when summing multiples of 3 and 5 individually. Subtracting their sum once ensures each number is counted exactly once.

---

### Full Python Code

```python
# Problem 1: Multiples of 3 and 5
threshold = 1000

# Count the number of multiples below threshold
number_of_3s = (threshold - 1) // 3
number_of_5s = (threshold - 1) // 5
number_of_15s = (threshold - 1) // 15

# Calculate sum of multiples using arithmetic series formula
sum_of_3s = 3 * number_of_3s * (number_of_3s + 1) // 2
sum_of_5s = 5 * number_of_5s * (number_of_5s + 1) // 2
sum_of_15s = 15 * number_of_15s * (number_of_15s + 1) // 2

# Compute final sum
final_sum = sum_of_3s + sum_of_5s - sum_of_15s
print(final_sum)
```

---

### Detailed Explanation

- **Step 1: Counting multiples**  
  `(threshold - 1) // n` gives the number of multiples of `n` below the threshold. Subtracting 1 ensures we stay strictly below the threshold.

- **Step 2: Sum of arithmetic series**  
  The sum of the first `n` multiples of `k` is:

```
k + 2k + 3k + ... + nk = k * (1 + 2 + 3 + ... + n) = k * n * (n + 1) / 2
```

- **Step 3: Correct for double-counting**  
  Numbers divisible by both 3 and 5 are multiples of 15. Summing multiples of 3 and multiples of 5 individually counts them twice. Subtracting the sum of multiples of 15 corrects this.

- **Step 4: Compute final sum**  
  `final_sum = sum_of_3s + sum_of_5s - sum_of_15s` produces the correct total sum efficiently.

---

### Example Calculation (threshold = 1000)

- Multiples of 3: 3, 6, 9, … , 999 → n_3 = 333 → sum = 166833  
- Multiples of 5: 5, 10, 15, … , 995 → n_5 = 199 → sum = 99500  
- Multiples of 15: 15, 30, 45, … , 990 → n_15 = 66 → sum = 33165  

Final sum: `166833 + 99500 - 33165 = 233168`

---

### Output

```
233168
```

---

### Notes

- `threshold` can be changed to compute the sum below any upper limit.  
- Using the arithmetic series formula is faster and more efficient than iterating through all numbers.  
- This README fully explains the problem, approach, code, example, and reasoning, making it portfolio-ready for employers.  
- Future solutions for Problem 1 can be added as `solution_2.py`, `solution_3.py`, etc.



