# Problem 20: Factorial Digit Sum

**Problem source:** [Project Euler Problem 20](https://projecteuler.net/problem=20)

**Problem statement:**

$n!$ means $n \times (n-1) \times \cdots \times 3 \times 2 \times 1$.

For example, $10! = 10 \times 9 \times \cdots \times 3 \times 2 \times 1 = 3628800$, and the sum of the digits in the number $10!$ is $3 + 6 + 2 + 8 + 8 + 0 + 0 = 27$.

Find the sum of the digits in the number $100!$.

---

## Solution 1: Arithmetic Digit Extraction (Modulo Method)

### Approach

- Calculate $100!$ using Python's built-in `math.factorial()` function.
- Extract each digit using **modulo and integer division** operations.
- Use the pattern: extract the last digit with `number % 10`, then remove it with `number //= 10`.
- Accumulate the sum of all digits.
- This approach uses pure arithmetic operations without string conversion.

**Reference:** The full Python implementation is available in [`solution_1.py`](solution_1.py).

### Detailed Explanation

- **Step 1: Calculate the Factorial**
  - Python's `math.factorial(100)` computes $100!$ exactly.
  - Python natively supports **arbitrary-precision integers**, allowing it to handle the 158-digit result without overflow.

- **Step 2: Digit Extraction Loop**
  - The `while number > 0:` loop continues until all digits are processed.
  - **Extract last digit:** `number % 10` gives the remainder when dividing by 10, which is the rightmost digit.
  - **Accumulate:** Add this digit to the running sum with `answer += number % 10`.
  - **Remove last digit:** `number //= 10` performs integer division by 10, effectively shifting all digits right by one position.

- **Step 3: Example Walkthrough**
  - For $10! = 3628800$:
    - First iteration: `3628800 % 10 = 0`, `answer = 0`, `number = 362880`
    - Second iteration: `362880 % 10 = 0`, `answer = 0`, `number = 36288`
    - Continue until all digits are extracted: final `answer = 27`

- **Efficiency:** This solution processes each digit exactly once using simple arithmetic operations. No memory allocation for strings is required, making it very efficient.

---

## Solution 2: String Conversion Method

### Approach

- Calculate $100!$ using Python's built-in `math.factorial()` function.
- Convert the result to a string to access individual digit characters.
- Use a **generator expression** to iterate through each character, convert it back to an integer, and sum all digits.
- This approach leverages Python's strength in string manipulation.

**Reference:** The full Python implementation is available in [`solution_2.py`](solution_2.py).

### Detailed Explanation

- **Step 1: Calculate and Convert**
  - `math.factorial(100)` computes $100!$ as an integer.
  - `str(math.factorial(100))` converts this large integer to a string representation.
  - For example, $10! = 3628800$ becomes the string `"3628800"`.

- **Step 2: Generator Expression**
  - The expression `int(d) for d in str(math.factorial(100))` creates a generator that:
    - Iterates through each character `d` in the string.
    - Converts each character back to an integer with `int(d)`.
    - For `"3628800"`, this yields: `3, 6, 2, 8, 8, 0, 0`.

- **Step 3: Sum the Digits**
  - Python's built-in `sum()` function consumes the generator and adds all values.
  - This produces the final digit sum in a single, concise line.

- **Efficiency:** This solution is highly readable and Pythonic. The string conversion has minimal overhead for numbers of this size, and the generator expression ensures memory efficiency by not creating an intermediate list.

---

## Solution 3: String Conversion with `map()`

### Approach

- Calculate $100!$ using Python's built-in `math.factorial()` function.
- Convert the result to a string, then use `map()` to apply `int()` to each character.
- Sum the resulting integers to get the digit sum.
- This approach is functionally identical to Solution 2 but uses `map()` instead of a generator expression.

**Reference:** The full Python implementation is available in [`solution_3.py`](solution_3.py).

### Detailed Explanation

- **Step 1: Calculate and Convert**
  - `math.factorial(100)` computes $100!$ as an integer.
  - `str(math.factorial(100))` converts this to a string.

- **Step 2: Map Function**
  - `map(int, str(math.factorial(100)))` applies the `int` function to each character in the string.
  - The `map()` function returns a map object (an iterator) that yields converted integers.
  - This is equivalent to the generator expression in Solution 2 but uses a different syntax.

- **Step 3: Sum the Results**
  - `sum()` consumes the map object and adds all integer values.

- **Efficiency:** Performance is virtually identical to Solution 2. The choice between `map()` and a generator expression is largely a matter of style preference. Some find `map()` more concise, while others prefer the explicit generator syntax.

---

## Solution 4: Divmod Method

### Approach

- Calculate $100!$ using Python's built-in `math.factorial()` function.
- Use Python's `divmod()` function to extract digits more elegantly.
- `divmod(number, 10)` returns both the quotient and remainder in a single operation.
- This provides clearer intent than separate modulo and division operations.

**Reference:** The full Python implementation is available in [`solution_4.py`](solution_4.py).

### Detailed Explanation

- **Step 1: Calculate the Factorial**
  - `math.factorial(100)` computes $100!$.

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
| **Approach** | Arithmetic extraction | String conversion | String conversion | Arithmetic extraction |
| **Operations** | `%` and `//` | `str()`, generator | `str()`, `map()` | `divmod()` |
| **Readability** | Moderate | High | High | High |
| **Pythonic Style** | Traditional | Very Pythonic | Functional style | Idiomatic |
| **Memory** | Minimal | String storage | String storage | Minimal |
| **Best For** | Avoiding strings | Conciseness | Functional programming | Clean arithmetic |

---

## Output

```
648
```

---

## Mathematical Notes

### Size of 100!

- The number $100!$ has exactly **158 digits**.
- This can be approximated using **Stirling's approximation**:
  $$\log_{10}(n!) \approx n \log_{10}(n) - n \log_{10}(e) + \frac{1}{2} \log_{10}(2\pi n)$$
- For $n = 100$:
  $$\log_{10}(100!) \approx 100 \times 2 - 100 \times 0.434 + 0.5 \times \log_{10}(200\pi) \approx 157.97$$
- Therefore, $100!$ has $\lfloor 157.97 \rfloor + 1 = 158$ digits.

### Average Digit Value

- For large factorials, the digits become effectively random in their distribution.
- The expected value of a uniformly random digit from 0-9 is:
  $$\frac{0 + 1 + 2 + \cdots + 9}{10} = 4.5$$
- Therefore, we expect the digit sum to be approximately:
  $$158 \times 4.5 = 711$$
- The actual sum is $648$, which is reasonably close to this theoretical expectation.

### Why Python is Ideal for This Problem

- **Arbitrary-Precision Arithmetic:** Python's `int` type can represent integers of any size, limited only by available memory.
- **Built-in Factorial:** The `math.factorial()` function is implemented in C and highly optimized.
- **No Overflow:** Unlike languages with fixed-size integers (e.g., C, Java), Python handles large numbers transparently.

---

## Notes

- The sum of the digits in $100!$ is **648**.
- All four solutions are efficient for this problem size. The choice between them depends on personal preference and coding style:
  - **Solutions 1 & 4** avoid string conversion and use pure arithmetic.
  - **Solutions 2 & 3** leverage Python's string handling for concise, readable code.
- **Solution 2** is arguably the most Pythonic, combining clarity with brevity.
- **Solution 4** demonstrates the elegant use of `divmod()` for digit extraction, a common pattern in Python programming.
- This problem demonstrates that sometimes the most straightforward approach (computing the factorial and summing digits) is both correct and efficient, requiring no advanced algorithmic optimization.

### Relationship to Problem 16

- **Problem 16** asks for the sum of digits in $2^{1000}$, while **Problem 20** asks for the sum of digits in $100!$.
- The digit extraction techniques are **identical** across both problems - only the initial calculation differs.
- Both problems demonstrate Python's strength in handling arbitrary-precision integers.
- If you've solved Problem 16, you already know all four techniques needed for Problem 20 (and vice versa).
