# Study Tutorial — Exercise 01: array2D.py

## 1. Exercise Overview

**What it asks:**
Create a module named `array2D.py` in directory `ex01/` containing a function:
```python
def slice_me(family: list, start: int, end: int) -> list:
```
- Accepts a 2D array `family` (a nested list representing rows and columns), an integer `start`, and an integer `end`.
- Calculates and prints the shape of the original 2D array:
  `My shape is : (<rows>, <columns>)`
- Truncates the array using Python's **slicing method** from index `start` up to index `end`.
- Calculates and prints the shape of the truncated array:
  `My new shape is : (<new_rows>, <columns>)`
- Returns the truncated 2D array as a standard Python `list`.

**Rules and Constraints:**
- Must handle error cases gracefully (e.g. if the input is not a list, not a 2D array, if inner lists have inconsistent row lengths, or if `start`/`end` are invalid types).
- Must use the slicing method (`family[start:end]`).
- Follow all 42 Python Norm rules: PEP 8 / `flake8` clean, docstrings on every function and module, no global code, and a `main()` function with caught exceptions.

**Main concepts you'll learn:**
- Representing 2D matrices as nested lists in Python.
- Determining and understanding array dimensions: `(rows, columns)`.
- Python slicing mechanics with positive and negative indices.
- Validating the structural integrity (rectangularity) of multi-dimensional data.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **Lists & Indexing (Module 0 ex00, ex02):** Accessing list items by index.
- **Slicing Basics (Module 0 ex06):** Using `seq[start:end]` to extract subsets.
- **Negative Indexing (Module 0 ex07):** Accessing elements counting from the end (`-1` is the last item, `-2` is second to last).
- **Error Handling (Module 1 ex00):** Raising and catching `TypeError` and `ValueError`.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `family[start:end]` | Python slice syntax | Extracts rows from index `start` up to (exclusive) `end` |
| `len(family)` | Returns the number of rows | First dimension of the 2D array |
| `len(family[0])` | Returns the number of columns | Second dimension (assuming rectangularity) |
| `all(len(row) == len(family[0]) for row in family)` | Validates rectangularity | Ensures every row has the same column count |
| `numpy` (allowed) | High-performance array library | `np.array(family).shape` gets shape; `.tolist()` converts back |

**Common pitfalls:**
- **Exclusive End Index:** Slicing is *half-open* `[start, end)`. The element at `end` is **not** included. For instance, `family[0:2]` extracts indices `0` and `1` (total of 2 rows).
- **Negative Indices in Slices:** `family[1:-2]` means start at index 1 and stop before the 2nd element from the end. In a 4-row list (`indices 0, 1, 2, 3`), `-2` corresponds to index 2, so it takes only index 1!
- **Ragged / Jagged Lists:** If one row has 2 columns and another has 3 columns, it is **not** a valid 2D array. You must validate that every row has the exact same length.
- **Empty Slices:** Slicing with indices like `[3:1]` results in an empty list `[]`. The column count should be preserved or handled cleanly without crashing.

---

## 4. Concepts You Need to Learn

### 4.1 What is a 2D Array in Python?
A 2D array is represented in Python as a list of lists, where the outer list represents rows and each inner list represents the columns in that row:
```python
family = [
    [1.80, 78.4],  # Row 0: height, weight
    [2.15, 102.7], # Row 1: height, weight
    [2.10, 98.5],  # Row 2: height, weight
    [1.88, 75.2]   # Row 3: height, weight
]
```
The shape is:
$$\text{shape} = (\text{rows}, \text{columns}) = (4, 2)$$

### 4.2 Slicing Mechanics (Positive & Negative)
Python slices follow the pattern `sequence[start:end]`:
- `start`: index to begin (inclusive).
- `end`: index to stop (exclusive).

Examples on a list with 4 elements `[R0, R1, R2, R3]`:
- `family[0:2]` $\rightarrow$ `[R0, R1]` (2 rows, rows 0 and 1).
- `family[1:-2]` $\rightarrow$ index `-2` points to `R2`, so `[1:-2]` gives `[R1]` (1 row, row 1).
- `family[:]` $\rightarrow$ copies all rows.

### 4.3 Validating a 2D Array
Before slicing, we must check:
1. Is `family` a `list`?
2. Are all elements inside `family` also `list` instances?
3. Do all inner lists have the same length?
4. Are `start` and `end` integers?

