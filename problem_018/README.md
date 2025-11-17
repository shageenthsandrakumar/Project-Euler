# Problem 18: Maximum Path Sum I

**Problem source:** [Project Euler Problem 18](https://projecteuler.net/problem=18)

**Problem statement:**

By starting at the top of the triangle below and moving to adjacent numbers on the row below, the maximum total from top to bottom is 23.

```
   3
  7 4
 2 4 6
8 5 9 3
```

That is, $3 + 7 + 4 + 9 = 23$.

Find the maximum total from top to bottom of the triangle below:

```
75
95 64
17 47 82
18 35 87 10
20 04 82 47 65
19 01 23 75 03 34
88 02 77 73 07 63 67
99 65 04 28 06 16 70 92
41 41 26 56 83 40 80 70 33
41 48 72 33 47 32 37 16 94 29
53 71 44 65 25 43 91 52 97 51 14
70 11 33 28 77 73 17 78 39 68 17 57
91 71 52 38 17 14 91 43 58 50 27 29 48
63 66 04 68 89 53 67 30 73 16 69 87 40 31
04 62 98 27 23 09 70 98 73 93 38 53 60 04 23
```

**NOTE:** As there are only 16384 routes, it is possible to solve this problem by trying every route. However, Problem 67, is the same challenge with a triangle containing one-hundred rows; it cannot be solved by brute force, and requires a clever method! ;o)

---

## Solution 1: Bottom-Up Dynamic Programming

### Approach

- Use **dynamic programming** with a bottom-up strategy to find the maximum path sum.
- Start from the second-to-last row and work upward toward the top.
- For each position, add the maximum of its two children from the row below.
- Modify the triangle **in-place** to store intermediate results.
- The final answer is stored at the top of the triangle.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Parse Input**
  - Split the multi-line string by newlines to get individual rows.
  - Convert each row into a list of integers using list comprehension.
  - Result: A 2D list `triangle` where `triangle[i][j]` is the element at row `i`, position `j`.

- **Step 2: Identify Triangle Structure**
  - The triangle has 15 rows (indices 0-14).
  - Row `i` has `i+1` elements (row 0 has 1 element, row 1 has 2 elements, etc.).
  - From position `(i, j)`, you can move to either `(i+1, j)` or `(i+1, j+1)`.

- **Step 3: Bottom-Up Dynamic Programming**
  - Start from row `levels-2` (second-to-last row, index 13) and work upward to row 0.
  - For each position `(i, j)` in the current row:
    - Look at the two children: `triangle[i+1][j]` and `triangle[i+1][j+1]`.
    - Choose the larger child: `max(triangle[i+1][j], triangle[i+1][j+1])`.
    - Add this maximum to the current value: `triangle[i][j] += max(...)`.
  - This updates each cell to represent: "the maximum sum achievable from this position down to the bottom."

- **Step 4: Extract Result**
  - After processing all rows, `triangle[0][0]` contains the maximum sum from top to bottom.
  - This is the final answer.

- **Why This Works**
  - **Optimal substructure:** The maximum path from position `(i, j)` to the bottom equals the current value plus the maximum path from the better child.
  - **Overlapping subproblems:** Many paths share common subpaths. By working bottom-up, we compute each cell's result exactly once.
  - **In-place modification:** We reuse the triangle structure to store results, requiring no additional memory.

- **Efficiency:** This solution processes each cell in the triangle exactly once, visiting approximately $\frac{n(n+1)}{2}$ cells for a triangle with $n$ rows. For the 15-row triangle, this is 120 operations. The in-place modification requires no additional memory beyond the input structure.

---

## Solution 2: Top-Down Recursive with Memoization

### Approach

- Use **recursion** starting from the top of the triangle and working downward.
- For each position, recursively compute the maximum path sum from that position to the bottom.
- Apply **memoization** using Python's `@lru_cache` decorator to avoid recomputing results.
- The base case is reaching the bottom row, where the path sum equals the cell's value.
- The recursive case adds the current cell's value to the maximum of its two children's path sums.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Parse Input**
  - Same as Solution 1: convert the text into a 2D list `triangle`.

- **Step 2: Define Recursive Function**
  - `max_path_sum(i, j)` returns the maximum sum from position `(i, j)` to the bottom.
  - **Base case:** If `i == levels-1` (bottom row), return `triangle[i][j]`.
  - **Recursive case:** Return `triangle[i][j] + max(max_path_sum(i+1, j), max_path_sum(i+1, j+1))`.

