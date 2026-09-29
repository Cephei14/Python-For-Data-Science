# Study Tutorial — Module 1, Exercise 00: give_bmi.py

## 1. Exercise Overview

**What it asks:** Write two functions. `give_bmi(height, weight)` takes two lists (heights in meters, weights in kg) and returns a list of BMI values, computed pairwise. `apply_limit(bmi, limit)` takes a list of BMI values and a threshold, and returns a list of booleans — `True` where the BMI exceeds the limit. Both must handle bad input (mismatched list lengths, wrong types) gracefully.

**Main concepts you'll learn:**
- Elementwise (pairwise) computation across two lists
- The BMI formula as a first taste of vectorized-style thinking
- Input validation across multiple related lists
- Producing a list of booleans as a "mask" — a concept you'll use constantly with NumPy later

**Why this matters:** This exercise is your bridge from Module 0's plain Python into Module 1's array-centric thinking. "Apply the same formula to every row of two aligned columns" is *exactly* what you'll do with real datasets — one column of heights, one of weights, computed together row by row. Even though NumPy is allowed here, doing it once with plain lists first cements why NumPy's vectorization is such a big deal later.

**Skills after completing it:**
- Zip/pair two lists together for elementwise computation
- Apply a mathematical formula across paired data
- Build a boolean mask from a numeric list and a threshold
- Validate multiple input lists against each other (same length, same/compatible types)

---

## 2. Prerequisites

- Module 0 concepts: functions, type checking, `AssertionError`/error handling, list basics
- Basic arithmetic in Python (`**` for power, `/` for division)
- What a "boolean mask" conceptually means: a list of `True`/`False` values, one per original item, marking which items satisfy a condition

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `zip(list1, list2)` | Pairs up items from two lists positionally | `zip([1,2],[3,4])` gives `(1,3), (2,4)` |
| List comprehension | Builds a new list from a loop (see Module 0, ex06) | The natural tool for "apply formula to every pair" |
| `numpy` (optional, allowed) | Provides true vectorized array math (`arr1 / arr2 ** 2`) | Not required — plain Python lists work fine here, but NumPy is worth trying since it's allowed |
| `len(list)` | Number of items | Used to validate two lists are the same length |
| `all(...)` / `isinstance(x, (int, float))` | Checking every item in a list is a number | Used for type validation |

Common pitfalls:
- Forgetting BMI's formula uses height **squared**: `BMI = weight / height ** 2`, not `weight / height`.
- Assuming the lists are always valid — the exercise explicitly asks you to handle mismatched lengths and wrong types.
- If using NumPy, forgetting that dividing mismatched-length arrays doesn't raise a friendly Python-level error the way you might expect — validate *before* handing data to NumPy.

---

## 4. Concepts You Need to Learn

### 4.1 The BMI formula
Body Mass Index is computed as:
```
BMI = weight (kg) / height (m)²
```
So for `height = 1.80`, `weight = 75`: `BMI = 75 / (1.80 ** 2)`.

### 4.2 Pairing two lists with `zip`
```python
heights = [1.80, 1.65]
weights = [75, 60]
for h, w in zip(heights, weights):
    print(h, w)
# 1.8 75
# 1.65 60
```
`zip` walks both lists in lockstep, giving you one `(h, w)` pair per iteration — exactly what you need to compute one BMI per person.

### 4.3 Boolean masks
A "mask" is just a list of `True`/`False` values, the same length as your data, indicating which items meet some condition:
```python
values = [10, 25, 5, 30]
limit = 15
mask = [v > limit for v in values]
print(mask)  # [False, True, False, True]
```
This pattern — "compare every element to a threshold, get back a list of booleans" — is the plain-Python version of what NumPy calls "boolean indexing," which you'll rely on heavily in the pandas module.

---

## 5. Syntax and Examples

### Computing BMI with a list comprehension
```python
def give_bmi(height, weight):
    return [w / (h ** 2) for h, w in zip(height, weight)]

print(give_bmi([1.80, 1.65], [75, 60]))
# [23.148148148148145, 22.03856749311295]
```
Small example first:
```python
h, w = 1.80, 75
print(w / (h ** 2))  # 23.148148148148145
```

### Building a boolean mask
```python
def apply_limit(bmi, limit):
    return [b > limit for b in bmi]

print(apply_limit([23.1, 29.0], 26))  # [False, True]
```

### Validating input length
```python
def give_bmi(height, weight):
    if len(height) != len(weight):
        raise ValueError("height and weight lists must be the same length")
    return [w / (h ** 2) for h, w in zip(height, weight)]
```

### Validating input type
```python
def all_numeric(lst):
    return all(isinstance(x, (int, float)) for x in lst)

print(all_numeric([1, 2.5, 3]))   # True
print(all_numeric([1, "two", 3]))  # False
```
Note: this deliberately checks `(int, float)` together, since `isinstance(x, (int, float))` accepts either type in one call — useful because the exercise says lists can contain "integers or floats" interchangeably.

---

## 6. How to Think About the Exercise

