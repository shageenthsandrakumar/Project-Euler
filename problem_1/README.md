# Problem 1: Multiples of 3 and 5

**Problem source:** [Project Euler Problem 1](https://projecteuler.net/problem=1)

**Problem statement:**  
If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6, and 9. The sum of these multiples is 23.  

Find the sum of all the multiples of 3 or 5 below 1000.

---

## Solution 1

### Approach

- Count the number of multiples of 3, 5, and 15 below the threshold.  
- Use the arithmetic series formula to calculate the sum of each set of multiples:  
  - sum_of_multiples = step * n * (n + 1) / 2  
  - Here, `step` is 3, 5, or 15, and `n` is the number of terms.  
- Correct for double-counting by subtracting the sum of multiples of 15.  
- Compute the final sum efficiently:


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




