# Problem 15: Lattice Paths

**Problem source:** [Project Euler Problem 15](https://projecteuler.net/problem=15)

**Problem statement:**

Starting in the top left corner of a $2 \times 2$ grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.

How many such routes are there through a $20 \times 20$ grid?

---

## Solution 1: Dynamic Programming (Iterative Table)

### Approach

- Build a 2D table where each cell represents the number of paths from that position to the bottom-right corner.
- Initialize the bottom row and rightmost column to 1 (base case: only one path along the edges).
- Fill the table from bottom-right to top-left using the recurrence relation: `paths[i][j] = paths[i+1][j] + paths[i][j+1]`.
- The top-left cell contains the total number of paths through the entire grid.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Grid Initialization**
  - Create a $(n+1) \times (n+1)$ grid initialized to zeros: `grid = [[0]*(grid_size+1) for _ in range(grid_size+1)]`.
  - **Why $(n+1) \times (n+1)$?** For a $20 \times 20$ grid, we need to track positions from $(0,0)$ to $(20,20)$, which requires 21 rows and 21 columns.
  - Indexing: `grid[i][j]` represents the number of paths from position $(i,j)$ to the goal $(20,20)$.

- **Step 2: Base Case Setup**
  - The bottom row and rightmost column form the boundary of the grid.
  - From any position on the bottom edge, there's only one path: move right until reaching the corner.
  - From any position on the right edge, there's only one path: move down until reaching the corner.
  - Initialize: `grid[grid_size][i] = 1` and `grid[i][grid_size] = 1` for all valid positions.
  - This sets up the boundary conditions for the recurrence relation.

- **Step 3: Recurrence Relation**
  - For any interior position $(i,j)$, the number of paths equals the sum of:
    - Paths from the cell below: `grid[i+1][j]`
    - Paths from the cell to the right: `grid[i][j+1]`
  - Formula: `grid[i][j] = grid[i+1][j] + grid[i][j+1]`
  - **Why this works:** At each position, you can only move right or down. The total paths from $(i,j)$ is the sum of paths if you go right plus paths if you go down.

- **Step 4: Filling the Table**
  - Use nested loops to fill the grid from bottom-right to top-left:
    - Outer loop: `for i in range(grid_size-1, -1, -1)` iterates rows from 19 down to 0.
    - Inner loop: `for j in range(grid_size-1, -1, -1)` iterates columns from 19 down to 0.
  - This order ensures that when computing `grid[i][j]`, the values `grid[i+1][j]` and `grid[i][j+1]` are already computed.

- **Step 5: Extract Result**
  - After filling the table, `grid[0][0]` contains the answer: the number of paths from the top-left to bottom-right corner.
  - For a $20 \times 20$ grid, this value is $137,846,528,820$.

- **Efficiency:** This solution fills a $(21 \times 21)$ table, performing 441 additions. The nested loops ensure each cell is computed exactly once. Memory usage is proportional to the grid size.

---

## Solution 2: Recursive Dynamic Programming with Memoization

### Approach

- Use a **recursive function** to compute the number of paths from any position $(i,j)$ to the goal.
- Apply **memoization** using Python's `@lru_cache` decorator to cache results and avoid redundant calculations.
- The base case: when reaching the bottom or right edge, there's exactly 1 path remaining.
- The recursive case: paths from $(i,j)$ equals paths from $(i+1,j)$ plus paths from $(i,j+1)$.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Memoization Setup**
  - Use `@lru_cache((grid_size+1)**2)` to cache function results.
  - **What is `@lru_cache`?** It's a decorator that automatically stores the results of function calls. When the function is called again with the same arguments, it returns the cached result instead of recomputing.
  - **Why `(grid_size+1)**2`?** For a $20 \times 20$ grid, there are $21 \times 21 = 441$ possible positions $(i,j)$. Setting the cache size to 441 ensures all unique calls are cached.
  - **LRU stands for "Least Recently Used":** If the cache fills up, it removes the least recently accessed entries. With the correct size, this never happens.

- **Step 2: Base Case**
  - When `i == grid_size` or `j == grid_size`, we've reached the bottom or right edge.
  - Return `1` because there's exactly one path remaining: follow the edge to the corner.
  - Example: From position $(20, 15)$, there's only one path: move down 5 times to reach $(20, 20)$.

- **Step 3: Recursive Case**
  - For any interior position $(i,j)$, compute: `paths(i+1, j) + paths(i, j+1)`
  - This represents: "paths if I move down" + "paths if I move right"
  - The recursion naturally explores all possible routes through the grid.

- **Step 4: How Memoization Transforms Performance**
  - **Without caching:** The same positions would be computed multiple times.
    - Example: Position $(10, 10)$ could be reached from $(9,10)$ or $(10,9)$, causing duplicate work.
  - **With caching:** Each position is computed exactly once, then reused.
  - The cache grows as the recursion explores the grid, eventually storing all 441 unique positions.

- **Step 5: Calling the Function**
  - `paths(0, 0)` initiates the recursion from the top-left corner.
  - The function recursively calls itself, building up the solution from smaller subproblems.
  - Thanks to memoization, this approach is just as efficient as the iterative table-filling method.

- **Step 6: Why Set Cache Size Explicitly?**
  - By default, `@lru_cache` has a maximum size of 128 entries.
  - For our problem with 441 positions, the default would cause cache evictions and recomputation.
  - Setting `maxsize=(grid_size+1)**2` ensures the cache can hold all results without evictions.
  - This guarantees each position is computed exactly once.

- **Efficiency:** This solution computes 441 unique function calls, each performing a simple addition. The recursive approach is elegant and intuitive, expressing the problem naturally while achieving the same performance as the iterative solution thanks to memoization.

---

## Solution 3: Closed-Form Mathematical Formula

### Approach

- Recognize that finding paths through a grid is equivalent to arranging moves in a sequence.
- For a $20 \times 20$ grid, any path consists of exactly 20 RIGHT moves and 20 DOWN moves (40 moves total).
- The problem becomes: "In how many ways can we arrange 20 R's and 20 D's?"
- This is a **combinatorics** problem answered by the binomial coefficient: $\binom{40}{20}$.
- Use Python's `math.comb` function to compute the result directly.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: The Combinatorial Insight**
  - Every path from $(0,0)$ to $(n,n)$ consists of exactly $n$ RIGHT moves and $n$ DOWN moves.
  - See the **Mathematical Foundation** section below for a rigorous proof of why this must be true.
  - The problem reduces to: "In how many ways can we arrange $n$ R's and $n$ D's?"

- **Step 2: Reframing the Problem**
  - **Original question:** How many different paths are there?
  - **Equivalent question:** How many ways can we choose which $n$ of our $2n$ total moves should be RIGHT (the rest will be DOWN)?
  - This is answered by the binomial coefficient: $\binom{2n}{n}$

- **Step 3: Implementation**
  - Python's `math.comb(n, k)` efficiently computes $\binom{n}{k} = \frac{n!}{k!(n-k)!}$
  - For an $n \times n$ grid: `math.comb(2*grid_size, grid_size)` computes $\binom{2n}{n}$
  - This single function call produces the answer instantly with no iteration required

- **Efficiency:** This is the most efficient solution. It computes the answer using a single mathematical formula with no iteration or recursion. The `math.comb` function is highly optimized and completes in microseconds regardless of grid size.

---

## Mathematical Foundation

### The Combinatorial Proof

**Theorem:** The number of lattice paths through an $n \times n$ grid equals $\binom{2n}{n}$.

**Proof:**

Consider any path from $(0,0)$ to $(n,n)$ using only RIGHT (R) and DOWN (D) moves.

Every such path consists of:
- Exactly $n$ RIGHT moves (to traverse $n$ columns)
- Exactly $n$ DOWN moves (to traverse $n$ rows)
- Total moves: $2n$

We can represent any path as a sequence of $2n$ symbols, where $n$ symbols are R and $n$ symbols are D.

The question "How many different paths exist?" is equivalent to "How many different sequences of $n$ R's and $n$ D's can we create?"

This is a combination problem: We have $2n$ positions and need to choose $n$ of them to place R (the remaining $n$ positions automatically get D).

The number of ways to choose $n$ items from $2n$ items is:
$\binom{2n}{n} = \frac{(2n)!}{n! \cdot n!}$

**Example for $n=2$:**
- Paths through a $2 \times 2$ grid require 2 R's and 2 D's (4 moves total)
- Possible sequences:
  1. `RRDD` → right, right, down, down
  2. `RDRD` → right, down, right, down  
  3. `RDDR` → right, down, down, right
  4. `DRRD` → down, right, right, down
  5. `DRDR` → down, right, down, right
  6. `DDRR` → down, down, right, right
- Count: $\binom{4}{2} = \frac{4!}{2! \cdot 2!} = \frac{24}{4} = 6$ ✓

Therefore, the number of lattice paths through an $n \times n$ grid is $\binom{2n}{n}$. ∎

---

## Comparison of Solutions

| Aspect | Solution 1<br>(DP Table) | Solution 2<br>(Memoized Recursion) | Solution 3<br>(Mathematical) |
|--------|-------------------------|-----------------------------------|----------------------------|
| **Approach** | Iterative table filling | Recursive with caching | Direct formula |
| **Computations** | 441 additions | 441 function calls | 1 combinatorial calculation |
| **Memory** | $(n+1)^2$ grid | Cache of $(n+1)^2$ results | Constant |
| **Code Clarity** | ★★★★★ | ★★★★★ | ★★★★★ |
| **Performance** | Fast | Fast | Instant |
| **Best For** | Understanding DP | Functional programming style | Optimal efficiency |

---

## A Note on NumPy and This Problem

While NumPy is excellent for many computational problems, it doesn't provide significant benefits for this lattice paths problem. The core challenge is that the dynamic programming recurrence has dependencies within each row being updated.

**Why NumPy vectorization doesn't help here:**
- The DP update `grid[i][j] = grid[i+1][j] + grid[i][j+1]` requires values from the same row (`grid[i][j+1]`).
- When updating an entire row at once with NumPy slicing like `grid[i, :-1] = grid[i+1, :-1] + grid[i, 1:]`, the right side reads from the row being modified on the left side.
- This creates incorrect dependencies where left cells use already-modified right cells, leading to wrong results.
- The dependencies must be respected by computing cells in a specific order (right-to-left within each row).

**Where NumPy excels:**
- Element-wise operations without dependencies
- Sliding window operations
- Convolutions and filters
- Problems like the Sieve of Eratosthenes where marking composites are independent operations

**For this problem:**
- Simple nested loops (Solution 1) are clear and efficient
- Memoized recursion (Solution 2) is elegant and equally fast
- The mathematical formula (Solution 3) is optimal

The lesson: Don't force a tool where it doesn't fit. NumPy is powerful, but understanding when **not** to use it is just as important as knowing when to use it.

---

## Output

```
137846528820
```

---

## Notes

- For an $n \times n$ grid, the number of paths is $\binom{2n}{n}$.
- For the specific case of a $20 \times 20$ grid, the answer is $137,846,528,820$.
- **Solution 3** (Mathematical Formula) is the optimal approach, computing the answer instantly using combinatorics.
- **Solution 2** demonstrates the power of memoization, transforming a potentially exponential recursive solution into an efficient one by caching results.
- **Solution 1** shows the classic dynamic programming approach, building the solution iteratively from base cases.
- The problem beautifully illustrates how a computational problem (counting paths) can be reframed as a combinatorics problem (arranging symbols), leading to a closed-form solution.
- The grid requires $(n+1) \times (n+1)$ cells because positions range from $(0,0)$ to $(n,n)$, inclusive.
- All three solutions produce the exact same answer, demonstrating different problem-solving paradigms: iteration, recursion with memoization, and pure mathematics.
