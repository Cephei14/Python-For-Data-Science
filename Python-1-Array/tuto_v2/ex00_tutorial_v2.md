# Study Tutorial — Exercise 00: give_bmi.py

## 1. Exercise Overview

**What it asks:**
Create a module named `give_bmi.py` in directory `ex00/` containing two functions:
1. `give_bmi(height: list[int | float], weight: list[int | float]) -> list[int | float]:`
   - Accepts two lists: heights (in meters) and weights (in kilograms).
   - Computes the Body Mass Index (BMI) pairwise for each person using the formula:
     $$\text{BMI} = \frac{\text{weight}}{\text{height}^2}$$
   - Returns a **plain Python list** of calculated BMI values (`list[int | float]`).
2. `apply_limit(bmi: list[int | float], limit: int) -> list[bool]:`
   - Accepts a list of BMI values and an integer threshold `limit`.
   - Returns a list of booleans indicating whether each BMI value is strictly greater than the limit (`True` if above `limit`, `False` otherwise).

**Rules and Constraints:**
- Must handle all error cases gracefully (mismatched list lengths, non-numeric values, empty lists, non-list arguments, non-positive numbers).
- Return type for `give_bmi` must be `<class 'list'>`, not a NumPy array.
- Must follow 42 Python Norm rules: PEP 8 / `flake8` compliance, function docstrings (`__doc__`), type annotations, no global variables, no code in global scope, and a `main()` function with clean exception handling.

**Main concepts you'll learn:**
- Pairwise (elementwise) computation across multiple lists using `zip()`.
- Building boolean masks (the foundation for NumPy boolean indexing).
- Strict type and value validation in Python (distinguishing `bool` from `int`).
- Bridging standard Python data structures with array/vectorized paradigms.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **Module 0 Basic Types (ex00, ex02):** Working with integers, floats, and Python lists.
- **Boolean Gotchas (Module 0 ex03):** In Python, `bool` is a subclass of `int` (`isinstance(True, int)` is `True`). Strict validation requires filtering out booleans.
- **List Comprehensions (Module 0 ex06):** Constructing new lists concisely with `[f(x) for x in seq]`.
- **Assertions & Error Handling (Module 0 ex04, ex05):** Raising and catching exceptions (`AssertionError`, `ValueError`, `TypeError`) inside `main()`.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `zip(height, weight)` | Iterates through multiple sequences simultaneously element by element | Stops at the shortest iterable if lengths differ |
| `[w / (h ** 2) for h, w in zip(...)]` | Computes pairwise BMI values concisely | Standard Python list comprehension |
| `[val > limit for val in bmi]` | Generates a boolean mask based on a threshold | Returns a list of booleans |
| `isinstance(x, (int, float))` | Checks if a variable is an int or float | Beware: returns `True` for booleans! |
| `type(x) in (int, float)` | Strict numeric type check | Properly excludes `bool` without extra flags |
| `numpy` (allowed) | High-performance array library | If used internally, results must be converted back to `list` |

**Common pitfalls:**
- **Operator Precedence in the BMI Formula:** Writing `weight / height ** 2` works because `**` binds tighter than `/`, but writing `weight / (height * height)` or `w / (h ** 2)` is much safer and avoids ambiguity.
- **Returning a NumPy Array instead of a Python List:** The subject tester explicitly checks `print(bmi, type(bmi))` and expects `<class 'list'>`. If you use `np.array`, you must call `.tolist()`.
- **Silent Truncation by `zip`:** In Python, `zip([1, 2], [10, 20, 30])` silently stops after 2 elements. You must explicitly verify `len(height) == len(weight)` before processing!
- **Boolean Sneakiness:** In Python, `isinstance(False, int)` is `True`! If an input contains `[True, 1.8]`, arithmetic works but the input is logically invalid. Check `type(x) is not bool`.
- **Division by Zero:** Heights $\le 0$ cause a `ZeroDivisionError` or produce negative BMI. Validate that heights and weights are strictly positive numbers.

---

## 4. Concepts You Need to Learn

### 4.1 The Body Mass Index (BMI) Formula
BMI is a standard health metric:
$$\text{BMI} = \frac{\text{weight (kg)}}{(\text{height (m)})^2}$$
For example, for a height of $1.80\text{ m}$ and weight of $75\text{ kg}$:
$$\text{BMI} = \frac{75}{1.80^2} = \frac{75}{3.24} \approx 23.148$$

### 4.2 Pairwise Iteration with `zip()`
When you have two parallel lists and need to compute something using the $i$-th element of each, use `zip()`:
```python
heights = [2.71, 1.15]
weights = [165.3, 38.4]

for h, w in zip(heights, weights):
    print(f"h={h}, w={w} -> BMI = {w / (h ** 2)}")
```
Output:
```
h=2.71, w=165.3 -> BMI = 22.507863455018317
h=1.15, w=38.4 -> BMI = 29.0359168241966
```

### 4.3 Boolean Masks
A boolean mask is a list or array of boolean values where each item represents whether the corresponding element in the original collection meets a condition:
```python
bmis = [22.51, 29.04]
limit = 26
mask = [val > limit for val in bmis]
print(mask)  # [False, True]
```
This is the core concept underlying data filtering in NumPy and Pandas.