- **Step 3: Memoization with `@lru_cache`**
  - The decorator `@lru_cache(levels*(levels+1)//2)` caches results for up to 120 unique `(i, j)` pairs.
  - This is exactly the number of cells in the triangle.
  - When `max_path_sum(i, j)` is called:
    - If the result is already cached, return it immediately (O(1) lookup).
    - Otherwise, compute it recursively and store it in the cache.

- **Step 4: Why This Works**
  - The problem has **optimal substructure**: the best path from `(i, j)` depends on the best paths from its children.
  - Without memoization, this would explore exponentially many paths (each position branches into two paths).
  - With memoization, each `(i, j)` pair is computed exactly once, reducing redundant computation.

- **Step 5: Call and Extract Result**
  - Call `max_path_sum(0, 0)` to start from the top of the triangle.
  - This triggers recursive calls that eventually reach the bottom row.
  - The memoization ensures efficient computation even though the approach is top-down.
  - The function returns the maximum path sum from top to bottom.

- **Efficiency:** With memoization, this solution computes each cell's result exactly once, similar to Solution 1. The recursive approach is more intuitive for some programmers, following the natural "path from top to bottom" mental model. However, it uses additional memory for the call stack and the cache dictionary.

---

## Solution 3: Tropical Matrix Multiplication

### Approach

- Reframe the maximum path sum problem as a **tropical algebra** computation.
- In tropical algebra (max-plus algebra), we redefine arithmetic operations:
  - **Tropical addition** (⊕): `a ⊕ b = max(a, b)`
  - **Tropical multiplication** (⊗): `a ⊗ b = a + b`
- Represent each row of the triangle as a **transformation matrix** in the tropical semiring.
- Use the `mplusa` library to perform tropical matrix multiplication.
- Propagate information from bottom to top by composing transformations.
- The final result is the maximum path sum.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Parse Input**
  - Same as previous solutions: convert the text into a 2D list `triangle`.

- **Step 2: Tropical Algebra Overview**
  - This solution uses **tropical algebra** (max-plus algebra), where standard operations are redefined.
  - In tropical algebra: "addition" means max, and "multiplication" means +.
  - See the **Mathematical Foundation** section for a complete explanation of tropical semirings and why this works.
  - The key insight: our DP recurrence translates directly to tropical matrix multiplication.

- **Step 3: Selector Matrix Construction**
  - For each row `i` of the triangle, create a **selector matrix** of shape `(i+1) × (i+2)`.
  - The matrix encodes both the triangle values and the adjacency structure (which children are reachable).
  - Most entries are `-np.inf` (which blocks paths in tropical algebra).
  - The selector matrix has two diagonals set to the row values:
    - Main diagonal (offset 0): `selector[j, j] = triangle[i][j]` (left child connection)
    - First superdiagonal (offset 1): `selector[j, j+1] = triangle[i][j]` (right child connection)
  - **Vectorized implementation using NumPy:**
    ```python
    selector = np.full((i+1, i+2), -np.inf)
    np.fill_diagonal(selector, triangle[i])
    np.fill_diagonal(selector[:, 1:], triangle[i]) 
    ```
  - **How the slicing works:**
    - `np.fill_diagonal(selector, triangle[i])` fills the main diagonal: positions `(0,0), (1,1), (2,2), ...`
    - `selector[:, 1:]` creates a **view** of the matrix starting from column 1 (skipping column 0).
      - This shifts the coordinate system: what appears as column 0 in the view is actually column 1 in the original matrix.
    - `np.fill_diagonal(selector[:, 1:], triangle[i])` fills the diagonal of this shifted view.
      - In the view's coordinates: positions `(0,0), (1,1), (2,2), ...`
      - In the original matrix: positions `(0,1), (1,2), (2,3), ...` — the superdiagonal!
    - The view modification directly affects the original matrix, so both diagonals are set.
  - This vectorized approach sets both diagonals efficiently without explicit loops.

- **Step 4: Example Selector Matrix**
  - Row 1 of small triangle has values `[7, 4]`.
  - Selector matrix (2 × 3):
    ```
    [[ 7,  7, -∞],
     [-∞,  4,  4]]
    ```
  - From position 0 (value 7): can reach positions 0 or 1 below.
  - From position 1 (value 4): can reach positions 1 or 2 below.

- **Step 5: Initialize with Bottom Row**
  - Start with the bottom row as a column vector:
    ```python
    current = np.array(triangle[-1], dtype=float).reshape(-1, 1)
    ```
  - This represents the "value from here to the bottom" for the bottom row (just the values themselves).

