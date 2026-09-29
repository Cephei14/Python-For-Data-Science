# Study Tutorial — Module 1, Exercise 01: array2D.py

## 1. Exercise Overview

**What it asks:** Write a function `slice_me(family, start, end)` that takes a 2D array (a list of lists), prints its "shape" (rows, columns), and returns a truncated version — keeping only rows from index `start` up to (but not including) `end` — using Python's slicing syntax. It must handle bad input (inconsistent row lengths, non-list input, etc).

**Main concepts you'll learn:**
- What "shape" means for 2D data (rows × columns)
- Python's slicing syntax, including negative indices
- Validating that a "2D array" is actually rectangular (every row the same length)

**Why this matters:** Slicing is one of the single most-used operations in all of data science — selecting a range of rows from a table, a window of time from a series, a subset of columns. Learning to reason about "shape" and slice ranges correctly here, with plain lists, sets you up perfectly for identical (but faster) operations in NumPy arrays and pandas DataFrames later.

**Skills after completing it:**
- Compute and report the shape of a 2D list structure
- Slice a list using `start:end` syntax, including negative indices
- Validate that a nested list is "rectangular" (a true 2D array, not a ragged list of lists)

---

## 2. Prerequisites

- Module 0's list basics
- Nested lists: a list where each item is itself a list (`[[1, 2], [3, 4]]`)
- Basic indexing: `my_list[0]` gets the first item

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `list[start:end]` | Slicing — returns a new list containing items from index `start` up to (not including) `end` | Negative indices count from the end |
| `len(list)` | Number of top-level items (rows, for a 2D list) | Used for both shape reporting and validation |
| `len(list[0])` | Number of items in the first row (columns) | Combined with `len(list)`, gives the shape |
| `all(len(row) == n for row in family)` | Checks every row has the same length | Used to validate the array is truly rectangular |

Common pitfalls:
- Forgetting that slicing is **exclusive** of the end index: `[0:2]` gives items at index 0 and 1, *not* index 2.
- Forgetting negative indices count backward from the end: `-1` is the last item, `-2` is second-to-last, so `family[1:-2]` means "from index 1 up to (but not including) two before the end."
- Confusing "shape" `(rows, columns)` order — rows come first, matching how you'd naturally read a nested list (outer list = rows).

---

## 4. Concepts You Need to Learn

