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

---

## 12. All test cases
## ex00: ScalarConverter

| # | Input | char | int | float | double |
|---|-------|------|-----|-------|--------|
| 1 | `0` | Non displayable | 0 | 0.0f | 0.0 |
| 2 | `nan` | impossible | impossible | nanf | nan |
| 3 | `42.0f` | '*' | 42 | 42.0f | 42.0 |
| 4 | `a` or `'a'` | 'a' | 97 | 97.0f | 97.0 |
| 5 | `*` | '*' | 42 | 42.0f | 42.0 |
| 6 | `5` (a digit is an int, not the char) | Non displayable | 5 | 5.0f | 5.0 |
| 7 | `42` | '*' | 42 | 42.0f | 42.0 |
| 8 | `-42` | impossible / Non displayable | -42 | -42.0f | -42.0 |
| 9 | `31` | Non displayable | 31 | 31.0f | 31.0 |
| 10 | `32` | ' ' | 32 | 32.0f | 32.0 |
| 11 | `126` | '~' | 126 | 126.0f | 126.0 |
| 12 | `127` | Non displayable | 127 | 127.0f | 127.0 |
| 13 | `128` | impossible | 128 | 128.0f | 128.0 |
| 14 | `2147483647` | impossible | 2147483647 | 2147483648.0f | 2147483647.0 |
| 15 | `-2147483648` | impossible | -2147483648 | -2147483648.0f | -2147483648.0 |
| 16 | `2147483648` | impossible | impossible | 2147483648.0f | 2147483648.0 |
| 17 | `-2147483649` | impossible | impossible | -2147483648.0f | -2147483649.0 |
| 18 | `0.0f` | Non displayable | 0 | 0.0f | 0.0 |
| 19 | `4.2f` | Non displayable | 4 | 4.2f | 4.2 |
| 20 | `-4.2f` | impossible / Non displayable | -4 | -4.2f | -4.2 |
| 21 | `42.5f` | '*' | 42 | 42.5f | 42.5 |
| 22 | `65.0f` | 'A' | 65 | 65.0f | 65.0 |
| 23 | `0.0` | Non displayable | 0 | 0.0f | 0.0 |
| 24 | `4.2` | Non displayable | 4 | 4.2f | 4.2 |
| 25 | `-4.2` | impossible / Non displayable | -4 | -4.2f | -4.2 |
| 26 | `1000000.5` | impossible | 1000000 | 1000000.5f | 1000000.5 |
| 27 | `2147483648.0` | impossible | impossible | 2147483648.0f | 2147483648.0 |
| 28 | `1000000000000000000000000000000000000000.0` | impossible | impossible | impossible (or inf) | large value |
| 29 | `nanf` | impossible | impossible | nanf | nan |
| 30 | `-inff` | impossible | impossible | -inff | -inf |
| 31 | `+inff` | impossible | impossible | +inff | +inf |
| 32 | `-inf` | impossible | impossible | -inff | -inf |
| 33 | `+inf` | impossible | impossible | +inff | +inf |

### ex00: invalid input and robustness

| # | Input | Expected |
|---|-------|----------|
| 34 | `abc`, `""`, `" "` | No crash. Recommended: all four lines `impossible` |
| 35 | `42ff`, `4.2.2`, `4.2ff`, `nanff` | No crash, all `impossible` |
| 36 | `++1`, `--5`, `+-3`, `.`, `f`, `.f` | No crash, all `impossible` |
| 37 | `NAN`, `Inf`, `0x1A`, `1e5`, `42abc` | No crash, all `impossible` |
| 38 | A 300-digit number | No crash, no hang |
| 39 | No argument, or `1 2 3` | Usage message, no crash |

### ex00: class rules

| # | Test | Expected |
|---|------|----------|
| 40 | `ScalarConverter a;` | Does not compile |
| 41 | `new ScalarConverter()` | Does not compile |
| 42 | Copy construction | Does not compile |
| 43 | Assignment | Does not compile |
| 44 | `ScalarConverter::convert("42");` | Compiles |
| 45 | Output goes to stdout, each line ends with `\n` | `./convert 42 \| cat -A` shows `$` at each line end |

## ex01: Serializer

| # | Test | Expected |
|---|------|----------|
| 1 | `sizeof(Data) > 1` | `Data` is non-empty |
| 2 | Stack object: `deserialize(serialize(&d)) == &d` | true |
| 3 | `serialize(&d) == reinterpret_cast<uintptr_t>(&d)` | true |
| 4 | Heap object round trip | Same pointer |
| 5 | Two different objects | Different raw values |
| 6 | Members read through the deserialized pointer | Unchanged values |
| 7 | `serialize(NULL)` | 0 |
| 8 | `deserialize(0)` | NULL |
| 9 | Double round trip | Same pointer |
| 10 | `Serializer s;` / `new Serializer()` | Does not compile |
| 11 | Valgrind | No leaks, no errors |
| 12 | `grep` for `reinterpret_cast`, and no C-style casts | Found / none |

## ex02: Identify real type

| # | Test | Expected |
|---|------|----------|
| 1 | `identify(Base*)` on a directly created `A` | `A` |
| 2 | `identify(Base*)` on `B` | `B` |
| 3 | `identify(Base*)` on `C` | `C` |
| 4 | `identify(Base&)` on `A` | `A` |
| 5 | `identify(Base&)` on `B` | `B` |
| 6 | `identify(Base&)` on `C` | `C` |
| 7 | 500 × `generate()`, pointer and reference versions vs real type | Always match |
| 8 | Distribution over 500 `generate()` calls | A, B and C all appear, each above about 10% |
| 9 | Several program runs | Different sequences (seeded once, not inside `generate()`) |
| 10 | `delete` on a `Base*` | No leak (virtual destructor) |
| 11 | `identify(NULL)` | No crash |
| 12 | `grep -rn "typeinfo\|typeid" ex02/` | Nothing found |
| 13 | `identify(Base&)` contains no pointer | Only `dynamic_cast<X&>` with `try/catch` |
| 14 | Catch uses `std::exception&` or `...` | Not `std::bad_cast` |
| 15 | `Base` has only a public virtual destructor, and A, B, C are empty and `: public Base` | Matches the subject |
| 16 | Valgrind | No leaks, no errors |

## General rules (all exercises)

| # | Test | Expected |
|---|------|----------|
| 1 | Build with `-Wall -Wextra -Werror -std=c++98` | No warnings or errors |
| 2 | `make` twice | Second run does not relink |
| 3 | `make clean`, `fclean`, `re` | Work correctly |
| 4 | `grep "using namespace\|friend"` | Nothing found |
| 5 | `grep "printf\|malloc\|free"` | Nothing found |
| 6 | `grep "<vector>\|<map>\|<algorithm>"` | Nothing found |
| 7 | Headers without `#ifndef` / `#pragma once` | None |
| 8 | Each header compiles alone and when included twice | OK |
| 9 | No function bodies in headers | OK |
| 10 | ex00 uses `static_cast` | Present |
| 11 | ex01 uses `reinterpret_cast` | Present |
| 12 | ex02 uses `dynamic_cast` | Present |

Rows marked "impossible / Non displayable" can go either way, since the subject doesn't say how to treat non-ASCII values. Just be consistent.

I can also add these tables to `CPP06_TESTS.md` if you want them in the file.
