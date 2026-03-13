# Problem 30: Digit Fifth Powers

**Problem source:** [Project Euler Problem 30](https://projecteuler.net/problem=30)

**Problem statement:**

Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:

$$1634 = 1^4 + 6^4 + 3^4 + 4^4$$
$$8208 = 8^4 + 2^4 + 0^4 + 8^4$$
$$9474 = 9^4 + 4^4 + 7^4 + 4^4$$

As $1 = 1^4$ is not a sum it is not included.

The sum of these numbers is $1634 + 8208 + 9474 = 19316$.

**Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.**

---

## Solution 1: Brute-Force with Computed Upper Bound

### Approach

- Derive a finite upper bound by finding the largest digit count $d$ for which the maximum achievable fifth-power digit sum can still reach a $d$-digit number (see **Mathematical Foundation: Proving the Upper Bound** for the full derivation).
- Scan every integer from 2 up to that upper bound, testing each number directly.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Computing the upper bound (the digit-ceiling loop)**

```python
power = 5
digits = 1
max_sum = digits*(9**power)

while(max_sum > 10**(digits-1)):
    digits += 1
    max_sum = digits*(9**power)
```

  This loop finds the first digit count $d$ for which the maximum possible fifth-power digit sum can no longer reach the smallest $d$-digit number. On each iteration:
  - `digits*(9**power)` is the maximum digit sum achievable (every digit is 9).
  - `10**(digits-1)` is the smallest number with that many digits.

  The loop exits with `digits = 7` because that is the first value where the condition fails. See the table in the **Mathematical Foundation** for the full breakdown of each digit count.

- **Step 2: Setting the upper bound**

```python
upper_bound = (digits-1)*(9**power)
```

  Since `digits` ends at 7 (the first *impossible* digit count), stepping back by one gives the last *possible* count: 6. The upper bound is therefore $6 \times 9^5 = 354{,}294$.

- **Step 3: Brute-force scan**

```python
result = sum(n for n in range(2, upper_bound+1)
             if sum(int(d)**power for d in str(n)) == n)
```

  For every candidate `n` from 2 to the upper bound, the inner expression converts `n` to a string, raises each digit character to the fifth power, and sums the results. Starting at 2 excludes the trivial case $1 = 1^5$.

- **Efficiency:** This solution scans ~354,000 candidates. For each one it converts the number to a string and recomputes `d**5` for every digit from scratch; the same digit may be raised to the fifth power thousands of times across the full scan. It is the simplest approach but recomputes powers redundantly.

---

## Solution 2: Brute-Force with Precomputed Power Lookup

### Approach

- Compute the upper bound using the identical digit-ceiling loop as Solution 1.
- Before scanning, precompute the fifth power of every digit (0–9) once and store the results in a dictionary keyed by digit character.
- Replace the per-digit exponentiation in the inner loop with an O(1) dictionary lookup.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Same upper bound loop as Solution 1**

```python
power = 5
digits = 1
max_sum = digits*(9**power)

while(max_sum > 10**(digits-1)):
    digits += 1
    max_sum = digits*(9**power)
upper_bound = (digits-1)*(9**power)
```

  This produces `upper_bound = 354,294` for the same reasons described in Solution 1.

- **Step 2: Precompute the power map**

```python
p = {str(d): d**power for d in range(10)}
```

  This dictionary maps each digit *character* (`'0'` through `'9'`) to its fifth power. The key type is a string because iterating over `str(n)` yields character strings. The ten powers are computed exactly once at startup.

- **Step 3: Scan using dictionary lookup**

```python
result = sum(n for n in range(2, upper_bound+1)
             if sum(p[d] for d in str(n)) == n)
```

  The inner sum now reads from `p` via a dictionary lookup instead of calling `int(d)**power`. The scanning logic is otherwise identical to Solution 1.

- **Why this is faster:** A dictionary lookup is an O(1) hash operation. Raising an integer to the fifth power is a multiplication chain. Over ~354,000 candidates each with up to 6 digits, replacing roughly 2 million exponentiations with 2 million hash lookups is a measurable constant-factor improvement, even if the asymptotic complexity is the same.

---

## Solution 3: Combinatorial Multiset Enumeration

### Approach

- Observe that the fifth-power digit sum is the same for all permutations of a digit multiset (addition is commutative). Rather than iterating over numbers, iterate over **multisets of digits** (their canonical sorted representatives) and check whether the fifth-power sum of each multiset equals a number that has exactly those digits.
- This collapses the search space from ~354,000 candidates down to 7,997 multisets, a reduction of roughly 44x.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Precompute power list and upper bound**

```python
from itertools import combinations_with_replacement
result = 0
power = 5
digits = 1
max_sum = digits*(9**power)
p = [d**power for d in range(10)]

while(max_sum > 10**(digits-1)):
    digits += 1
    max_sum = digits*(9**power)
```

  The same digit-ceiling loop determines that `digits = 7` is the first impossible digit count, so we enumerate multisets of length 2 through 6 (`range(2, digits)` = `range(2, 7)`). The power list `p` uses integer indices (0–9), since `combinations_with_replacement(range(10), length)` yields integer tuples.

- **Step 2: Enumerate multisets and verify**

```python
for length in range(2, digits):
    for combo in combinations_with_replacement(range(10), length):
        s = sum(p[d] for d in combo)
        if s-1 and sorted(int(d) for d in str(s)) == list(combo):
            result += s
```

  For each multiset `combo`:
  - **Compute `s`:** sum the fifth powers of each digit in the multiset. This is the candidate number.
  - **Verify:** extract the digits of `s`, sort them, and compare to the (already sorted) `combo` tuple. Both sides must be equal for `s` to qualify (see **Mathematical Foundation: The Sorted-Digits Invariant** for a full explanation of why this check is both necessary and sufficient).
  - **Guard `s-1`:** equivalent to `s != 1`, which excludes the trivial case $1 = 1^5$ without a separate if-statement.

- **Search space:** The total number of multisets across all lengths is:

| Length | Formula | Multisets |
|--------|---------|-----------|
| 2 | $\binom{11}{2}$ | 55 |
| 3 | $\binom{12}{3}$ | 220 |
| 4 | $\binom{13}{4}$ | 715 |
| 5 | $\binom{14}{5}$ | 2,002 |
| 6 | $\binom{15}{6}$ | 5,005 |
| **Total** | | **7,997 vs ~354,000 numbers** |

---

## Mathematical Foundation

### Proving the Upper Bound

The upper bound is the most important insight in this problem. It turns what would otherwise be an infinite search into a finite one. The core question is: for how many digits $d$ can a number possibly equal its own fifth-power digit sum?

Define:
- **Smallest $d$-digit number:** $10^{d-1}$
- **Maximum fifth-power digit sum for $d$ digits:** $d \times 9^5 = d \times 59{,}049$

For a $d$-digit number to possibly satisfy the condition, the maximum achievable digit sum must be at least as large as the smallest $d$-digit number:

$$d \times 9^5 \geq 10^{d-1}$$

When this inequality fails, no $d$-digit number can satisfy the problem. The digit-ceiling loop in all three solutions finds exactly the first $d$ where this fails:

| $d$ | $d \times 9^5$ (max sum) | $10^{d-1}$ (min $d$-digit) | Possible? |
|-----|--------------------------|----------------------------|-----------|
| 1 | 59,049 | 1 | ✓ |
| 2 | 118,098 | 10 | ✓ |
| 3 | 177,147 | 100 | ✓ |
| 4 | 236,196 | 1,000 | ✓ |
| 5 | 295,245 | 10,000 | ✓ |
| 6 | 354,294 | 100,000 | ✓ |
| **7** | **413,343** | **1,000,000** | **✗** |

At $d = 7$, the maximum achievable sum (413,343) is less than the smallest 7-digit number (1,000,000). The while loop exits with `digits = 7` because this is the first value for which `max_sum > 10**(digits-1)` is false.

The upper bound is then set to $(7-1) \times 9^5 = 6 \times 59{,}049 = 354{,}294$. A subtle but important point: the loop exits at `digits = 7`, but the upper bound uses `digits - 1 = 6`. After the loop, `digits` holds the *first impossible* digit count, so we must subtract 1 to get the last *possible* one. Any number satisfying the condition must be $\leq 354{,}294$.

This bound generalises directly to any power $k$: the digit-ceiling loop terminates because $d \times 9^k$ grows linearly in $d$ while $10^{d-1}$ grows exponentially, so the exponential always wins eventually.

### The Sorted-Digits Invariant

The heart of Solution 3's efficiency is the observation that the fifth-power digit sum is an **invariant** over all permutations of a digit multiset. Because addition is commutative, every arrangement of the digits $\{d_1, d_2, \ldots, d_k\}$ gives the same sum:

$$d_1^5 + d_2^5 + d_3^5 = d_2^5 + d_1^5 + d_3^5 = d_3^5 + d_1^5 + d_2^5 = \cdots$$

There is therefore no value in checking all permutations separately, as they all produce the same candidate number. Instead, we enumerate only the **canonical sorted representative** of each multiset exactly once, using `combinations_with_replacement`. This is how the search space shrinks from ~354,000 to 7,997.

The verification line `sorted(int(d) for d in str(s)) == list(combo)` enforces a two-way contract:

1. We picked a sorted digit tuple (`combo`) and computed a sum `s`.
2. We ask: when we look at `s` as a number and sort its digits, do we recover exactly `combo`?
3. Since `combo` is already in non-decreasing order by construction (guaranteed by `combinations_with_replacement`), and `sorted()` normalises the digits of `s` into the same form, this single comparison simultaneously verifies that `s` has the **right number of digits** and the **right digit values**.

A worked example with the known answer 4150:

```
combo = (0, 1, 4, 5)               # from combinations_with_replacement
s = 0⁵ + 1⁵ + 4⁵ + 5⁵
  = 0 + 1 + 1024 + 3125 = 4150

str(4150)                          →  "4150"
sorted(int(d) for d in "4150")     →  [0, 1, 4, 5]
list((0, 1, 4, 5))                 →  [0, 1, 4, 5]   ✓  match
```

A failing example that illustrates the digit-count check:

```
combo = (9, 9, 9)                  # 3-digit multiset
s = 9⁵ + 9⁵ + 9⁵ = 177,147        # but s has 6 digits!

sorted digits of 177147            →  [1, 1, 1, 4, 7, 7]
list((9, 9, 9))                    →  [9, 9, 9]
                                       ✗  length mismatch → rejected
```

Because each number has a unique sorted digit fingerprint, and `combinations_with_replacement` generates every possible sorted fingerprint exactly once, every qualifying number is found exactly once: no duplicates, nothing missed.

### Why There Is No Information Loss

A natural concern with Solution 3 is: could two different multisets produce the same sum $s$? If so, might the algorithm only check $s$ against one of them and miss a valid match?

This concern is unfounded. The verification step checks whether the sum's own sorted digit fingerprint equals the *specific multiset that produced it*. So even if multiset A and multiset B happen to produce the same numerical sum $s$, the check will succeed only for whichever multiset matches the actual digits of $s$, and fail for the other. No qualifying number can be missed. The only structural assumption the algorithm relies on is commutativity (that the sum does not depend on digit order), and this is a basic property of integer addition.

---

## Comparison of Solutions

| Aspect | Solution 1 (Brute-Force) | Solution 2 (Precomputed Map) | Solution 3 (Multiset Enumeration) |
|--------|--------------------------|------------------------------|-----------------------------------|
| **Approach** | Scan all numbers 2 to 354,294 | Same scan, lookup table | Enumerate digit multisets |
| **Upper bound method** | Digit-ceiling loop | Same digit-ceiling loop | Same digit-ceiling loop |
| **Search space** | ~354,000 numbers | ~354,000 numbers | 7,997 multisets |
| **Power computation** | `int(d)**power` per digit | `dict` lookup `p[d]` | `list` lookup `p[d]` |
| **Key insight used** | Upper bound only | Upper bound + caching | Commutativity + invariant |
| **Duplicates possible?** | No (each number once) | No (each number once) | No (each multiset once) |
| **Best for** | Readable baseline | Constant-factor gain | Optimal search space |

---

## Output

```
443839
```

---

## Notes

- The six numbers satisfying the condition are: $4150,\ 4151,\ 54748,\ 92727,\ 93084,\ 194979$. Their sum is $443{,}839$.
- **Solution 1** is the clearest baseline. Each number is checked independently with no setup cost beyond the upper bound loop.
- **Solution 2** is a drop-in upgrade to Solution 1: replace per-digit exponentiation with a dictionary lookup built once before the scan. The ten precomputed values are reused across every candidate.
- **Solution 3** is the most algorithmically interesting. Reducing 354,000 candidates to 7,997 multisets by exploiting the commutativity of addition is a genuine insight rather than a constant-factor tweak. The sorted-digits invariant is the mechanism that makes the reduction both correct and complete.
- All three solutions share the same digit-ceiling loop for computing the upper bound. This loop generalises directly to any power $k$: change `power = 5` to `power = k` and the bound is found automatically.
- The problem generalises cleanly: to find numbers equal to the sum of their $k$-th powers, change `power = 5` everywhere. The upper bound loop and Solution 3's multiset approach both adapt without modification.
