# Problem 24: Lexicographic Permutations

**Problem source:** [Project Euler Problem 24](https://projecteuler.net/problem=24)

**Problem statement:**

A permutation is an ordered arrangement of objects. For example, 3124 is one possible permutation of the digits 1, 2, 3 and 4. If all of the permutations are listed numerically or alphabetically, we call it lexicographic order. The lexicographic permutations of 0, 1 and 2 are:

$$012 \quad 021 \quad 102 \quad 120 \quad 201 \quad 210$$

What is the millionth lexicographic permutation of the digits 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9?

---

## Solution 1: Generate All Permutations

### Approach

- Use Python's built-in `itertools.permutations()` to generate all permutations of the digits 0-9.
- The permutations are automatically generated in lexicographic order.
- Access the millionth permutation directly using list indexing (position 999,999 in 0-indexed arrays).
- Convert the tuple of digits to a string for output.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Generate All Permutations**
  - Create a list of digits: `numbers = list(range(highest_number+1))` produces `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`.
  - Use `permutations(numbers)` to generate all possible orderings.
  - Convert to a list: `sorted_list = list(permutations(numbers))`.
  - This creates a list containing all 10! = 3,628,800 permutations.

- **Step 2: Access the Millionth Permutation**
  - Since Python uses 0-based indexing, the millionth permutation is at index `nth-1 = 999999`.
  - Access directly: `sorted_list[nth-1]` returns a tuple like `(2, 7, 8, 3, 9, 1, 5, 4, 6, 0)`.

- **Step 3: Format the Output**
  - Convert each digit to a string: `map(str, sorted_list[nth-1])`.
  - Join them together: `"".join(...)` produces a string like `"2783915460"`.

- **Efficiency:** This solution is straightforward but memory-intensive. It generates and stores all 3.6+ million permutations in memory (approximately 200-300 MB). The generation process takes several seconds, making this impractical for larger datasets but acceptable for this specific problem.

---

## Solution 2: Factorial Number System (Direct Calculation)

### Approach

- Use the **factorial number system** to directly compute the millionth permutation without generating all permutations.
- The key insight: permutations can be indexed using a mixed-radix numeral system based on factorials.
- For each digit position, use `divmod(position, factorial)` to determine which available digit to select.
- Remove selected digits from the available pool as we go.
- This computes the answer in linear time with constant memory.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Understanding the Factorial Number System**
  - Permutations can be uniquely represented using factorial-based indexing.
  - Position 0 represents the first permutation, position 1 the second, etc.
  - To find the millionth permutation, we use position `nth-1 = 999999`.

- **Step 2: Key Insight - Why `nth-1`**
  - The factorial number system is **0-indexed by mathematical definition**.
  - Position 0 maps to the first permutation (0123456789).
  - Position 1 maps to the second permutation (0123456798).
  - Position 999,999 maps to the millionth permutation.
  - This is **not** about Python's indexing. It's how the factorial number system inherently works.
  - The system encodes "how many permutations to skip" before reaching your target.

- **Step 3: The Mathematical Principle**
  - When we compute `divmod(number, factorial(k))`:
    - **Quotient**: tells us which "group" we're in (how many complete groups to skip)
    - **Remainder**: tells us our position within that group
  - The remainder at each step ranges from 0 to (factorial-1).
  - **Crucially**: remainder 0 means "first position in this group," not "no position."
  - This is a fundamental property of modular arithmetic: 0 is a valid, meaningful output.

- **Step 4: Why This Forces 0-Indexing**
  - Modulo operations inherently include 0 as a valid result representing "the first position."
  - If we tried to make remainder 0 mean "nothing," we'd lose access to the first element of each group.
  - Floor division naturally creates a 0-indexed system because:
    - 0 complete groups means you're in the first group (group 0)
    - 1 complete group means you're in the second group (group 1)
  - The multiples of factorials start at 0: positions 0, k!, 2k!, 3k!, ... mark group boundaries.

- **Step 5: Algorithm Walkthrough**
  - Start with `number = nth-1 = 999999` and `numbers = [0,1,2,3,4,5,6,7,8,9]`.
  - For the first digit:
    - `divmod(999999, 9!) = divmod(999999, 362880) = (2, 274239)`
    - Quotient 2 means: skip 2 complete groups, select from position 2 of available digits
    - Select `numbers[2] = 2`, remove it → `numbers = [0,1,3,4,5,6,7,8,9]`
    - Remainder 274239 is passed to the next level
  - For the second digit:
    - `divmod(274239, 8!) = divmod(274239, 40320) = (6, 31359)`
    - Select `numbers[6] = 7`, remove it → `numbers = [0,1,3,4,5,6,8,9]`
  - Continue this process for all 10 positions.

- **Step 6: Implementation Details**
  - The code uses a while loop: `while numbers and number:`.
  - In each iteration:
    - Compute `n = len(numbers) - 1` (the factorial size to use).
    - Get the quotient (index) and new remainder: `index, number = divmod(number, math.factorial(n))`.
    - Select and remove: `combination += str(numbers.pop(index))`.
  - When `number` becomes 0, append all remaining digits in order.

- **Step 7: Why the Remainder Propagates Correctly**
  - At each level, the remainder represents "offset within the current subgroup."
  - A remainder of 0 means "select the first permutation of this subgroup."
  - The remainder naturally provides 0-indexed positions at every recursive level.
  - This cascading property is what makes the algorithm work. The single `-1` at the start converts from ordinal counting (1st, 2nd, 3rd) to positional indexing (position 0, 1, 2).

- **Step 8: Connecting to Intuition**
  - Think of it like this analogy:
    - Question: "Give me the 3rd item"
    - System: "Items are at positions 0, 1, 2, 3..."
    - Answer: Position 2 contains the 3rd item
  - The `-1` converts between these two counting systems once, at the beginning.
  - All subsequent modulo operations maintain the 0-indexed positioning naturally.

- **Efficiency:** This solution is **dramatically more efficient** than Solution 1. It uses only constant memory (a list of 10 digits) and performs exactly 10 division operations. No permutation generation is needed. The algorithm completes essentially instantaneously.

---

## Mathematical Foundation

### The Factorial Number System

The factorial number system (also called **factoradic**) is a mixed-radix numeral system that provides a bijection between integers and permutations.

Any non-negative integer $n$ can be uniquely represented as:
$$n = a_1 \times 1! + a_2 \times 2! + a_3 \times 3! + \cdots + a_k \times k!$$

where $0 \leq a_i \leq i$ for each coefficient $a_i$.

### Mapping to Permutations

The coefficients $(a_k, a_{k-1}, \ldots, a_2, a_1)$ directly encode a permutation:
- Start with the ordered list of elements.
- For each coefficient $a_i$ (from largest to smallest):
  - Select the element at position $a_i$ from the remaining elements.
  - Remove that element from the list.
  
**Example:** For digits [0,1,2], position 4 in factorial number system:
- $4 = 2 \times 2! + 0 \times 1!$, giving coefficients $(2, 0)$
- Start with [0,1,2]
- Coefficient 2: select index 2 → digit 2, remaining [0,1]
- Coefficient 0: select index 0 → digit 0, remaining [1]
- Result: 201 (the 5th permutation, at 0-indexed position 4)

### Why 0-Indexing is Fundamental

The factorial number system representation of 0 is:
$$0 = 0 \times 1! + 0 \times 2! + 0 \times 3! + \cdots$$

This gives coefficients $(0, 0, 0, \ldots)$, which encodes the permutation formed by:
- Selecting index 0 at each step
- Always choosing the first available element
- Result: the sorted order (0123456789)

This is **mathematically defined** as the first permutation. The system cannot start at 1 because:
1. The factoradic representation naturally begins at 0
2. The coefficients can be 0 (representing "first choice")
3. Modular arithmetic produces 0 as a valid output

### The Divmod Operation Explained

When we compute `divmod(n, k!)`:
- **Mathematical meaning**: "Organize positions into groups of size k!"
- **Quotient q**: "I've completed q groups" → I'm in group q (0-indexed)
- **Remainder r**: "I'm at offset r within my group" → position r (0-indexed)

**Example**: `divmod(7, 3) = (2, 1)` with items organized in groups of 3:
```
Group 0: positions 0, 1, 2
Group 1: positions 3, 4, 5
Group 2: positions 6, 7, 8
```
Position 7 is in group 2 (completed 2 full groups), at offset 1 within that group.

### Why Single Subtraction Works

The conversion from ordinal to positional happens **once** at the beginning with `number = nth - 1`.

After that, every modulo operation maintains the 0-indexed structure naturally because:
- **Remainders inherently start at 0**: The output of `n % k` ranges from 0 to k-1
- **Floor division counts completed groups**: `n // k` counts how many full groups fit before reaching n
- **Group boundaries are multiples**: Positions 0, k, 2k, 3k, ... start new groups

This is not an implementation detail. It's a mathematical property of modular arithmetic and factorial number systems.

---

## Comparison of Solutions

| Aspect | Solution 1<br>(Generate All) | Solution 2<br>(Factorial System) |
|--------|------------------------------|----------------------------------|
| **Approach** | Generate all permutations | Direct calculation |
| **Memory Usage** | ~200-300 MB | Constant (~100 bytes) |
| **Permutations Generated** | 3,628,800 (all) | 0 (none) |
| **Operations** | Millions of swaps | 10 divisions |
| **Speed** | Several seconds | Instantaneous |
| **Dependencies** | itertools | math |
| **Scalability** | Poor (memory limited) | Excellent |
| **Mathematical Insight** | None required | Factorial number system |
| **Best For** | Small problems, learning | Optimal efficiency |

---

## Output

```
2783915460
```

---

## Notes

- The millionth lexicographic permutation of the digits 0-9 is **2783915460**.
- **Solution 2** is the optimal approach, demonstrating the power of mathematical number systems to solve combinatorial problems efficiently.
- The factorial number system provides an elegant bijection between integers and permutations, enabling direct access to any permutation without generation.
- The **critical insight** about 0-indexing: it's not an arbitrary choice but a fundamental property of how modular arithmetic and the factorial number system work. The remainder can be 0, and this must represent a valid position (the first one in each group).
- Understanding why `nth-1` works requires grasping that the entire system operates in 0-indexed space by mathematical necessity, not convention.
- For the general problem of finding the $n$-th permutation of $k$ elements, Solution 2's approach scales to any size while Solution 1 becomes impractical for $k > 12$ (due to memory constraints).
- The algorithm in Solution 2 can be modified to work in reverse: given a permutation, compute its position in lexicographic order using the same factorial number system.
- This problem beautifully illustrates how understanding the mathematical structure of a problem can lead to solutions that are orders of magnitude more efficient than brute force approaches.
