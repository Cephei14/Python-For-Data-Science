# Study Tutorial — Exercise 02: find_ft_type.py

## 1. Exercise Overview

**What it asks:** Write a function `all_thing_is_obj(object)` that looks at whatever value it's given, prints a sentence describing its type in a specific human-readable way, and always returns `42`. Different types get different sentences (e.g., a list prints `"List : <class 'list'>"`, a string prints `"<value> is in the kitchen : <class 'str'>"`), and anything unrecognized prints `"Type not found"`.

**Main concepts you'll learn:**
- Writing your first proper Python function, with type hints
- Using `type()` to inspect any value at runtime
- Branching logic (`if`/`elif`/`else`) based on type
- The difference between a script that *runs* logic and a **module** that only *defines* logic (importable without side effects)

**Why this matters:** Real-world data is messy — a column you expect to be all integers might secretly contain strings or `None`. Being able to inspect and branch on type at runtime is a core defensive-programming skill you'll use constantly when cleaning data later (e.g., in the pandas module).

**Skills after completing it:**
- Define a function with a type-annotated parameter and return type
- Use `type()` and compare it against built-in type objects
- Understand why "importing a module shouldn't run its logic"

---

## 2. Prerequisites

- Function basics: `def name(params):`, `return`
- What `if`/`elif`/`else` does
- Knowing that `list`, `tuple`, `set`, `dict`, `str`, `int` are themselves values in Python (they're *type objects*, not just labels)

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `type(x)` | Returns the type object of `x`, e.g. `<class 'list'>` | Compare with `is` or `==` against `list`, `str`, etc. |
| `def f(object: any) -> int:` | Function definition with type hints | `object: any` is the subject's given prototype. Note: in Python, `any` is actually the built-in boolean function, but Python allows it as an annotation without error. In standard code, you'd use `typing.Any`. |
| `if __name__ == "__main__":` | Runs code only when the file is executed directly, not when imported | Explains why "running the function alone does nothing" |
| `f"{x}"` | String interpolation | Used to build the exact required sentence per type |

Common pitfalls:
- Using `isinstance()` when the exercise's expected output distinguishes types precisely by `type()` — for this exercise, plain `type(x) is list` or `type(x) == list` style checks are simplest and match the required exact printed class name.
- Forgetting `bool` is technically a subtype of `int` in Python — `type(True) == int` is `False`, but `isinstance(True, int)` is `True`. This exercise doesn't test booleans, but keep it in mind for Exercise 03.
- Using tabs instead of 4 spaces: 42 C norminette required tabs, but Python PEP 8 / `flake8` strictly requires 4 spaces (`W191`).

---

## 4. Concepts You Need to Learn

### 4.1 Functions and return values
A function is a reusable block of code. `def all_thing_is_obj(object: any) -> int:` declares a function named `all_thing_is_obj` that takes one parameter (`object`) and is documented to return an `int`. Inside, `return 42` sends the value `42` back to whoever called the function.

### 4.2 `type()` — inspecting what something is
```python
type([1, 2, 3])   # <class 'list'>
type("hello")      # <class 'str'>
type(10)           # <class 'int'>
```
`type(x)` doesn't just tell *you* the type for debugging — it returns an actual object you can compare:
```python
type([1, 2, 3]) == list   # True
```

### 4.3 Modules vs. scripts
A `.py` file can be **run directly** (`python file.py`) or **imported** (`from file import something`). If you write top-level code (not inside a function or an `if __name__ == "__main__":` block), it runs *both* when you execute the file directly *and* every time someone imports it — usually not what you want for a reusable function file. Wrapping your test calls in `if __name__ == "__main__":` means they only run when you execute the file directly, not when it's imported elsewhere. This is why the subject says "Running your function alone does nothing" — with no `__main__` block content, importing/running `find_ft_type.py` by itself produces no output; the *tester* script is what calls the function.

---

## 5. Syntax and Examples

### Defining and calling a function
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("Alex"))  # Hello, Alex!
```
`name: str` documents that `name` should be a string; `-> str` documents the return type. Neither is enforced — Python will still run `greet(42)` without error.

### Branching on type
```python
def describe(x):
    if type(x) == list:
        print("It's a list!")
    elif type(x) == str:
        print("It's a string!")
    else:
        print("Unknown type")

describe([1, 2])   # It's a list!
describe("hi")      # It's a string!
describe(3.14)       # Unknown type
```

### Building the exact required sentence
```python
def all_thing_is_obj(object):
    if type(object) == list:
        print(f"List : {type(object)}")
    elif type(object) == str:
        print(f"{object} is in the kitchen : {type(object)}")
    else:
        print("Type not found")
    return 42