```python
def validate_2d_array(family: list, start: int, end: int) -> tuple[int, int]:
    if not isinstance(family, list):
        raise TypeError("Input 'family' must be a list.")
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("Arguments 'start' and 'end' must be integers.")
    if len(family) == 0:
        return (0, 0)
    if not all(isinstance(row, list) for row in family):
        raise TypeError("All elements of family must be lists.")
    row_len = len(family[0])
    if not all(len(row) == row_len for row in family):
        raise ValueError("All rows in the 2D array must have the same length.")
    return (len(family), row_len)
```

---

## 5. Syntax and Examples

### Pure Python Implementation
```python
family = [[1.80, 78.4], [2.15, 102.7], [2.10, 98.5], [1.88, 75.2]]

rows = len(family)
cols = len(family[0])
print(f"My shape is : ({rows}, {cols})")

sliced = family[0:2]
new_rows = len(sliced)
print(f"My new shape is : ({new_rows}, {cols})")
print(sliced)
```

### NumPy Implementation (Alternative)
```python
import numpy as np

arr = np.array(family)
print(f"My shape is : {arr.shape}")
sliced_arr = arr[0:2]
print(f"My new shape is : {sliced_arr.shape}")
return sliced_arr.tolist()  # Must return a list!
```

---

## 6. How to Think About the Exercise

1. **Step 1: Check arguments.** Validate that `family` is a list and `start`/`end` are integers.
2. **Step 2: Inspect matrix dimensions.** If non-empty, check that every item in `family` is a list of equal length. Determine initial shape `(len(family), len(family[0]))`.
3. **Step 3: Print original shape.** Print `My shape is : (rows, cols)`.
4. **Step 4: Slice the array.** Use standard Python slice syntax: `sliced = family[start:end]`.
5. **Step 5: Determine and print new shape.** If `sliced` is not empty, its shape is `(len(sliced), len(sliced[0]))`. Otherwise `(0, cols)` or `(0, 0)`. Print `My new shape is : (new_rows, cols)`.
6. **Step 6: Return the sliced list.**

---

## 7. Guided Practice

**Practice 1 (Easiest — Compute shape of a 2D list):**
Given a list of lists `matrix = [[1, 2, 3], [4, 5, 6]]`, print its shape in the format `(rows, columns)`.

Expected output:
```python
(2, 3)
```

<details><summary>Solution</summary>

```python
matrix = [[1, 2, 3], [4, 5, 6]]
rows = len(matrix)
cols = len(matrix[0]) if rows > 0 else 0
print((rows, cols))
```
</details>

**Practice 2 (Slice rows with positive indices):**
Write a function `slice_rows(lst, start, end)` that slices a 2D list and returns the subset. Test with `start=0, end=2`.

Expected output:
```python
family = [[1.80, 78.4], [2.15, 102.7], [2.10, 98.5], [1.88, 75.2]]
print(slice_rows(family, 0, 2))
# [[1.8, 78.4], [2.15, 102.7]]
```

<details><summary>Solution</summary>

```python
def slice_rows(lst: list, start: int, end: int) -> list:
    """Slice rows from start to end."""
    return lst[start:end]
```
</details>

**Practice 3 (Negative index slicing and shape reporting):**
Extend Practice 2 to print both the original and new shape before returning the sliced result. Test with `start=1, end=-2`.

Expected output:
```
My shape is : (4, 2)
My new shape is : (1, 2)
[[2.15, 102.7]]
```

<details><summary>Solution</summary>

```python
def slice_and_report(family: list, start: int, end: int) -> list:
    """Report shapes and return sliced array."""
    orig_shape = (len(family), len(family[0]))
    sliced = family[start:end]
    new_shape = (len(sliced), len(family[0])) if sliced else (0, len(family[0]))
    print(f"My shape is : {orig_shape}")
    print(f"My new shape is : {new_shape}")
    return sliced
```
</details>

**Practice 4 (Rectangularity and type validation):**
Add validation to reject non-list inputs or jagged lists where rows have different lengths.

Expected output:

| Call | Result |
|---|---|
| `slice_me([[1, 2], [3, 4]], 0, 1)` | Prints shapes and returns `[[1, 2]]` |
| `slice_me([[1, 2], [3]], 0, 1)` | Raises `ValueError` |
| `slice_me("not a list", 0, 1)` | Raises `TypeError` |

<details><summary>Solution</summary>