1. Start from the formula. Write a version of `give_bmi` that works correctly on well-formed input first — don't tackle error handling before the happy path works.
2. Add validation: same length for both lists, and every element in both lists is numeric (`int` or `float`, explicitly *not* `bool`, `str`, etc. — recall from Module 0 ex03 that `bool` is sneaky since `True`/`False` behave like `1`/`0`).
3. Decide *how* to signal an error — the subject doesn't show an exact error message format here (unlike Module 0's `AssertionError` exercises), so a sensible choice is to `raise` a `ValueError` (or similar) with a clear message, matching the general rule "handle any error with a clear message" seen in later exercises of this module.
4. For `apply_limit`, the logic is much simpler: one condition applied to every item.
5. Try the NumPy approach too, since it's explicitly allowed: `np.array(weight) / np.array(height) ** 2` computes the whole thing in one vectorized expression, no loop needed. Compare this to your list-comprehension version — this contrast is exactly why the array module exists.

---

## 7. Guided Practice

**Practice 1 (Easy):** Compute BMI for a single person with height `1.75` and weight `70`.
<details><summary>Solution</summary>

```python
print(70 / (1.75 ** 2))  # 22.857142857142858
```
</details>

**Practice 2 (Easy):** Pair up `["a", "b", "c"]` and `[1, 2, 3]` using `zip` and print each pair.
<details><summary>Solution</summary>

```python
for letter, number in zip(["a", "b", "c"], [1, 2, 3]):
    print(letter, number)
```
</details>

**Practice 3 (Medium):** Write a function `over_threshold(values, limit)` returning a boolean mask of which values exceed `limit`.
<details><summary>Solution</summary>

```python
def over_threshold(values, limit):
    return [v > limit for v in values]
```
</details>

**Practice 4 (Close to the real exercise):** Write `give_bmi` with validation: raise a `ValueError` if the two lists aren't the same length.
<details><summary>Solution</summary>

```python
def give_bmi(height, weight):
    if len(height) != len(weight):
        raise ValueError("lists must be the same length")
    return [w / (h ** 2) for h, w in zip(height, weight)]
```
</details>

**Practice 5 (Bonus, NumPy version):** Rewrite `give_bmi` using NumPy's vectorized operations instead of a list comprehension.
<details><summary>Solution</summary>

```python
import numpy as np

def give_bmi(height, weight):
    h = np.array(height)
    w = np.array(weight)
    return list(w / (h ** 2))
```
Note the `list(...)` at the end — the tester's expected output shows `<class 'list'>`, so if you compute with NumPy internally, convert back to a plain list before returning.
</details>

---

## 8. Exercise-Specific Knowledge

- `give_bmi` return type must specifically be a plain `list` (the tester checks `type(bmi)` and expects `<class 'list'>`), even if you use NumPy internally to compute it.
- `apply_limit` returns a list of `bool`, `True` where BMI is *above* the limit (strictly greater than, based on the example: BMI `26` limit with `29.03...` → `True`, and `22.5...` → `False`).
- You must handle error cases: mismatched list lengths, non-numeric entries.
- Allowed tools: NumPy or "any lib of table manipulation" — but plain Python lists are perfectly valid too.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `weight / height ** 2` without parentheses around `height` when height itself is a fraction of an expression | Usually fine due to operator precedence (`**` binds tighter than `/`), but double-check for compound expressions | `w / (h ** 2)` is safest and most readable |
| Not checking list lengths before zipping | `zip` silently truncates to the shorter list instead of erroring | Explicitly compare `len(height) != len(weight)` first |
| Returning a NumPy array instead of a `list` | Forgetting the required return type | Wrap the final result in `list(...)` |
| Treating `bool` values as valid numeric input | Forgetting `isinstance(True, int)` is `True` | If strict validation matters, explicitly exclude `bool`: `isinstance(x, (int, float)) and not isinstance(x, bool)` |

---

## 10. Debugging Guide

- **`ZeroDivisionError`** → a height of `0` was passed; decide whether to validate against this explicitly (heights should logically never be zero).
- **Wrong-length result list** → check whether `zip` silently truncated because your two input lists weren't actually the same length; validate lengths *before* zipping.
- **`TypeError: unsupported operand type(s)`** → one of your list's entries isn't numeric (e.g., a string snuck in); validate types before computing.
- Useful inspection: `print([type(x) for x in height])` to quickly see the types of every element if something isn't behaving as expected.

---

## 11. Cheat Sheet

```python
def give_bmi(height, weight):
    if len(height) != len(weight):
        raise ValueError("height and weight must be the same length")
    return [w / (h ** 2) for h, w in zip(height, weight)]

def apply_limit(bmi, limit):
    return [b > limit for b in bmi]
```

`zip(a, b)` → pairs elements positionally.
List comprehension with a comparison → boolean mask.

---

## 12. Knowledge Checklist

- [ ] I know the BMI formula and can implement it correctly.
- [ ] I can pair two lists together with `zip` for elementwise computation.
- [ ] I can build a boolean mask from a list and a threshold.
- [ ] I can validate that two lists have matching lengths before processing them together.
- [ ] I understand why this "same operation, applied per-pair or per-element" pattern is the conceptual seed of NumPy vectorization.
