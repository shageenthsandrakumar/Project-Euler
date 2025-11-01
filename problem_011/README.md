# Problem 11: Largest Product in a Grid

**Problem source:** [Project Euler Problem 11](https://projecteuler.net/problem=11)

**Problem statement:**

In the 20×20 grid below, four numbers along a diagonal line have been marked in red.

```
08 02 22 97 38 15 00 40 00 75 04 05 07 78 52 12 50 77 91 08
49 49 99 40 17 81 18 57 60 87 17 40 98 43 69 48 04 56 62 00
81 49 31 73 55 79 14 29 93 71 40 67 53 88 30 03 49 13 36 65
52 70 95 23 04 60 11 42 69 24 68 56 01 32 56 71 37 02 36 91
22 31 16 71 51 67 63 89 41 92 36 54 22 40 40 28 66 33 13 80
24 47 32 60 99 03 45 02 44 75 33 53 78 36 84 20 35 17 12 50
32 98 81 28 64 23 67 10 26 38 40 67 59 54 70 66 18 38 64 70
67 26 20 68 02 62 12 20 95 63 94 39 63 08 40 91 66 49 94 21
24 55 58 05 66 73 99 26 97 17 78 78 96 83 14 88 34 89 63 72
21 36 23 09 75 00 76 44 20 45 35 14 00 61 33 97 34 31 33 95
78 17 53 28 22 75 31 67 15 94 03 80 04 62 16 14 09 53 56 92
16 39 05 42 96 35 31 47 55 58 88 24 00 17 54 24 36 29 85 57
86 56 00 48 35 71 89 07 05 44 44 37 44 60 21 58 51 54 17 58
19 80 81 68 05 94 47 69 28 73 92 13 86 52 17 77 04 89 55 40
04 52 08 83 97 35 99 16 07 97 57 32 16 26 26 79 33 27 98 66
88 36 68 87 57 62 20 72 03 46 33 67 46 55 12 32 63 93 53 69
04 42 16 73 38 25 39 11 24 94 72 18 08 46 29 32 40 62 76 36
20 69 36 41 72 30 23 88 34 62 99 69 82 67 59 85 74 04 36 16
20 73 35 29 78 31 90 01 74 31 49 71 48 86 81 16 23 57 05 54
01 70 54 71 83 51 54 69 16 92 33 48 61 43 52 01 89 19 67 48
```

The product of these numbers is $26 \times 63 \times 78 \times 14 = 1788696$.

What is the greatest product of four adjacent numbers in the same direction (up, down, left, right, or diagonally) in the 20×20 grid?

---

## Generalization and Input Validation

All three solutions are designed to be **fully generalizable** beyond the specific problem parameters. The key parameters are:

- **`grid_size`:** The dimension of the square grid (20 in this problem, but can be any size).
- **`adj_size`:** The number of adjacent elements to multiply together (4 in this problem, but fully configurable).

### Input Validation

All three solutions implement a **critical validation check** to ensure the parameters are valid:

```python
class CustomError(Exception):
    pass

if adj_size <= 0 or adj_size > grid_size or not isinstance(adj_size, int):
    raise CustomError("Not a valid adj_size. It must be a positive integer less than the grid size")
```

This validation enforces three essential constraints:
1. **Positive adjacency:** `adj_size > 0` ensures we're multiplying at least one number.
2. **Feasibility:** `adj_size <= grid_size` ensures the adjacency length fits within the grid dimensions.
3. **Integer constraint:** `isinstance(adj_size, int)` prevents floating-point or invalid types.

**Why this matters:** Without validation, invalid parameters could cause:
- **Index errors:** Attempting to access non-existent grid positions.
- **Infinite loops:** Negative values causing range errors.
- **Logical errors:** Non-integer values producing unexpected behavior.

This defensive programming practice ensures the solutions are robust and provide clear error messages when misused.

---

## Solution 1: Index-Swapping Loop Optimization

### Approach

- Use a **clever index-swapping technique** to check horizontal, vertical, and both diagonal directions simultaneously.
- Iterate through valid starting positions where `adj_size` adjacent numbers can fit.
- For each position, compute products in all four directions using compact loop logic.
- Track the maximum product found across all directions.
- **Fully generalizable:** Works for any `grid_size` and `adj_size` combination.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Initialization and Input Validation**
  - Parse the grid string into a 2D list: `Matrix = [list(map(int, line.split())) for line in grid.splitlines()]`.
  - Define `grid_size = 20` and `adj_size = 4` (both fully configurable).
  - **Validate parameters** using the custom error check described above.
  - This ensures the algorithm only runs with valid, safe parameters.

- **Step 2: Loop Structure and Boundary Handling**
  - **Outer loop:** `for i in range(grid_size - adj_size + 1)`:
    - This range ensures we can fit `adj_size` consecutive numbers starting at position `i`.
    - For `grid_size=20` and `adj_size=4`: iterates from 0 to 16 (17 positions).
    - General formula: last valid starting position is `grid_size - adj_size`.
  - **Inner loop:** `for j in range(grid_size)` iterates through all positions.
    - Not all positions are valid for all directions (handled with conditionals).

- **Step 3: The Index-Swapping Technique**
  - **Vertical products:** `product_y *= Matrix[i+a][j]`
    - Fixed column `j`, varying rows from `i` to `i+adj_size-1`.
  - **Horizontal products:** `product_x *= Matrix[j][i+a]`
    - Fixed row `j`, varying columns from `i` to `i+adj_size-1`.
    - **Key insight:** By swapping `i` and `j` indices, we avoid writing separate loops for horizontal direction.
  - This symmetry exploitation is the elegant core of this solution.

- **Step 4: Diagonal Products with Boundary Checks**
  - **Down-right diagonals (↘):**
    - Condition: `if j <= grid_size - adj_size` ensures we have space for `adj_size` diagonal elements.
    - Product: `product_dr *= Matrix[i+a][j+a]` for `a` in `range(adj_size)`.
    - Both row and column indices increase together.
    - **General form:** Starting at `(i, j)`, elements are at positions `(i+a, j+a)` for `a = 0, 1, ..., adj_size-1`.
  
  - **Down-left diagonals (↙):**
    - Condition: `if j >= adj_size - 1` ensures column index remains valid when decreasing.
    - Product: `product_dl *= Matrix[i+a][j-a]` for `a` in `range(adj_size)`.
    - Row increases, column decreases.
    - **General form:** Starting at `(i, j)`, elements are at positions `(i+a, j-a)` for `a = 0, 1, ..., adj_size-1`.

- **Step 5: Computing Products**
  - For each position, initialize products to 1: `product_x`, `product_y`, `product_dr`, `product_dl`.
  - Loop through adjacent positions: `for a in range(adj_size)`.
  - Multiply the appropriate matrix elements for each direction.
  - Update the maximum: `max_product = max(max_product, product_x, product_y, product_dr, product_dl)`.

- **Step 6: Why This Generalization Works**
  - The outer loop bound `grid_size - adj_size + 1` automatically adjusts to any adjacency length.
  - Diagonal boundary checks `j <= grid_size - adj_size` and `j >= adj_size - 1` scale with `adj_size`.
  - The inner product loops `for a in range(adj_size)` work for any adjacency length.
  - **Example:** For `adj_size=6` on a 30×30 grid, the algorithm would find products of 6 consecutive elements.

- **Efficiency:** This solution is clean and efficient. It checks all valid `adj_size`-element sequences in all four directions with minimal code duplication. The index-swapping technique eliminates the need for separate horizontal/vertical loops, demonstrating elegant algorithm design.

---

## Solution 2: NumPy Sliding Window with Diagonal Extraction

### Approach

- Use **NumPy's `sliding_window_view`** for efficient horizontal and vertical product computation.
- Extract diagonals using **`np.diagonal`** with different offsets to get all diagonal lines.
- Apply sliding windows to each diagonal to compute products of `adj_size` consecutive elements.
- Leverage NumPy's vectorized operations for maximum performance.
- **Fully generalizable:** Automatically adapts to any `grid_size` and `adj_size`.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: NumPy Array Conversion and Validation**
  - Convert the grid to a NumPy array: `Matrix = np.array([line.split() for line in grid_str.splitlines()], dtype=int)`.
  - Extract `grid_size = len(Matrix)` dynamically from the input.
  - Define `adj_size` (configurable parameter).
  - **Apply input validation** to ensure parameters are valid before processing.

- **Step 2: Horizontal Products with Sliding Windows**
  - Create sliding windows: `np.lib.stride_tricks.sliding_window_view(Matrix, (1, adj_size))`.
  - **Window shape:** `(1, adj_size)` means 1 row and `adj_size` columns.
  - This creates all possible 1×`adj_size` horizontal windows in the grid.
  - Compute products: `np.prod(..., axis=-1)` multiplies along the last axis (the `adj_size` elements).
  - Result shape: `(grid_size, grid_size - adj_size + 1)`.
  - **Generalization:** For `adj_size=5` on a 25×25 grid, this would create 25×21 windows.

- **Step 3: Vertical Products with Sliding Windows**
  - Create sliding windows: `np.lib.stride_tricks.sliding_window_view(Matrix, (adj_size, 1))`.
  - **Window shape:** `(adj_size, 1)` means `adj_size` rows and 1 column.
  - Compute products: `np.prod(..., axis=-2)` multiplies along the row axis.
  - Result shape: `(grid_size - adj_size + 1, grid_size)`.
  - **Generalization:** Window size automatically scales with `adj_size`.

- **Step 4: Diagonal Extraction Logic**
  - **Understanding `np.diagonal(Matrix, offset=k)`:**
    - `offset=0` gives the main diagonal: elements where row index equals column index.
    - `offset=1` gives the diagonal one step above the main diagonal.
    - `offset=-1` gives the diagonal one step below the main diagonal.
    - **General range:** `offset` from `-(grid_size - adj_size)` to `(grid_size - adj_size)` covers all diagonals with at least `adj_size` elements.

- **Step 5: Down-Right Diagonals**
  - Loop through offsets: `for offset in range(adj_size - grid_size, grid_size - adj_size + 1)`.
  - This range ensures we only process diagonals long enough to contain `adj_size` elements.
  - Extract diagonal: `diag = np.diagonal(Matrix, offset=offset)`.
  - Filter valid diagonals: `if len(diag) >= adj_size` ensures at least `adj_size` elements.
  - Apply sliding window to the diagonal: `np.lib.stride_tricks.sliding_window_view(diag, adj_size)`.
  - Compute products: `np.prod(..., axis=1)` gives products of each `adj_size`-element window.
  - Collect all products: `dr_products.extend(...)`.
  - **Generalization:** For `adj_size=7`, only diagonals with ≥7 elements are processed.

- **Step 6: Down-Left Diagonals**
  - Flip the matrix horizontally: `flipped = np.fliplr(Matrix)`.
  - **Why flipping works:** Down-left diagonals (↙) in the original matrix become down-right diagonals (↘) in the flipped matrix.
  - Apply the same diagonal extraction logic as down-right diagonals.
  - This elegant trick avoids writing separate down-left diagonal code.
  - **Generalization:** Works for any grid size and adjacency length.

- **Step 7: Finding the Maximum**
  - Compute maximums from each direction:
    - `horizontal.max()` — maximum horizontal product.
    - `vertical.max()` — maximum vertical product.
    - `max(dr_products)` — maximum down-right diagonal product.
    - `max(dl_products)` — maximum down-left diagonal product.
  - Take the overall maximum: `max(...)` across all four values.

- **Efficiency:** This solution leverages NumPy's highly optimized C implementations. The sliding window view creates efficient memory views without copying data. Vectorized operations eliminate Python loops, making this approach very fast for large grids. The generalization works seamlessly—changing `adj_size` from 4 to 10 requires only modifying one variable.

---

## Solution 3: Scipy Signal Processing with Matrix Skewing

### Approach

- Transform the problem into a **2D convolution** task using signal processing techniques.
- Convert products to sums using **logarithms**: $\log(a \times b \times c) = \log(a) + \log(b) + \log(c)$.
- Apply **`signal.correlate2d`** with kernels of size `adj_size` for horizontal and vertical directions.
- Use **matrix skewing** to transform diagonals into columns, enabling vertical convolution.
- Handle zeros in the grid by replacing them before taking logarithms.
- **Fully generalizable:** Kernel sizes and padding automatically scale with `adj_size`.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Input Validation and Zero Handling**
  - **Validate parameters** using the custom error check to ensure safety.
  - Some grid values are 0, which creates problems: $\log(0)$ is undefined.
  - Strategy: Replace zeros with 1, then mark those positions as $-\infty$ in log space.
  - Implementation:
    ```python
    Matrix_safe = np.where(Matrix == 0, 1, Matrix)
    log_matrix = np.log(Matrix_safe.astype(float))
    log_matrix[Matrix == 0] = -np.inf
    ```
  - **Why this works:** $\log(1) = 0$, so replacing zeros with 1 doesn't affect sums. The $-\infty$ ensures these positions are ignored when taking the maximum.

- **Step 2: Horizontal Convolution**
  - Create a kernel: `h_kernel = np.ones((1, adj_size))` — shape `(1, adj_size)`.
  - Apply correlation: `h_corr = signal.correlate2d(log_matrix, h_kernel, mode='valid')`.
  - **What this does:** Slides a 1×`adj_size` window across each row, summing `adj_size` consecutive log values.
  - In log space, summing = multiplying in normal space: $\log(a) + \log(b) + \log(c) = \log(a \times b \times c)$.
  - `mode='valid'` ensures only complete `adj_size`-element windows are included.
  - **Generalization:** For `adj_size=6`, the kernel becomes `(1, 6)`, automatically finding products of 6 numbers.

- **Step 3: Vertical Convolution**
  - Create a kernel: `v_kernel = np.ones((adj_size, 1))` — shape `(adj_size, 1)`.
  - Apply correlation: `v_corr = signal.correlate2d(log_matrix, v_kernel, mode='valid')`.
  - This slides an `adj_size`×1 window down each column.
  - **Generalization:** Kernel height scales with `adj_size`.

- **Step 4: Understanding Matrix Skewing for Diagonals**
  - **The Problem:** Diagonals don't align with rows or columns, so simple convolution doesn't work.
  - **The Solution:** Transform the matrix so diagonals become vertical columns.
  - **Skewing Visualization (for general `adj_size`):**
    ```
    Original:           After padding + rolling:
    a b c d            a b c d
    e f g h            _ e f g h
    i j k l     →      _ _ i j k l
    m n o p            _ _ _ m n o p
    
    Diagonals now align vertically in different columns
    ```

- **Step 5: Down-Right Diagonal Skewing**
  - **Pad left:** `padded_dr = np.pad(log_matrix, ((0, 0), (grid_size-1, 0)), constant_values=-np.inf)`.
    - Adds `grid_size-1` columns of $-\infty$ on the left.
    - **Generalization:** Padding width scales with `grid_size`, not `adj_size`.
  - **Roll each row left:** `skewed_dr = np.array([np.roll(padded_dr[i], -i) for i in range(grid_size)])`.
    - Row 0: no shift.
    - Row 1: shift left by 1.
    - Row 2: shift left by 2.
    - ...
    - Row `grid_size-1`: shift left by `grid_size-1`.
  - **Result:** Down-right diagonals now align vertically.
  - Apply vertical convolution: `dr_corr = signal.correlate2d(skewed_dr, v_kernel, mode='valid')`.
  - **Generalization:** The vertical kernel size `(adj_size, 1)` determines how many diagonal elements are multiplied.

- **Step 6: Down-Left Diagonal Skewing**
  - **Pad right:** `padded_dl = np.pad(log_matrix, ((0, 0), (0, grid_size-1)), constant_values=-np.inf)`.
  - **Roll each row right:** `skewed_dl = np.array([np.roll(padded_dl[i], i) for i in range(grid_size)])`.
  - **Result:** Down-left diagonals now align vertically.
  - Apply vertical convolution: `dl_corr = signal.correlate2d(skewed_dl, v_kernel, mode='valid')`.
  - **Generalization:** Same kernel `v_kernel` works for any `adj_size`.

- **Step 7: The Role of $-\infty$ Padding**
  - When correlation encounters $-\infty$, the sum becomes $-\infty$.
  - These invalid windows are automatically excluded when taking the maximum.
  - This is cleaner than manually tracking valid regions.
  - **Generalization:** Works regardless of `adj_size` or `grid_size`.

- **Step 8: Converting Back from Log Space**
  - Find maximum in log space: `max_log = max(h_corr.max(), v_corr.max(), dr_corr.max(), dl_corr.max())`.
  - Convert back: `max_product = int(round(np.exp(max_log)))`.
  - Rounding handles any floating-point precision issues.

- **Step 9: Why `correlate2d` Instead of `convolve2d`?**
  - `convolve2d` flips the kernel both horizontally and vertically.
  - `correlate2d` doesn't flip the kernel.
  - For our symmetric kernels (all 1s), it doesn't matter, but `correlate2d` is conceptually clearer.

- **Efficiency:** This solution is highly efficient for large grids. The convolution operations are implemented in optimized C code. The skewing transformation adds some overhead but scales well. The beauty is that changing `adj_size` from 4 to 8 only requires changing one variable—all kernel sizes and convolution operations adjust automatically.

---

## Mathematical Foundation

### Matrix Skewing for Diagonal Extraction

**Theorem:** By padding a matrix on one side and shifting each row by its index, diagonals can be transformed into vertical columns for any adjacency length.

**Proof for Down-Right Diagonals (General Case):**

Consider an $n \times n$ matrix with elements at positions $(i, j)$ where $0 \leq i, j < n$.

A down-right diagonal with offset $k$ contains elements where $j - i = k$.

After padding left with $n-1$ columns and rolling row $i$ left by $i$ positions:
- The original element $(i, j)$ now appears at column position $j + (n-1) - i$.
- For elements on a diagonal where $j - i = k$, the new column position is:
  $$\text{new\_col} = j + (n-1) - i = (j-i) + (n-1) = k + (n-1)$$

Since all elements on the same diagonal have the same $k$ value, they all align in the same column.

**Key insight:** The adjacency length `adj_size` doesn't affect the skewing transformation itself—it only determines the kernel size used in the subsequent convolution. This is why the solution generalizes seamlessly. ∎

---

### Logarithmic Product-to-Sum Transformation

**Property:** For positive numbers $a_1, a_2, \ldots, a_m$ where $m$ is any positive integer:
$$\log(a_1 \times a_2 \times \cdots \times a_m) = \log(a_1) + \log(a_2) + \cdots + \log(a_m)$$

**Application to Convolution:**
- Convolution with a kernel of all 1s computes sums of elements.
- By working in log space, these sums represent products in normal space.
- This transforms a multiplication problem into an addition problem.
- Addition is the fundamental operation in convolution, making this transformation natural.
- **Generalization:** Works for any adjacency length—a kernel of size $m$ sums $m$ log values, representing a product of $m$ numbers.

**Caution:** This transformation assumes all values are positive. Zeros must be handled separately (as done in Solution 3).

---

## Comparison of Solutions

| Aspect | Solution 1<br>(Index-Swapping) | Solution 2<br>(NumPy Sliding Window) | Solution 3<br>(Scipy Convolution) |
|--------|-------------------------------|-------------------------------------|-----------------------------------|
| **Approach** | Compact loops with index symmetry | Vectorized sliding windows | Signal processing with skewing |
| **Dependencies** | Pure Python (lists) | NumPy | NumPy + Scipy |
| **Generalizability** | Fully general with simple bounds | Automatic with window sizes | Kernel sizes scale automatically |
| **Code Clarity** | Very readable | Clear with NumPy knowledge | Requires advanced understanding |
| **Parameter Changes** | Modify loop bounds and conditions | Only change window dimensions | Only change kernel sizes |
| **Validation** | Custom error handling | Custom error handling | Custom error handling |
| **Scalability** | Good for small-medium grids | Excellent for large grids | Excellent for very large grids |
| **Educational Value** | ★★★★★ | ★★★★ | ★★★★★ |
| **Production Use** | ★★★ | ★★★★★ | ★★★★ |

---

## Output

```
70600674
```

---

## Notes

- The greatest product of four adjacent numbers in the 20×20 grid is **70,600,674**.
- This product comes from four numbers arranged horizontally, vertically, or diagonally.
- **All three solutions are fully generalizable:**
  - Changing `adj_size` from 4 to any other value (e.g., 6, 8, 10) requires modifying only the parameter definition.
  - The algorithms automatically adjust loop bounds, window sizes, kernel dimensions, and padding to accommodate the new adjacency length.
  - Grid size can also be changed by providing a different input matrix.
- **Input validation is crucial:**
  - All three solutions implement the same validation check to prevent invalid parameters.
  - This defensive programming ensures robustness and provides clear error messages.
  - Without validation, attempting `adj_size=25` on a 20×20 grid would cause index errors rather than a helpful error message.
- **Solution 1** demonstrates elegant algorithm design through symmetry exploitation—checking multiple directions with minimal code duplication. The boundary conditions automatically scale with `adj_size`.
- **Solution 2** showcases modern array processing with NumPy's `sliding_window_view`, providing excellent performance through vectorization. Window dimensions scale naturally with the adjacency parameter.
- **Solution 3** illustrates advanced mathematical transformations, converting a grid search problem into signal processing via logarithms and matrix skewing. Kernel sizes adjust automatically to any adjacency length.
- The **matrix skewing technique** in Solution 3 is independent of adjacency length—it transforms diagonals into columns regardless of how many elements we plan to multiply. The adjacency length only affects the convolution kernel size.
- For grid-based problems with configurable parameters, choosing between direct iteration (Solution 1), vectorized array operations (Solution 2), or signal processing techniques (Solution 3) depends on grid size, performance requirements, and code maintainability considerations.
- The generalizability of these solutions makes them suitable for extended versions of this problem, such as finding products of 6, 8, or even 12 adjacent numbers in larger grids.