- **Step 6: Iterate Bottom-Up with Tropical Multiplication**
  - For each row from second-to-last up to the top:
    - Create the selector matrix for that row.
    - Perform tropical matrix multiplication: `current = mp.mult_matrices(selector, current)`
    - This propagates maximum path information upward.
  - The `mp.mult_matrices` function from `mplusa` computes: `C[i,k] = maxⱼ (A[i,j] + B[j,k])`
  - See **Mathematical Foundation** for proof that this equals the DP recurrence.

- **Step 7: Extract Result**
  - After all multiplications, `current[0, 0]` contains the maximum path sum.
  - Convert to integer: `int(current[0, 0])`.

- **Library and Practical Notes**
  - **`mplusa`** is a specialized Python library for max-plus algebra developed by Sébastien Lahaye at Université d'Angers (France). 
  - **When to use:** Educational purposes, research contexts, or when working with problems naturally expressed in tropical algebra.

- **Efficiency:** This approach performs the same fundamental computations as standard DP—computing the maximum over valid children for each position. The matrix formulation adds some overhead (matrix construction, library calls) but demonstrates that path optimization problems can be expressed as linear algebra in a different algebraic structure. For practical applications, Solutions 1 or 2 are recommended.

---

## Mathematical Foundation

### The Maximum Path Problem

For a triangle with $n$ rows, let $T[i][j]$ denote the value at row $i$, position $j$ (0-indexed).

**Movement rules:** From position $(i, j)$, you can move to:
- $(i+1, j)$ (down-left)
- $(i+1, j+1)$ (down-right)

**Goal:** Find the maximum sum along any valid path from $(0, 0)$ to any cell in row $n-1$.

### Dynamic Programming Recurrence

Define $M[i][j]$ as the maximum sum from position $(i, j)$ to the bottom row.

**Base case:** For row $n-1$ (bottom row):
$$M[n-1][j] = T[n-1][j]$$

**Recursive case:** For rows $i < n-1$:
$$M[i][j] = T[i][j] + \max(M[i+1][j], M[i+1][j+1])$$

**Solution:** The answer is $M[0][0]$.

### Why Dynamic Programming Works

**Optimal substructure:** The optimal path from $(i, j)$ to the bottom consists of:
1. The value at $(i, j)$
2. Plus the optimal path from the better of its two children

**Overlapping subproblems:** Many paths converge at the same positions. For example, paths through $(0, 0) \to (1, 0)$ and $(0, 0) \to (1, 1)$ may both pass through $(2, 1)$. Computing $M[2][1]$ once and reusing it avoids redundant work.

### Tropical Algebra Foundations

**Definition:** A **tropical semiring** (max-plus algebra) consists of:
- Set: $\mathbb{R} \cup \{-\infty\}$
- Operations:
  - **Tropical addition (⊕):** $a \oplus b = \max(a, b)$
  - **Tropical multiplication (⊗):** $a \otimes b = a + b$
- Identities:
  - Additive identity: $-\infty$ (since $\max(-\infty, a) = a$)
  - Multiplicative identity: $0$ (since $a + 0 = a$)

**Properties:**
- **Associativity:** Both operations are associative.
- **Commutativity:** $a \oplus b = b \oplus a$ and $a \otimes b = b \otimes a$.
- **Distributivity:** $a \otimes (b \oplus c) = (a \otimes b) \oplus (a \otimes c)$
  - Proof: $a + \max(b, c) = \max(a+b, a+c)$ ✓

### Tropical Matrix Multiplication

For matrices $A$ (size $m \times p$) and $B$ (size $p \times n$), the tropical product $C = A \otimes B$ is:
$$C[i][k] = \bigoplus_{j=1}^{p} (A[i][j] \otimes B[j][k]) = \max_{j=1}^{p} (A[i][j] + B[j][k])$$

**Comparison to standard multiplication:**
- Standard: $C[i][k] = \sum_{j} A[i][j] \times B[j][k]$
- Tropical: $C[i][k] = \max_{j} (A[i][j] + B[j][k])$

### Connection to Path Problems

The dynamic programming recurrence:
$$M[i][j] = T[i][j] + \max(M[i+1][j], M[i+1][j+1])$$

can be rewritten in tropical algebra as:
$$M[i][j] = T[i][j] \otimes (M[i+1][j] \oplus M[i+1][j+1])$$

This is a tropical linear combination! By encoding the triangle structure as matrices and using tropical multiplication, we compute the same result through matrix operations.

### The Selector Matrix Construction

For row $i$ with values $T[i][0], T[i][1], \ldots, T[i][i]$:

**Matrix dimensions:** $(i+1) \times (i+2)$
- Rows: positions in current row
- Columns: positions in next row