```
Notice: `{type(object)}` inside an f-string prints exactly `<class 'list'>` because that's how Python's `type` objects render as strings — you don't need to build that text manually.

---

## 6. How to Think About the Exercise

1. List out every case shown in the expected output: list, tuple, set, dict, string (two different string inputs, same behavior), int (the fallback "Type not found" line), and the final `print(all_thing_is_obj(10))` which shows the return value.
2. Wait — int isn't in the "found" list at all based on the expected output (`10` triggers "Type not found", then separately prints `42` because `print(...)` wraps the *return value*). So: don't add a special case for `int`; let it fall into `else`.
3. Write one `if/elif` branch per known type, each producing its specific required sentence.
4. Every branch — and the fallback — must still `return 42` at the end, since the function's contract is "always returns 42 regardless of what happens."
5. Remember: this file, when run directly (`python find_ft_type.py`), should produce **no output** — meaning no top-level code outside function/class definitions.

---

## 7. Guided Practice

**Practice 1 (Easy):** Write a function `whatami(x)` that prints `"integer"` if `x` is an `int`, `"other"` otherwise, and returns `None`.
<details><summary>Solution</summary>

```python
def whatami(x):
    if type(x) == int:
        print("integer")
    else:
        print("other")
```
</details>

**Practice 2 (Medium):** Extend it to handle `int`, `float`, and `str` with three different messages, falling back to `"unknown"` for anything else.
<details><summary>Solution</summary>

```python
def whatami(x):
    if type(x) == int:
        print("integer")
    elif type(x) == float:
        print("float")
    elif type(x) == str:
        print("string")
    else:
        print("unknown")
```
</details>

**Practice 3 (Close to the real exercise):** Write `describe_and_count(x)` that prints a type-specific message *and* returns the number of times it was called — track this using a mutable default trick... actually, simpler: just make it return a fixed constant like the real exercise (avoid overcomplicating; global counters are against the rules anyway).
<details><summary>Solution</summary>

```python
def describe_and_count(x):
    if type(x) == list:
        print(f"List with {len(x)} items")
    else:
        print("Not a list")
    return 1
```
This mirrors the real exercise's pattern: branch on type, print something type-specific, return a fixed value.
</details>

---

## 8. Exercise-Specific Knowledge

- Exact required outputs (from the subject):
  - list → `List : <class 'list'>`
  - tuple → `Tuple : <class 'tuple'>`
  - set → `Set : <class 'set'>`
  - dict → `Dict : <class 'dict'>`
  - str → `<value> is in the kitchen : <class 'str'>`
  - anything else (e.g. `10`) → `Type not found`
- The function always returns `42`, regardless of the branch taken.
- Running `find_ft_type.py` directly must produce **zero output** — confirming there's no stray top-level code.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Using `isinstance()` and getting unexpected matches (e.g. `bool` matching `int`) | Not knowing `bool` is a subclass of `int` | For this exercise, `type(x) is list` style exact-type checks avoid the subclass trap |
| Adding top-level `print()` calls or test calls outside a function | Habit from ex00/ex01 | Keep the file to *only* the function definition — no executable code |
| Forgetting `return 42` in one of the branches | Easy to miss when adding `elif` branches | Put `return 42` once, after all branches, not duplicated inside each one |
| Missing colon/space in the printed sentence (`List :` vs `List:`) | Not matching the subject's exact spacing | Copy the exact punctuation and spacing from the subject |
| Using tabs for indentation | Habit from 42 C norminette | Python flake8 reports `W191 indentation contains tabs`. Convert all tabs to 4 spaces |
| Leaving unused scratch variables (e.g. `flag = True`) | Forgetting to clean up code | Flake8 reports `F841 local variable is assigned to but never used`. Remove dead code |

---

## 10. Debugging Guide

- **`NameError: name 'all_thing_is_obj' is not defined`** in your tester → check your `from find_ft_type import all_thing_is_obj` import line matches the actual function name exactly.
- **`flake8` errors (`W191`, `F841`, `W292`)** → Replace tabs with 4 spaces, remove any unused variables, and make sure the file ends with a blank newline.
- **Wrong sentence printed** → `print(type(object))` alone first, to confirm what Python actually reports before wrapping it in your f-string.
- **Extra blank output when running the file directly** → search for any `print()` or function call sitting outside a `def` block.
- Useful inspection: `print(repr(x))` if you're unsure exactly what value is being passed in your tester.

---

## 11. Cheat Sheet

```python
def all_thing_is_obj(object: any) -> int:
    """Print the type of object and return 42."""
    if type(object) == list:
        print(f"List : {type(object)}")
    elif type(object) == tuple:
        print(f"Tuple : {type(object)}")
    elif type(object) == set:
        print(f"Set : {type(object)}")
    elif type(object) == dict:
        print(f"Dict : {type(object)}")
    elif type(object) == str:
        print(f"{object} is in the kitchen : {type(object)}")
    else:
        print("Type not found")
    return 42
```

---

## 12. Knowledge Checklist

- [ ] I can define a function with type-hinted parameters and a return type.
- [ ] I can use `type(x)` and compare it to built-in type objects.
- [ ] I understand why importing a file shouldn't execute top-level logic.
- [ ] I can branch on type with `if/elif/else` and produce type-specific output.
- [ ] I know `bool` is technically a subtype of `int`, and why that matters for `isinstance()`.
