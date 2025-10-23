# Problem 8: Largest Product in a Series

**Problem source:** [Project Euler Problem 8](https://projecteuler.net/problem=8)

**Problem statement:**

The four adjacent digits in the 1000-digit number that have the greatest product are $9 \times 9 \times 8 \times 9 = 5832$.

```
73167176531330624919225119674426574742355349194934
96983520312774506326239578318016984801869478851843
85861560789112949495459501737958331952853208805511
12540698747158523863050715693290963295227443043557
66896648950445244523161731856403098711121722383113
62229893423380308135336276614282806444486645238749
30358907296290491560440772390713810515859307960866
70172427121883998797908792274921901699720888093776
65727333001053367881220235421809751254540594752243
52584907711670556013604839586446706324415722155397
53697817977846174064955149290862569321978468622482
83972241375657056057490261407972968652414535100474
82166370484403199890008895243450658541227588666881
16427171479924442928230863465674813919123162824586
17866458359124566529476545682848912883142607690042
24219022671055626321111109370544217506941658960408
07198403850962455444362981230987879927244284909188
84580156166097919133875499200524063689912560717606
05886116467109405077541002256983155200055935729725
71636269561882670428252483600823257530420752963450
```

Find the thirteen adjacent digits in the 1000-digit number that have the greatest product. What is the value of this product?

---

## Solution 1: Zero-Segment Optimization with NumPy

### Approach

- Recognize that any product containing a zero equals zero, so only examine segments between zeros.
- Use NumPy to efficiently identify zero positions and calculate segment lengths.
- Filter segments that are long enough to contain 13 consecutive digits.
- Apply a sliding window within each valid segment to find the maximum product.
- Track the best product and its corresponding digits.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Initialization and Data Preparation**
  - Convert the 1000-digit string into a NumPy array of integers: `array = np.array([int(digit) for digit in number], dtype=np.int64)`.
  - Using `np.int64` ensures no overflow when computing products of 13 digits.
  - Initialize tracking variables:
    - `max_product = -1` (will store the largest product found)
    - `start_index = -1` and `end_index = -1` (will store positions of best digits)
    - `length = 13` (the window size)

- **Step 2: Identify Zero Positions**
  - Use `end_indices = np.where(array == 0)[0]` to find all positions where zeros occur.
  - These positions act as "boundaries" that divide the number into zero-free segments.
  - Example: If zeros are at positions [10, 25, 50], the segments are [0-9], [11-24], [26-49], [51-999].

- **Step 3: Calculate Segment Lengths**
  - Create `pre_indices = np.r_[-1, end_indices[:-1]]` to get the position before each zero.
    - `np.r_[-1, ...]` prepends -1 to handle the first segment (which starts at position 0).
    - `end_indices[:-1]` excludes the last zero to align arrays.
  - Compute segment lengths: `diff = end_indices - pre_indices`.
  - This gives the distance between consecutive zeros (length of each segment).

- **Step 4: Filter Valid Segments**
  - Use `good = np.where(diff > length)[0]` to find segments longer than 13 digits.
  - Only these segments can contain a valid 13-digit window.
  - Calculate starting positions: `start_indices = pre_indices + 1`.

- **Step 5: Calculate Window Counts**
  - For each valid segment, compute how many 13-digit windows fit inside it.
  - Formula: `extrass = end_indices - (start_indices + length - 1)`.
  - **Explanation:**
    - `start_indices + length - 1` gives the position of the last digit in the first window.
    - Subtracting this from `end_indices` (position of the zero) gives the number of additional windows.
    - Example: If a segment spans positions 0-29 (30 digits), it contains 30 - 13 + 1 = 18 windows.

- **Step 6: Sliding Window Within Each Segment**
  - For each valid segment (indexed by `index` in `good`):
    - `extras = extrass[index]` gives the number of windows to check.
    - `first_start = start_indices[index]` is the segment's starting position.
    - Inner loop: `for j in range(extras)`:
      - Calculate window start: `start = first_start + j`.
      - Compute product: `product = 1` then multiply all 13 digits using `for i in range(length)`.
      - Update maximum if this product is larger.

- **Step 7: Result Extraction**
  - After checking all segments, `max_product` contains the answer.
  - Extract the digits using slice notation: `number[start_index:end_index + 1]`.

- **Efficiency:** This approach is **highly optimized** compared to checking all 988 possible windows (1000 - 13 + 1). By skipping zero-containing windows, it dramatically reduces the number of products to compute. For the given input, this reduces computations by approximately 60-70%.

- **Why This Works:**
  - **Mathematical insight:** Any product containing a zero equals zero, so it can never be the maximum (unless all products are zero).
  - **Segmentation:** By dividing the number into zero-free segments, we guarantee that all products computed are non-zero.
  - **Efficiency gain:** Instead of computing ~988 products, we only compute products in segments between zeros.

---

## Solution 2: Sliding Window with Dynamic Product Updates

### Approach

- Use a **fixed-size sliding window** that moves through all digits from left to right.
- Maintain a running product (`current_product`) that is efficiently updated as the window slides.
- When adding a digit, multiply it into the product.
- When removing a digit:
  - If the digit is non-zero, divide it out (O(1) operation).
  - If the digit is zero, recalculate the product for the new window (O(13) operation).
- Track the maximum product and corresponding digits throughout the process.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Initialization**
  - Convert the string to a list of integers: `digits = [int(digit) for digit in number]`.
  - Initialize tracking variables:
    - `max_product = 0` (stores the largest product found)
    - `current_product = 1` (running product of the current window)
    - `left = 0` (left boundary of the sliding window)
    - `best_digits = []` (stores the digits that produce the maximum product)
  - Set `length = 13` (window size).

- **Step 2: Expanding the Window**
  - Loop through all positions: `for right in range(N)`.
  - The variable `right` represents the right boundary of the window.
  - Add the new digit to the window: `current_product *= digits[right]`.
  - This expands the window by one position to the right.

- **Step 3: Window at Target Size**
  - Check if the window has reached the desired size: `if right - left + 1 == length`.
  - Window size = (right position - left position + 1).
  - When the window is exactly 13 digits:
    - Compare with the maximum: `if current_product > max_product`.
    - Update the maximum and store the digits: `best_digits = digits[left:right + 1]`.

- **Step 4: Sliding the Window (Critical Logic)**
  - To move the window forward, remove the leftmost digit: `digit_to_remove = digits[left]`.
  - **Case 1: Non-zero digit removal**
    - If `digit_to_remove != 0`, simply divide it out: `current_product //= digit_to_remove`.
    - This is an O(1) operation (constant time).
    - **Why integer division?** We use `//` to maintain integer arithmetic and avoid floating-point precision issues.
  - **Case 2: Zero digit removal**
    - If `digit_to_remove == 0`, we cannot divide by zero.
    - Recalculate the product from scratch for the new window:
      ```python
      current_product = 1
      for k in range(left + 1, right + 1):
          current_product *= digits[k]
      ```
    - This loops through the 12 remaining digits in the window (O(13) operation).
  - Advance the left boundary: `left += 1`.

- **Step 5: Why This Approach is Efficient**
  - **Best case (no zeros):** Every window update is just a single multiplication and division.
  - **Worst case (many zeros):** Occasional recalculations when encountering zeros require multiplying 12-13 numbers.
  - **Average case:** For the given input (which has relatively few zeros), most updates are very fast.
  - This approach is **much faster** than recalculating the product from scratch for each window.

- **Step 6: Handling the Zero Problem Elegantly**
  - The algorithm doesn't skip windows containing zeros; it processes them naturally.
  - When a zero enters the window, the product becomes 0 (correctly).
  - When a zero exits the window, we recalculate (unavoidable, but infrequent).
  - This design ensures **correctness** while maintaining **efficiency**.

- **Efficiency:** This solution is very efficient in practice. In the best case (no zeros), it processes each digit once with simple multiplication and division operations. When zeros are encountered, it occasionally needs to recalculate the product for a window (multiplying 13 numbers), but these recalculations are infrequent. For the given input with approximately 1000 digits, this performs roughly 1000 operations with occasional recalculations.


---

## Comparison of Solutions

| Aspect | Solution 1 (Zero-Segment) | Solution 2 (Sliding Window) |
|--------|---------------------------|----------------------------|
| **Approach** | Skip zero-containing segments | Process all windows dynamically |
| **Dependencies** | Requires NumPy | Pure Python |
| **Complexity (Setup)** | More complex (segment calculation) | Simpler and more intuitive |
| **Complexity (Main Loop)** | Nested loops on valid segments | Single loop with conditional logic |
| **Speed** | Very fast for inputs with many zeros | Very fast for inputs with few zeros |
| **Space Usage** | Uses NumPy arrays | Uses Python lists |
| **Best For** | Inputs with many zeros | General purpose, fewer zeros |
| **Readability** | Requires NumPy knowledge | More readable for most programmers |

---

## Output

```
The greatest product of 13 adjacent digits is: 23514624000
The digits are: 5, 5, 7, 6, 6, 8, 9, 6, 6, 4, 8, 9, 5
```

---

## Notes

- The largest product of 13 consecutive digits in the 1000-digit number is $23{,}514{,}624{,}000 = 5 \times 5 \times 7 \times 6 \times 6 \times 8 \times 9 \times 6 \times 6 \times 4 \times 8 \times 9 \times 5$.
- **Solution 2** (Sliding Window) is generally more elegant and easier to understand, making it preferable for educational purposes and general use cases.
- **Solution 1** (Zero-Segment Optimization) demonstrates advanced array manipulation and is particularly effective when the input contains many zeros.
- Both solutions correctly handle the key challenge: avoiding unnecessary computation of products containing zeros.
- The sliding window technique with dynamic product updates is a classic algorithm design pattern applicable to many sequence processing problems.
- For further optimization, Solution 2 could be enhanced with a rolling product technique that detects zeros entering the window and skips ahead, but the current implementation is already efficient for most practical purposes.