### 4.4 Robust Input Validation
In 42 projects, input validation is mandatory. For `give_bmi`:
1. Check that inputs are instances of `list`.
2. Check that both lists are non-empty and have identical length.
3. Check that every element is an `int` or `float` (and NOT a `bool`).
4. Check that all heights and weights are greater than zero.

```python
def validate_lists(height: list, weight: list) -> None:
    if not isinstance(height, list) or not isinstance(weight, list):
        raise TypeError("Arguments must be lists.")
    if len(height) != len(weight):
        raise ValueError("Height and weight lists must have the same length.")
    if len(height) == 0:
        raise ValueError("Lists cannot be empty.")
    for h, w in zip(height, weight):
        if type(h) not in (int, float) or type(w) not in (int, float):
            raise TypeError("List elements must be int or float.")
        if h <= 0 or w <= 0:
            raise ValueError("Height and weight must be positive numbers.")
```

---

## 5. Syntax and Examples

### Using List Comprehension
```python
bmi_list = [w / (h ** 2) for h, w in zip(height, weight)]
```

### Using NumPy (Vectorized)
```python
import numpy as np

h = np.array(height, dtype=float)
w = np.array(weight, dtype=float)
bmi_list = (w / (h ** 2)).tolist()  # Convert back to plain list!
```

### Applying the Limit
```python
mask = [b > limit for b in bmi]
```

---

## 6. How to Think About the Exercise

1. **Step 1: Understand the contract.**
   - Two functions, exact prototypes with type hints.
   - Output types: `list[int | float]` and `list[bool]`.
2. **Step 2: Validate the inputs.**
   - Confirm both arguments are lists.
   - Confirm equal lengths.
   - Confirm element types (`int` or `float`, no `bool`) and valid positive numbers.
3. **Step 3: Implement `give_bmi`.**
   - Pair up the elements using `zip(height, weight)`.
   - Calculate `w / (h ** 2)` for each pair and collect into a list.
4. **Step 4: Implement `apply_limit`.**
   - Validate that `bmi` is a list of numbers and `limit` is an integer or float.
   - Evaluate `b > limit` for each element.
5. **Step 5: Wrap in `main()` with error handling and verify with `flake8`.**

---

## 7. Guided Practice

These five drills go from easiest to hardest, each adding one more requirement from the subject, until Practice 5 reproduces the complete, rule-compliant `give_bmi.py`.

**Practice 1 (Easiest — Single BMI calculation):**
Write a Python expression that computes the BMI for a height of `2.71` and weight of `165.3`.

Expected output:
```python
22.507863455018317
```

<details><summary>Solution</summary>

```python
height = 2.71
weight = 165.3
bmi = weight / (height ** 2)
print(bmi)
```
</details>

**Practice 2 (Elementwise calculation on two lists):**
Write a function `simple_bmi(height, weight)` that takes two equal-length lists of numbers and returns a list of BMI values using `zip()` and list comprehension.

Expected output:
```python
print(simple_bmi([2.71, 1.15], [165.3, 38.4]))
# [22.507863455018317, 29.0359168241966]
```

<details><summary>Solution</summary>

```python
def simple_bmi(height: list, weight: list) -> list:
    """Calculate BMI values from height and weight lists."""
    return [w / (h ** 2) for h, w in zip(height, weight)]
```
</details>

**Practice 3 (Boolean mask thresholding):**
Write `apply_limit(bmi, limit)` that takes a list of BMI numbers and returns a list of booleans indicating whether each value is strictly greater than `limit`.

Expected output:
```python
print(apply_limit([22.5078, 29.0359], 26))
# [False, True]
```

<details><summary>Solution</summary>

```python
def apply_limit(bmi: list[int | float], limit: int) -> list[bool]:
    """Return boolean mask indicating if values exceed limit."""
    return [b > limit for b in bmi]
```
</details>

**Practice 4 (Input validation):**
Add input checks to `give_bmi`: verify that `height` and `weight` are lists, have the same length, contain only numbers (not booleans), and have positive values. Raise `AssertionError` or `TypeError`/`ValueError` on bad inputs.

Expected output:

| Call | Result |
|---|---|
| `give_bmi([1.8], [75])` | `[23.148148148148145]` |
| `give_bmi([1.8], [75, 80])` | Raises `ValueError` |
| `give_bmi([True], [75])` | Raises `TypeError` |

<details><summary>Solution</summary>

```python
def give_bmi(height: list[int | float], weight: list[int | float]) -> list[int | float]:
    """Calculate BMI with strict input validation."""
    if not isinstance(height, list) or not isinstance(weight, list):
        raise TypeError("Inputs must be lists.")
    if len(height) != len(weight):
        raise ValueError("Height and weight lists must have the same length.")
    for h, w in zip(height, weight):
        if type(h) not in (int, float) or type(w) not in (int, float):
            raise TypeError("List elements must be int or float.")
        if h <= 0 or w <= 0:
            raise ValueError("Height and weight must be positive.")
    return [w / (h ** 2) for h, w in zip(height, weight)]
```
</details>

