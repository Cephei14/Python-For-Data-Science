# Study Tutorial — Exercise 03: NULL_not_found.py

## 1. Exercise Overview

**What it asks:** Write a function `NULL_not_found(object)` that identifies which flavor of "nothing/empty/null" a value represents — `None`, `NaN` (not-a-number), `0`, an empty string, or `False` — prints a description, and returns `0` on success or `1` if the value doesn't match any known "null-like" case.

**Main concepts you'll learn:**
- That Python (and data science generally) has *multiple different representations* of "nothing," and they are **not interchangeable**
- `math.isnan()` for detecting `NaN`
- Careful type-based branching (this time, order and exactness really matter, because `False == 0` and `0 == 0.0` in Python's eyes)
- Using a function's return value as a status/error code, separate from what it prints

**Why this matters:** This is *the* most important habit for real data work. Missing data in pandas can show up as `None`, `NaN`, an empty string, or a literal `0` depending on the source — and treating them all the same can silently corrupt your analysis. Distinguishing them cleanly, as this exercise forces you to do, is foundational for the pandas module later.

**Skills after completing it:**
- Recognize and correctly detect all common "null-like" Python values
- Use `math.isnan()` correctly (and know why `value == float('nan')` never works)
- Return a status code from a function independent of its printed output

---

## 2. Prerequisites

- Exercise 02's concepts: `type()`, functions, `if/elif/else`
- Basic familiarity with `True`/`False` as values

---

## 3. Tools and Libraries

The subject specifies **`Allowed functions : None`**, meaning you should avoid importing standard libraries like `math`. You can solve this entirely using Python's built-in syntax:

| Tool | What it does | Notes |
|---|---|---|
| `None` | Python's built-in "no value" object, type `NoneType` | Check with `object is None` |
| `float("nan")` | Creates a "Not a Number" float | Represents an undefined/missing numeric result |
| `object != object` | Detects `NaN` using pure Python (**No imports needed!**) | By IEEE 754 standard, NaN is the *only* value that does not equal itself |
| `math.isnan(x)` | Standard library NaN check | Good to know for real projects, but requires `import math` (which conflicts with `Allowed functions : None`) |
| `type(x) is bool` | Checks if something is specifically a boolean | Needed because `False == 0` evaluates to `True` in Python |

Common pitfalls:
- `NaN != NaN` is `True` in Python (and all IEEE 754 conforming systems). This means `x == float('nan')` is *always* `False`! Instead, `x != x` is the purest and simplest way to detect NaN in Python without importing any modules.
- `False == 0` evaluates to `True` in Python because `bool` is a subclass of `int`. Checking `x == 0` before checking `type(x) is bool` will misidentify `False` as `0`.
- Using tabs instead of 4 spaces: In Python, `flake8` forbids tabs (`W191`). Always use 4 spaces.

---

## 4. Concepts You Need to Learn

### 4.1 The many faces of "nothing"

| Value | Type | Subject Output Label | Meaning |
|---|---|---|---|
| `None` | `NoneType` | `Nothing:` | Explicit absence of a value |
| `float("nan")` | `float` | `Cheese:` | Undefined numeric result (NaN) |
| `0` | `int` | `Zero:` | The number zero |
| `""` | `str` | `Empty:` | An empty string |
| `False` | `bool` | `Fake:` | The boolean false |

They are all "falsy" in Python (i.e. `bool(x)` is `False` for each), but each represents a distinct type of "null".

> [!NOTE]
> **Why is the label "Cheese" when the tester variable was `Garlic`?**
> A common beginner question is: *"Can my function see the variable name from the caller?"* No. In Python, arguments are passed as object references — the function receives the float value `nan`, not the name `Garlic`. The subject simply assigned fixed labels (`Nothing:`, `Cheese:`, `Zero:`, `Empty:`, `Fake:`) to each null type.

### 4.2 Detecting NaN without importing `math` (`x != x`)

In the IEEE 754 floating-point specification, `NaN` is specifically designed so that **any comparison with NaN returns False**, including `NaN == NaN`.
Therefore:
```python
x = float("nan")
print(x == x)  # False!
print(x != x)  # True!
```
Because `x != x` is only True for NaN, you can detect NaN with zero imports:
```python
if type(object) is float and object != object:
    # object is guaranteed to be float NaN!
```

### 4.3 Type-first, value-second branching

Since `False == 0` is `True` in Python, checking `object == 0` or using `isinstance(object, int)` would accidentally match `False`. The safe pattern is to check exact types using `type(object) is bool` or check the boolean condition before checking the integer condition.

---

## 5. Syntax and Examples

### Checking for None
```python
x = None
print(x is None)  # True
```
Use `is None`, not `== None` — this is a Python style convention (`is` checks identity, which is the semantically correct check for the unique `None` singleton).

### Checking for NaN
```python
import math
x = float("nan")
print(math.isnan(x))  # True
print(x == x)          # False  (!)
```
Small example, larger one:
```python
values = [1.0, float("nan"), 3.0]
for v in values:
    if math.isnan(v):
        print(f"{v} is NaN")
    else:
        print(f"{v} is a normal number")
```

### Checking for bool vs. int zero
```python
def describe(x):
    if type(x) == bool:
        print("boolean")
    elif type(x) == int:
        print("integer")

describe(False)  # boolean
describe(0)       # integer
```
Order matters here only in the sense that you must check `bool` *specifically* — using `isinstance(x, int)` would incorrectly also match `False` (since `bool` subclasses `int`), so `type(x) == bool` / `type(x) == int` with `==` is the safer pattern for this exercise.

---

## 6. How to Think About the Exercise

1. List the five null-like cases the subject shows in its tester: `None`, `float("nan")`, `0`, `""`, `False`.
2. For each, decide the *check* that uniquely identifies it:
   - `None` → `x is None`
   - NaN → needs `type(x) == float` first (so you don't call `math.isnan()` on a non-float and crash), *then* `math.isnan(x)`
   - `0` → `type(x) == int and x == 0`
   - `""` → `type(x) == str and x == ""`
   - `False` → `type(x) == bool and x == False` (or just `type(x) == bool`, since the exercise only tests `False`)
3. Anything that doesn't match any case (like the string `"Brian"`) falls into an `else` that prints `"Type not Found"` and returns `1`.
4. Every matched case returns `0`; the unmatched case returns `1`. This separates *what gets printed* from *the function's status code* — a pattern you'll see constantly in real code (e.g. functions returning `0`/non-zero like shell exit codes).

---

## 7. Guided Practice

**Practice 1 (Easy):** Write a function that returns `True` if a value is exactly `None`, `False` otherwise.
<details><summary>Solution</summary>

```python
def is_none(x):
    return x is None
```
</details>

**Practice 2 (Medium):** Write a function that safely reports whether a value is NaN, without crashing on non-float inputs (e.g. a string).
<details><summary>Hint</summary>`math.isnan()` raises `TypeError` if given a non-numeric type — guard with a type check first.</details>
<details><summary>Solution</summary>

```python
import math

def safe_is_nan(x):
    if type(x) == float:
        return math.isnan(x)
    return False
```
</details>

**Practice 3 (Medium):** Write a function that distinguishes `0` (int) from `False` (bool), printing which one it received.
<details><summary>Solution</summary>

```python
def zero_or_false(x):
    if type(x) == bool:
        print("This is False")
    elif type(x) == int and x == 0:
        print("This is zero")
    else:
        print("Neither")
```
</details>

**Practice 4 (Close to the real exercise):** Combine the above into one function covering `None`, NaN, `0`, `""`, and `False`, returning `0` for a match and `1` otherwise (without importing any libraries).
<details><summary>Solution</summary>

```python
def null_check(x):
    t = type(x)
    if x is None:
        print(f"Nothing: {x} {t}")
        return 0
    if t is float and x != x:
        print(f"Cheese: {x} {t}")
        return 0
    if t is bool and x is False:
        print(f"Fake: {x} {t}")
        return 0
    if t is int and x == 0:
        print(f"Zero: {x} {t}")
        return 0
    if t is str and x == "":
        print(f"Empty: {t}")
        return 0
    print("Type not Found")
    return 1
```
</details>

---

## 8. Exercise-Specific Knowledge

- Exact expected output lines (from the subject's tester):
  - `Nothing: None <class 'NoneType'>`
  - `Cheese: nan <class 'float'>`
  - `Zero: 0 <class 'int'>`
  - `Empty: <class 'str'>` (single space between colon and type!)
  - `Fake: False <class 'bool'>`
  - `Type not Found` (for the unmatched `"Brian"` case)
  - Final printed return value: `1`
- **The Empty String Spacing Trap:**
  For the other cases, the output format is `{Label}: {value} {type}`.
  However, for `Empty`, the value is `""` (empty string). If you use `f"Empty: {object} {type(object)}"`, Python puts a space before and after the empty string, resulting in **two spaces** (`Empty:  <class 'str'>`), failing the tester! Use `f"Empty: {type(object)}"` or `f"Empty:{object} {type(object)}"` so exactly one space appears before `<class 'str'>`.
- **Zero Libraries Allowed:**
  The subject states `Allowed functions : None`. Do not `import math` — detect NaN with `type(x) is float and x != x`.
- Return `0` for every recognized null-like value, `1` only for the fallback case.
- Check `type(x) is bool` (or check bool before int) because in Python `False == 0` is `True`.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `import math` and `math.isnan(x)` | Not checking allowed functions | The subject specifies `Allowed functions : None`. Use `type(x) is float and x != x` |
| `x == float("nan")` to detect NaN | Looks logical but NaN never equals anything | Use `type(x) is float and x != x` |
| Two spaces after `Empty:` (`Empty:  <class 'str'>`) | Writing `f"Empty: {x} {type(x)}"` with empty `x` | Write `f"Empty: {type(x)}"` to ensure exactly one space |
| `0` and `False` both landing in the same branch | Checking value before type (`False == 0` is True) | Check `type(x) is bool` separately from `type(x) is int` |
| Using tabs for indentation | Habit from C norminette | PEP 8 / `flake8` forbids tabs (`W191`). Always use 4 spaces |
| Wrong return value on the fallback (`0` instead of `1`) | Copy-paste from the "success" branches | Fallback branch must explicitly `return 1` |

---

## 10. Debugging Guide

- **`Empty:` line has two spaces before `<class 'str'>`** → `f"Empty: {x} {type(x)}"` creates two spaces when `x` is `""`. Use `f"Empty: {type(x)}"`.
- **`False` matching your "zero" branch** → Ensure you test `type(x) is bool` or check boolean before `x == 0`.
- **`flake8` errors (`W191 indentation contains tabs`)** → Replace all tabs with 4 spaces.
- **Peer says `import math` is forbidden** → Replace `math.isnan(x)` with `x != x`.
- Useful inspection: `print(type(x), repr(x))` shows you both the exact type and an unambiguous representation of the value (e.g. `''` vs `None` look different under `repr`).

---

## 11. Cheat Sheet

```python
def NULL_not_found(object: any) -> int:
    """Detect various types of Null without external libraries."""
    obj_type = type(object)
    if object is None:
        print(f"Nothing: {object} {obj_type}")
        return 0
    elif obj_type is float and object != object:
        print(f"Cheese: {object} {obj_type}")
        return 0
    elif obj_type is bool and object is False:
        print(f"Fake: {object} {obj_type}")
        return 0
    elif obj_type is int and object == 0:
        print(f"Zero: {object} {obj_type}")
        return 0
    elif obj_type is str and object == "":
        print(f"Empty: {obj_type}")
        return 0
    else:
        print("Type not Found")
        return 1
```