### 4.1 "Shape" of a 2D list
For a nested list like:
```python
family = [[1.80, 78.4],
          [2.15, 102.7],
          [2.10, 98.5],
          [1.88, 75.2]]
```
The **shape** is `(4, 2)`: 4 rows (outer list length), 2 columns (each inner list's length). You compute it as:
```python
rows = len(family)
cols = len(family[0])
```

### 4.2 Slicing syntax
```python
my_list = [10, 20, 30, 40, 50]
print(my_list[1:3])    # [20, 30]      -- indices 1 and 2
print(my_list[0:2])    # [10, 20]      -- indices 0 and 1
print(my_list[1:-2])   # [20, 30]      -- from index 1, up to 2 before the end
print(my_list[:2])     # [10, 20]      -- omitting start defaults to 0
print(my_list[2:])     # [30, 40, 50]  -- omitting end defaults to "to the end"
```
The general form is `list[start:end]`, where `end` is exclusive.

### 4.3 Negative indices
Negative indices count from the end of the list: `-1` is the last element, `-2` is second-to-last. This is especially useful for slices like "everything except the last two rows," which is exactly what `family[1:-2]` expresses in the exercise's example.

### 4.4 Validating rectangularity
A true 2D array must have every row the same length. If one row has 2 items and another has 3, it's not a valid rectangular 2D structure:
```python
def is_rectangular(family):
    if len(family) == 0:
        return True
    first_len = len(family[0])
    return all(len(row) == first_len for row in family)
```

---

## 5. Syntax and Examples

### Reporting shape
```python
family = [[1.80, 78.4], [2.15, 102.7], [2.10, 98.5], [1.88, 75.2]]
print(f"My shape is : ({len(family)}, {len(family[0])})")
# My shape is : (4, 2)
```

### Slicing rows
```python
def slice_me(family, start, end):
    sliced = family[start:end]
    return sliced

print(slice_me(family, 0, 2))
# [[1.8, 78.4], [2.15, 102.7]]
print(slice_me(family, 1, -2))
# [[2.15, 102.7]]
```
Walking through `slice_me(family, 1, -2)`: `family` has 4 rows (indices 0, 1, 2, 3). `-2` refers to index `4 - 2 = 2`. So the slice `[1:-2]` = `[1:2]`, which gives just the row at index 1: `[2.15, 102.7]`.

### Putting it together with shape reporting
```python
def slice_me(family, start, end):
    print(f"My shape is : ({len(family)}, {len(family[0])})")
    sliced = family[start:end]
    print(f"My new shape is : ({len(sliced)}, {len(sliced[0])})")
    return sliced
```

---

## 6. How to Think About the Exercise

1. First print the *original* shape, before slicing anything — this needs `len(family)` for rows and `len(family[0])` for columns (assuming a valid rectangular input).
2. Perform the slice using plain Python list slicing: `family[start:end]` — no manual loop needed.
3. Print the *new* shape of the sliced result the same way.
4. Return the sliced result.
5. For error handling: think about what could go wrong — `family` isn't a list, `family` is empty, rows have inconsistent lengths, `start`/`end` aren't integers. Decide how to signal each (the subject doesn't show an example, so a `ValueError`/`TypeError` with a clear message, consistent with this module's general "handle errors with a clear message" instruction, is reasonable).
6. Watch the exact wording in the expected output: `"My shape is : (4, 2)"` and `"My new shape is : (2, 2)"` — note the spacing around the colon.

---

## 7. Guided Practice

**Practice 1 (Easy):** Given `nums = [10, 20, 30, 40, 50]`, get items at indices 1 through 3 (inclusive of 1, exclusive of 4... i.e., `[20, 30, 40]`).
<details><summary>Solution</summary>

```python
nums = [10, 20, 30, 40, 50]
print(nums[1:4])  # [20, 30, 40]
```
</details>

**Practice 2 (Easy):** Given the same list, get everything except the last two items, using a negative index.
<details><summary>Solution</summary>

```python
print(nums[:-2])  # [10, 20, 30]
```
</details>

**Practice 3 (Medium):** Write a function `shape_of(table)` that returns a tuple `(rows, cols)` for a 2D list.
<details><summary>Solution</summary>

```python
def shape_of(table):
    return (len(table), len(table[0]) if table else 0)

print(shape_of([[1, 2, 3], [4, 5, 6]]))  # (2, 3)
```
</details>

**Practice 4 (Medium):** Write a function `is_rectangular(table)` that checks whether every row has the same length.
<details><summary>Solution</summary>

```python
def is_rectangular(table):
    if not table:
        return True
    n = len(table[0])
    return all(len(row) == n for row in table)

print(is_rectangular([[1, 2], [3, 4]]))     # True
print(is_rectangular([[1, 2], [3, 4, 5]]))   # False
```
</details>

**Practice 5 (Close to the real exercise):** Combine shape-printing and slicing into one function, similar to `slice_me`.
<details><summary>Solution</summary>

```python
def slice_me(family, start, end):
    if not is_rectangular(family):
        raise ValueError("rows must all be the same length")
    print(f"My shape is : ({len(family)}, {len(family[0])})")
    sliced = family[start:end]
    print(f"My new shape is : ({len(sliced)}, {len(sliced[0])})")
    return sliced
```
</details>

---

## 8. Exercise-Specific Knowledge

- Prototype: `def slice_me(family: list, start: int, end: int) -> list:`
- Must print `"My shape is : (rows, cols)"` before slicing, then `"My new shape is : (rows, cols)"` after slicing, matching the exact wording and spacing shown in the subject.
- `slice_me(family, 0, 2)` on a 4-row family → 2-row result.
- `slice_me(family, 1, -2)` on a 4-row family → 1-row result (row index 1 only), demonstrating negative-index slicing specifically.
- You must use the slicing method (`family[start:end]`) — not a manual loop-and-append reimplementation.
- Handle error cases: rows not the same size, input not a list, etc.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Off-by-one on the end index | Forgetting slicing's end is exclusive | `[start:end]` never includes index `end` itself — double check against the expected output examples |
| Miscalculating negative slice results by hand | Negative indices are easy to get wrong mentally | Convert to a positive equivalent first: `-2` on a length-4 list = index `4 - 2 = 2` |
| Computing shape on an empty result | `len(sliced[0])` crashes with `IndexError` if `sliced` is empty | Guard against empty results before indexing into row 0 |
| Manually reimplementing slicing with a loop | Not realizing built-in slicing already does this | Just use `family[start:end]` — the subject explicitly wants you to use slicing |

---

## 10. Debugging Guide

- **`IndexError: list index out of range`** → likely from `len(sliced[0])` when `sliced` is an empty list; check the slice actually produced results before reporting its shape.
- **Wrong number of rows in the output** → recompute the slice indices by hand against the actual list length to confirm what `[start:end]` should produce.
- **`TypeError: 'list' object is not callable`** → check you haven't accidentally shadowed a built-in name like `list` as a variable.
- Useful inspection: `print(family[start:end])` on its own, before wrapping it in shape-printing logic, to isolate whether the bug is in the slicing or the shape-reporting.

---

## 11. Cheat Sheet

```python
list[start:end]      # slice, end exclusive
list[:end]            # from the beginning
list[start:]          # to the end
list[-n:]             # last n items
list[:-n]             # everything except the last n items

len(table)             # number of rows
len(table[0])          # number of columns (assuming rectangular)
```

---

## 12. Knowledge Checklist

- [ ] I can compute the shape `(rows, cols)` of a 2D list.
- [ ] I can slice a list using `start:end` syntax, including negative indices.
- [ ] I understand that the end index in a slice is exclusive.
- [ ] I can validate that a nested list is rectangular before treating it as a 2D array.
- [ ] I understand how this slicing pattern maps directly onto NumPy array slicing and pandas `.iloc[]` later.