**Practice 5 (Hardest — the full, rule-compliant `give_bmi.py`):**
Write the complete module with prototypes, full type annotations, docstrings, and a `main()` function testing both normal behavior and error handling.

Expected output when running `tester.py`:
```
$> python tester.py
[22.507863455018317, 29.0359168241966] <class 'list'>
[False, True]
```

<details><summary>Solution</summary>

```python
"""Module to calculate Body Mass Index (BMI) and apply thresholds."""


def give_bmi(
    height: list[int | float],
    weight: list[int | float]
) -> list[int | float]:
    """Calculate BMI pairwise from height (meters) and weight (kg).

    Args:
        height: List of heights in meters.
        weight: List of weights in kilograms.

    Returns:
        List of calculated BMI values.

    Raises:
        TypeError: If inputs are not lists or contain non-numeric types.
        ValueError: If list lengths differ or values are non-positive.
    """
    if not isinstance(height, list) or not isinstance(weight, list):
        raise TypeError("Arguments height and weight must be lists.")
    if len(height) != len(weight):
        raise ValueError("Height and weight lists must have the same length.")

    for h, w in zip(height, weight):
        if type(h) not in (int, float) or type(w) not in (int, float):
            raise TypeError("List elements must be int or float.")
        if h <= 0 or w <= 0:
            raise ValueError("Height and weight must be strictly positive.")

    return [w / (h ** 2) for h, w in zip(height, weight)]


def apply_limit(bmi: list[int | float], limit: int) -> list[bool]:
    """Check if BMI values exceed a specified limit threshold.

    Args:
        bmi: List of BMI numbers.
        limit: Threshold limit to compare against.

    Returns:
        List of booleans, True if the BMI exceeds limit, False otherwise.

    Raises:
        TypeError: If bmi is not a list or limit is not an int or float.
    """
    if not isinstance(bmi, list):
        raise TypeError("Argument bmi must be a list.")
    if type(limit) not in (int, float):
        raise TypeError("Limit must be an integer or float.")

    for val in bmi:
        if type(val) not in (int, float):
            raise TypeError("BMI elements must be int or float.")

    return [val > limit for val in bmi]


def main():
    """Execute sample test cases and verify error handling."""
    try:
        height = [2.71, 1.15]
        weight = [165.3, 38.4]
        bmi = give_bmi(height, weight)
        print(bmi, type(bmi))
        print(apply_limit(bmi, 26))
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
```
</details>

If your test output matches the subject exactly and passes `flake8`, you're done!

---

## 8. Exercise-Specific Knowledge

- **Exact Subject Tester (`tester.py`):**
  ```python
  from give_bmi import give_bmi, apply_limit

  height = [2.71, 1.15]
  weight = [165.3, 38.4]
  bmi = give_bmi(height, weight)
  print(bmi, type(bmi))
  print(apply_limit(bmi, 26))
  ```
  Expected output:
  ```
  [22.507863455018317, 29.0359168241966] <class 'list'>
  [False, True]
  ```
- **Strict Inequality:** The subject specifies `True` if *above* the limit: `val > limit` (not `>=`).
- **Allowed Libraries:** You can use NumPy internally if you prefer (`(w / h**2).tolist()`), but pure Python lists are simpler and avoid external dependency overhead.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Returning a `numpy.ndarray` | Using `np.array` without `.tolist()` | Always return a standard Python `list` |
| `zip()` truncating silently | Passing lists of unequal length | Check `len(height) != len(weight)` first |
| `isinstance(True, int) == True` | `bool` is a subclass of `int` in Python | Use `type(x) in (int, float)` |
| Missing `main()` or unhandled exception | 42 Chapter II rules require a caught `main()` | Wrap test calls in `try ... except` |
| `flake8` lines exceeding 79 characters | Long type annotations or docstrings | Split parameters across multiple lines |

---

## 10. Debugging Guide

- **`TypeError: unsupported operand type(s) for **: 'str' and 'int'`**: One of the elements in the height list is a string. Ensure your validation checks every element before computation.
- **`ZeroDivisionError: float division by zero`**: A height is `0`. Add a check for `h <= 0`.
- **Tester prints `<class 'numpy.ndarray'>` instead of `<class 'list'>`**: Call `.tolist()` on the resulting NumPy array before returning.

---

## 11. Cheat Sheet

```python
# Pairwise list comprehension (pure Python):
bmi = [w / (h ** 2) for h, w in zip(height, weight)]

# Threshold mask:
mask = [val > limit for val in bmi]

# Type check avoiding booleans:
if type(x) not in (int, float):
    raise TypeError(...)
```

---

## 12. Knowledge Checklist

- [ ] I can compute elementwise mathematical operations across multiple lists using `zip()`.
- [ ] I know how to construct boolean masks with list comprehensions.
- [ ] I understand why `type(x) in (int, float)` is safer than `isinstance(x, int)` when excluding booleans.
- [ ] I ensured that `give_bmi` returns a `<class 'list'>`.
- [ ] My code conforms to PEP 8 and passes `flake8` without warnings.