```python
def slice_me(family: list, start: int, end: int) -> list:
    """Validate 2D rectangularity and slice."""
    if not isinstance(family, list):
        raise TypeError("family must be a list")
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("start and end must be integers")
    if len(family) > 0:
        if not all(isinstance(r, list) for r in family):
            raise TypeError("all rows must be lists")
        cols = len(family[0])
        if not all(len(r) == cols for r in family):
            raise ValueError("all rows must have the same length")
    return family[start:end]
```
</details>

**Practice 5 (Hardest — the full, rule-compliant `array2D.py`):**
Write the complete module with documentation, PEP 8 compliance, and a `main()` function testing the tester commands.

Expected output:
```
$> python tester.py
My shape is : (4, 2)
My new shape is : (2, 2)
[[1.8, 78.4], [2.15, 102.7]]
My shape is : (4, 2)
My new shape is : (1, 2)
[[2.15, 102.7]]
```

<details><summary>Solution</summary>

```python
"""Module for 2D array manipulation and slicing."""


def slice_me(family: list, start: int, end: int) -> list:
    """Slice a 2D array along rows and print its original and new shapes.

    Args:
        family: A 2D list representing a rectangular matrix.
        start: Starting row index for the slice.
        end: Ending row index (exclusive) for the slice.

    Returns:
        The sliced 2D list.

    Raises:
        TypeError: If inputs are invalid types or non-list rows exist.
        ValueError: If rows have inconsistent lengths.
    """
    if not isinstance(family, list):
        raise TypeError("Input 'family' must be a list.")
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("Indices 'start' and 'end' must be integers.")

    if len(family) == 0:
        print("My shape is : (0, 0)")
        print("My new shape is : (0, 0)")
        return []

    if not all(isinstance(row, list) for row in family):
        raise TypeError("All elements in 'family' must be lists.")

    cols = len(family[0])
    if not all(len(row) == cols for row in family):
        raise ValueError("All rows in the 2D array must have the same length.")

    print(f"My shape is : ({len(family)}, {cols})")

    sliced = family[start:end]
    new_rows = len(sliced)
    print(f"My new shape is : ({new_rows}, {cols})")

    return sliced


def main():
    """Execute sample slicing tests."""
    try:
        family = [
            [1.80, 78.4],
            [2.15, 102.7],
            [2.10, 98.5],
            [1.88, 75.2]
        ]
        print(slice_me(family, 0, 2))
        print(slice_me(family, 1, -2))
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
  from array2D import slice_me

  family = [[1.80, 78.4],
            [2.15, 102.7],
            [2.10, 98.5],
            [1.88, 75.2]]

  print(slice_me(family, 0, 2))
  print(slice_me(family, 1, -2))
  ```
  Expected output:
  ```
  My shape is : (4, 2)
  My new shape is : (2, 2)
  [[1.8, 78.4], [2.15, 102.7]]
  My shape is : (4, 2)
  My new shape is : (1, 2)
  [[2.15, 102.7]]
  ```
- **Printing Format:** Note the single space before the colon in the subject's expected output: `My shape is : (4, 2)`. Follow this exact spacing!
- **Preserving Column Dimension:** Even if `sliced` has `1` row, the column dimension remains `2`: `(1, 2)`.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Missing space before colon | Printing `My shape is: (4, 2)` | Subject specifies `My shape is : (4, 2)` |
| Confusing `(rows, cols)` order | Printing `(cols, rows)` | Outer list length is rows, inner list length is columns |
| Returning a NumPy array | Forgetting subject requires Python `list` | Slice pure lists or call `.tolist()` |
| Allowing jagged rows | Not checking `len(row) == len(family[0])` | Validate with `all(len(row) == cols ...)` |

---

## 10. Debugging Guide

- **`IndexError: list index out of range`**: Raised if you check `len(family[0])` without first checking if `family` is empty (`len(family) == 0`).
- **Wrong new shape with negative slicing**: Remember `family[1:-2]` on a 4-row list takes only index 1 (1 row total).

---

## 11. Cheat Sheet

```python
# Slicing:
sliced = family[start:end]

# Shape tuple:
shape = (len(family), len(family[0]))

# Exact subject print string:
print(f"My shape is : ({rows}, {cols})")
print(f"My new shape is : ({new_rows}, {cols})")
```

---

## 12. Knowledge Checklist

- [ ] I understand how 2D rectangular structures map to rows and columns.
- [ ] I can slice lists using both positive and negative indices.
- [ ] I verified that the output matches the required spacing `My shape is : ...`.
- [ ] I validated that jagged/ragged inputs raise an appropriate exception.
- [ ] My code conforms to PEP 8 and passes `flake8` without warnings.