**Interpretation:** The selector matrix encodes both:
1. The values at the current row
2. The adjacency structure (which children are reachable)

The $-\infty$ entries act as "blocked paths" because:

$-\infty \otimes x = -\infty + x = -\infty$

$a \oplus (-\infty) = \max(a, -\infty) = a$

So blocked paths don't contribute to the maximum.

### Why Tropical Multiplication Gives the DP Recurrence

When we multiply selector matrix $S_i$ (for row $i$) with column vector $V_{i+1}$ (containing $M[i+1][j]$ values):

$(S_i \otimes V_{i+1})[j] = \bigoplus_{k} (S_i[j][k] \otimes V_{i+1}[k])$
$= \max_{k} (S_i[j][k] + V_{i+1}[k])$

Since $S_i[j][k]$ is $T[i][j]$ only when $k \in \{j, j+1\}$ and $-\infty$ otherwise:

$= \max(T[i][j] + V_{i+1}[j], \, T[i][j] + V_{i+1}[j+1], \, -\infty, \ldots, -\infty)$
$= T[i][j] + \max(V_{i+1}[j], V_{i+1}[j+1])$
$= T[i][j] + \max(M[i+1][j], M[i+1][j+1])$

This is exactly the DP recurrence! The tropical matrix multiplication naturally computes the maximum path sum.


### Historical Note on Tropical Algebra

Tropical algebra emerged in the 1980s from work on **idempotent analysis** by mathematicians including:
- **V. P. Maslov** (Russian school of idempotent analysis)
- **Imre Simon** (after whom the field is named)

The term "tropical" was coined as a tribute to Simon's Brazilian nationality. The algebra has found applications in:
- **Optimization theory:** Shortest/longest path problems
- **Discrete event systems:** Timing and scheduling analysis
- **Algebraic geometry:** Tropical geometry, a piecewise-linear analogue of classical geometry
- **Computational biology:** Phylogenetic tree reconstruction
- **Control theory:** Max-plus linear systems

---

## Comparison of Solutions

| Aspect | Solution 1<br>(Bottom-Up DP) | Solution 2<br>(Top-Down Memoization) | Solution 3<br>(Tropical Matrices) |
|--------|------------------------------|-------------------------------------|----------------------------------|
| **Approach** | Iterative, bottom-up | Recursive, top-down | Algebraic transformations |
| **Direction** | Start at bottom, work up | Start at top, recurse down | Bottom-up matrix composition |
| **Memory** | In-place modification | Cache + call stack | Matrices + library overhead |
| **Dependencies** | None (pure Python) | None (pure Python) | `numpy`, `mplusa` |
| **Code Clarity** | ★★★★★ | ★★★★★ | ★★★ |
| **Mathematical Elegance** | ★★★ | ★★★ | ★★★★★ |
| **Practical Use** | Excellent | Excellent | Educational/research |
| **Speed** | Very fast | Very fast | Comparable (library overhead) |
| **Installation** | Immediate | Immediate | Requires external library |
| **Best For** | Production code | Intuitive understanding | Mathematical insight |

---

## Output

```
1074
```

---

## Notes

- The maximum path sum from top to bottom of the 15-row triangle is **1074**.
- **Solution 1** (Bottom-Up DP) is the optimal choice for production code: simple, fast, and requires no external dependencies.
- **Solution 2** (Top-Down Memoization) offers an equally efficient alternative with a more intuitive recursive structure that mirrors the natural "path from top to bottom" mental model.
- **Solution 3** (Tropical Matrix Multiplication) demonstrates the deep connection between optimization problems and algebraic structures. While not practical for production use, it provides valuable mathematical insight.
- The tropical algebra approach shows that the maximum path problem is fundamentally a **linear algebra problem in a different semiring**. This perspective connects discrete optimization to continuous algebraic structures.
- The `mplusa` library is an academic research tool not widely available through standard package managers. For practical applications, Solutions 1 or 2 are strongly recommended.
- **Problem 67** uses a 100-row triangle and cannot be solved by brute force (which would require checking $2^{99} \approx 6.3 \times 10^{29}$ paths). All three solutions presented here scale to Problem 67 without modification.
- The dynamic programming solutions reduce the computational complexity from exponential (brute force) to quadratic (processing each cell once), making previously intractable problems easily solvable.
- Tropical algebra finds real-world applications in scheduling theory, where "maximizing sum" corresponds to finding critical paths, and in network optimization, where finding longest paths determines system bottlenecks.
- The distributive property in tropical algebra — $a + \max(b, c) = \max(a+b, a+c)$ — is the key mathematical fact that makes tropical matrix multiplication equivalent to the dynamic programming recurrence.
