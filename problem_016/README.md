# Problem 16: Power Digit Sum

**Problem source:** [Project Euler Problem 16](https://projecteuler.net/problem=16)

**Problem statement:**

$2^{15} = 32768$ and the sum of its digits is $3 + 2 + 7 + 6 + 8 = 26$.

What is the sum of the digits of the number $2^{1000}$?

---

## Solution 1: Arithmetic Digit Extraction (Modulo Method)

### Approach

- Calculate $2^{1000}$ using Python's built-in exponentiation operator `**`.
- Extract each digit using **modulo and integer division** operations.
- Use the pattern: extract the last digit with `number % 10`, then remove it with `number //= 10`.
- Accumulate the sum of all digits.
- This approach uses pure arithmetic operations without string conversion.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Calculate the Power**
  - Python's `2**1000` computes $2^{1000}$ exactly.
  - Python natively supports **arbitrary-precision integers**, allowing it to handle the 302-digit result without overflow.
  - Unlike languages with fixed-size integers (C, Java, JavaScript), Python transparently handles arbitrarily large numbers.

- **Step 2: Digit Extraction Loop**
  - The `while number > 0:` loop continues until all digits are processed.
  - **Extract last digit:** `number % 10` gives the remainder when dividing by 10, which is the rightmost digit.
  - **Accumulate:** Add this digit to the running sum with `answer += number % 10`.
  - **Remove last digit:** `number //= 10` performs integer division by 10, effectively shifting all digits right by one position.

- **Step 3: Example Walkthrough**
  - For $2^{15} = 32768$:
    - First iteration: `32768 % 10 = 8`, `answer = 8`, `number = 3276`
    - Second iteration: `3276 % 10 = 6`, `answer = 14`, `number = 327`
    - Continue until all digits are extracted: final `answer = 26`

- **Efficiency:** This solution processes each digit exactly once using simple arithmetic operations. No memory allocation for strings is required, making it very efficient. The algorithm works from right to left, extracting digits in reverse order, but since we're only summing them, the order doesn't matter.

---

## Solution 2: String Conversion with Generator Expression

### Approach

- Calculate $2^{1000}$ using Python's bit-shift operator `<<` (left shift).
- Convert the result to a string to access individual digit characters.
- Use a **generator expression** to iterate through each character, convert it back to an integer, and sum all digits.
- This approach leverages Python's strength in string manipulation.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Calculate Using Bit Shift**
  - `1 << 1000` is equivalent to `1 * 2^1000` or simply `2^1000`.
  - The **left shift operator** `<<` shifts the binary representation left by the specified number of positions.
  - Shifting left by $n$ positions is equivalent to multiplying by $2^n$.
  - Example: `1 << 3` = `0b1 << 3` = `0b1000` = `8` = $2^3$

- **Step 2: Convert to String**
  - `str(1 << 1000)` converts this large integer to a string representation.
  - For example, $2^{15} = 32768$ becomes the string `"32768"`.

- **Step 3: Generator Expression**
  - The expression `int(d) for d in str(1 << 1000)` creates a generator that:
    - Iterates through each character `d` in the string.
    - Converts each character back to an integer with `int(d)`.
    - For `"32768"`, this yields: `3, 2, 7, 6, 8`.

- **Step 4: Sum the Digits**
  - Python's built-in `sum()` function consumes the generator and adds all values.
  - This produces the final digit sum in a single, concise line.

- **Efficiency:** This solution is highly readable and Pythonic. The string conversion has minimal overhead for numbers of this size, and the generator expression ensures memory efficiency by not creating an intermediate list. The bit-shift operator is slightly more efficient than `**` for powers of 2.

---

## Solution 3: String Conversion with `map()` and Bit Shift

### Approach

- Calculate $2^{1000}$ using Python's bit-shift operator `<<`.
- Convert the result to a string, then use `map()` to apply `int()` to each character.
- Sum the resulting integers to get the digit sum.
- This approach is functionally identical to Solution 2 but uses `map()` instead of a generator expression.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Calculate Using Bit Shift**
  - `1 << 1000` efficiently computes $2^{1000}$ using bit manipulation.

- **Step 2: Convert to String**
  - `str(1 << 1000)` converts this to a string.

- **Step 3: Map Function**
  - `map(int, str(1 << 1000))` applies the `int` function to each character in the string.
  - The `map()` function returns a map object (an iterator) that yields converted integers.
  - This is equivalent to the generator expression in Solution 2 but uses a different syntax.

- **Step 4: Sum the Results**
  - `sum()` consumes the map object and adds all integer values.
  - The entire solution fits in a single line: `print(sum(map(int, str(1 << 1000))))`

- **Efficiency:** Performance is virtually identical to Solution 2. The choice between `map()` and a generator expression is largely a matter of style preference. The one-liner format demonstrates Python's expressiveness for concise problem-solving.

---

## Solution 4: Divmod Method with Power Operator

### Approach

- Calculate $2^{1000}$ using Python's exponentiation operator `**`.
- Use Python's `divmod()` function to extract digits more elegantly.
- `divmod(number, 10)` returns both the quotient and remainder in a single operation.
- This provides clearer intent than separate modulo and division operations.

**Reference:** The full Python implementation is available in [`solution_4.py`](solution_4.py).

### Detailed Explanation

- **Step 1: Calculate the Power**
  - `2**1000` computes $2^{1000}$ using the standard exponentiation operator.

- **Step 2: Divmod-Based Extraction**
  - The `while number:` loop continues while `number` is non-zero (more Pythonic than `while number > 0:`).
  - `divmod(number, 10)` returns a tuple `(quotient, remainder)`:
    - **Quotient:** `number // 10` (the number with the last digit removed)
    - **Remainder:** `number % 10` (the last digit)
  - The unpacking `number, digit = divmod(number, 10)` simultaneously:
    - Updates `number` to the quotient (removing the last digit)
    - Stores the extracted digit in `digit`

- **Step 3: Accumulate the Sum**
  - Add each extracted `digit` to the running `answer`.

- **Step 4: Why `divmod()` is Better**
  - **Clarity:** The intent (extract digit and update number) is explicit in one line.
  - **Efficiency:** Computes both quotient and remainder in a single operation rather than two separate operations.
  - **Pythonic:** Using `divmod()` for this pattern is idiomatic Python.

- **Efficiency:** This solution is marginally more efficient than Solution 1 because `divmod()` computes both the quotient and remainder in a single internal operation, though the performance difference is negligible for this problem size.

---

## Comparison of Solutions

| Aspect | Solution 1<br>(Modulo) | Solution 2<br>(Generator) | Solution 3<br>(Map) | Solution 4<br>(Divmod) |
|--------|----------------------|--------------------------|---------------------|----------------------|
| **Power Calculation** | `**` operator | `<<` bit shift | `<<` bit shift | `**` operator |
| **Digit Extraction** | `%` and `//` | `str()`, generator | `str()`, `map()` | `divmod()` |
| **Code Length** | 5 lines | 1 line | 1 line | 5 lines |
| **Readability** | Moderate | High | High | High |
| **Pythonic Style** | Traditional | Very Pythonic | Functional style | Idiomatic |
| **Memory** | Minimal | String storage | String storage | Minimal |
| **Best For** | Avoiding strings | Conciseness | One-liner fans | Clean arithmetic |

---

## Output

```
1366
```

---

## Mathematical Notes

### Size of $2^{1000}$

- The number $2^{1000}$ has exactly **302 digits**.
- This can be calculated using logarithms:
  $$\text{Number of digits} = \lfloor \log_{10}(2^{1000}) \rfloor + 1 = \lfloor 1000 \cdot \log_{10}(2) \rfloor + 1$$
- Since $\log_{10}(2) \approx 0.30103$:
  $$\lfloor 1000 \times 0.30103 \rfloor + 1 = \lfloor 301.03 \rfloor + 1 = 302$$

### The Wheat and Chessboard Problem

This problem is reminiscent of the ancient fable about the inventor of chess who asked a king for one grain of rice on the first square of a chessboard, two on the second, four on the third, and so on, doubling each time. The final square would contain more than 461 billion tonnes of grain, illustrating the explosive growth of exponential functions.

### Expected Digit Sum

- For large numbers, if digits were uniformly distributed from 0-9, the expected value per digit would be:
  $$\frac{0 + 1 + 2 + \cdots + 9}{10} = 4.5$$
- For a 302-digit number, we'd expect approximately:
  $$302 \times 4.5 = 1359$$
- The actual sum is $1366$, which is very close to this theoretical expectation, suggesting that the digits of $2^{1000}$ are relatively well-distributed.

### Bit Shift vs. Exponentiation

- For powers of 2, the bit-shift operator `<<` is more efficient than `**`:
  - `1 << 1000` is equivalent to `2**1000` but uses bit manipulation.
  - Bit shifts are fundamental CPU operations and can be slightly faster.
  - However, for arbitrary-precision arithmetic in Python, the difference is minimal.

### Why Python is Ideal for This Problem

- **Arbitrary-Precision Arithmetic:** Python's `int` type can represent integers of any size, limited only by available memory.
- **No Overflow:** Unlike C (64-bit max: $2^{63}-1$) or JavaScript ($2^{53}-1$), Python handles $2^{1000}$ transparently.
- **Built-in Operations:** Both `**` and `<<` operators work seamlessly with large integers.

---

## Notes

- The sum of the digits in $2^{1000}$ is **1366**.
- All four solutions are efficient for this problem size. The choice between them depends on personal preference and coding style:
  - **Solutions 1 & 4** avoid string conversion and use pure arithmetic.
  - **Solutions 2 & 3** leverage Python's string handling for concise, readable code.
- **Solutions 2 & 3** are the most concise, each fitting on a single line.
- **Solution 4** demonstrates the elegant use of `divmod()` for digit extraction, a common pattern in Python programming.
- The bit-shift operator `<<` is a clever optimization for powers of 2, though the performance gain is minimal for this specific problem.
- This problem demonstrates Python's strength in handling arbitrarily large integers, making it an ideal language for Project Euler problems involving big numbers.
