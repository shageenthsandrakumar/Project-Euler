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
- Compute the final sum efficiently.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

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

## Solution 2

**Approach:**

- Iterate through all numbers from 1 up to (but not including) the threshold.
- Check if each number is a multiple of 3 or 5.
- If it is, add it to the running sum.
- This approach is straightforward but less efficient than the arithmetic series formula.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Iteration**  
  We loop through each number `n` from 1 up to `threshold - 1` to examine all candidates below the threshold.

- **Step 2: Check for multiples using modular arithmetic**  
  - `n % 3` computes the remainder when `n` is divided by 3.  
  - `n % 5` computes the remainder when `n` is divided by 5.  
  - If a number is a multiple of 3 or 5, at least one of these remainders is 0.  
  - The expression `n % 3 * n % 5` multiplies the remainders:  
    - If `n` is divisible by 3 or 5, at least one remainder is 0 → the product is 0.  
    - Using `not (n % 3 * n % 5)` evaluates to `True` when `n` is a multiple of 3 or 5.  

- **Step 3: Accumulating the sum**  
  When the condition is true, we add `n` to the running total sum.

- **Step 4: Result**  
  After the loop, the variable `sum` holds the sum of all multiples of 3 or 5 below the threshold.


## Output

```
233168
```

---

## Notes

- `threshold` can be changed to compute the sum below any upper limit.  
- Using the arithmetic series formula is faster and more efficient than iterating through all numbers.  




