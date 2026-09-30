# Study Tutorial — Exercise 06: ft_filter.py & filterstring.py

## 1. Exercise Overview

**What it asks:**
This exercise has two distinct parts:
1. **Part 1 (`ft_filter.py`):** Reimplement Python's built-in `filter()` function from scratch using a **list comprehension**. Using the real `filter()` is strictly forbidden. Your function must also have a docstring that reflects `filter.__doc__`.
2. **Part 2 (`filterstring.py`):** Write a standalone CLI program that takes two arguments: a string `S` and an integer `N`. The program outputs a list of words from `S` whose length is strictly greater than `N`.
   - Must use at least **one list comprehension** and at least **one `lambda`**.
   - If argument count is not 2, or if argument types are invalid, print:
     `AssertionError: the arguments are bad`.
   - Must follow all mandatory rules from Exercise 05 (`main()`, docstrings, caught exceptions, `flake8`).

**Main concepts you'll learn:**
- **List comprehensions:** Python's elegant syntax for transforming and filtering sequences.
- **Lambdas:** Quick, single-line anonymous functions.
- **Higher-order functions:** Functions that take other functions as arguments.
- **String tokenization:** Splitting text into words using `str.split()`.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **Lists & Strings (ex00, ex05):** Indexing, iterating over sequences, measuring length with `len()`.
- **Functions & Docstrings (ex02, ex05):** Defining functions with `def`, adding `"""docstrings"""`.
- **CLI Arguments & Exceptions (ex04, ex05):** Accessing `sys.argv`, validating types with `try ... except`, and catching `AssertionError` inside `main()`.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `[x for x in seq if cond]` | List comprehension (creates a new filtered list) | Core requirement for both Part 1 and Part 2 |
| `lambda x: x > n` | Anonymous inline function | Core requirement for Part 2 |
| `str.split()` | Splits a string into a list of words by whitespace | `"Hello World".split() -> ['Hello', 'World']` |
| `import sys` | Accesses CLI arguments via `sys.argv` | Used in Part 2 |
| `filter` (built-in) | **FORBIDDEN** in this exercise | You are writing `ft_filter` to replace it |

Common pitfalls:
- Using the forbidden `filter()`: Even if called accidentally, using the built-in `filter` results in an immediate 0.
- Forgetting to include BOTH a list comprehension and a lambda in Part 2: The subject strictly grades the presence of both language constructs.
- Checking types in reverse: Notice in the subject tester that `python filterstring.py 3 'Hello'` prints `AssertionError: the arguments are bad`. The first argument must be the string, and the second must be the integer!

---

## 4. Concepts You Need to Learn

### 4.1 Understanding List Comprehensions

Until now, whenever you wanted to filter a list, you wrote a traditional loop:
```python
# The loop approach:
words = ["apple", "bat", "carrot", "dog"]
long_words = []
for w in words:
    if len(w) > 3:
        long_words.append(w)
```

A **list comprehension** performs the exact same operation in a single, readable line:
```python
# The list comprehension approach:
long_words = [w for w in words if len(w) > 3]
```

Read it aloud from left to right:
*"Give me `w`, for each `w` in `words`, only if `len(w) > 3`."*

The syntax pattern:
```
[<EXPRESSION> for <ITEM> in <ITERABLE> if <CONDITION>]
```

### 4.2 Understanding `lambda` (Anonymous Functions)

Normally, you define a function using `def`:
```python
def is_even(n):
    """Check if number is even."""
    return n % 2 == 0
```

When you only need a quick, one-line function to evaluate a condition, Python lets you create a **lambda** (an anonymous function without a name):
```python
# Syntax: lambda <parameters>: <expression to return>
is_even = lambda n: n % 2 == 0

print(is_even(4))  # True
print(is_even(5))  # False
```
Notice:
- No `def` keyword.
- No `return` statement (the expression result is returned automatically).
- No docstring.

In Part 2, the subject requires you to use a lambda to check word length:
```python
check_length = lambda word: len(word) > n
```

### 4.3 Part 1: Reimplementing `filter` (`ft_filter.py`)

What does Python's built-in `filter(function, iterable)` do?
It tests each item in `iterable` using `function(item)`:
- If `function(item)` returns `True` (or a truthy value), the item is kept.
- If `function` is `None`, Python keeps items that are truthy on their own.

Using a list comprehension, `ft_filter` can be implemented directly:
```python
def ft_filter(function, iterable):
    """filter(function or None, iterable) --> filter object

Return an iterator yielding those items of iterable for which function(item)
is true. If function is None, return the items that are true.
"""
    if function is None:
        return [item for item in iterable if item]
    return [item for item in iterable if function(item)]
```
*(Note: Built-in `filter` returns an iterator. In Python, a list or an iterator created via `iter([...])` works smoothly. Using the list comprehension directly meets the subject requirement).*

### 4.4 Part 2: Splitting Strings and Argument Validation

`str.split()` without arguments splits text by spaces and strips redundant whitespace:
```python
text = "Hello    the   World"
print(text.split())  # ['Hello', 'the', 'World']
```

The subject specifies:
- Argument 1 (`sys.argv[1]`): String `S` (must not contain punctuation).
- Argument 2 (`sys.argv[2]`): Integer `N`.
- Any mismatch in argument count or types must print:
  `AssertionError: the arguments are bad`

How to validate:
1. `len(sys.argv) == 3` (script name + 2 arguments).
2. `int(sys.argv[2])` succeeds (using `try ... except ValueError`).
3. `sys.argv[1]` is a valid string without punctuation (e.g. check `char in string.punctuation`).

---

## 5. Syntax and Examples

### Combining Lambda and List Comprehension

```python
text = "Hello the World"
n = 4

# Lambda definition
is_longer = lambda w: len(w) > n

# List comprehension utilizing the lambda
result = [word for word in text.split() if is_longer(word)]
print(result)  # ['Hello', 'World']
```

---

## 6. How to Think About the Exercise

### For `ft_filter.py`:
1. Take two arguments: `function` and `iterable`.
2. Set the docstring to match `filter.__doc__`.
3. Use a list comprehension to filter elements where `function(item)` is truthy.
4. Keep the file importable without executing top-level code.

### For `filterstring.py`:
1. Check `len(sys.argv) == 3`. If not, raise `AssertionError("the arguments are bad")`.
2. Try parsing `sys.argv[2]` with `int()`. If it fails, raise `AssertionError("the arguments are bad")`.
3. Check `sys.argv[1]`: verify it does not contain punctuation symbols.
4. Split the string into words.
5. Filter with `lambda` + list comprehension.
6. Print the resulting list directly.
7. Wrap in `main()` and catch `AssertionError`.

---

## 7. Guided Practice

These six drills go from easiest to hardest, and cover **both** parts of the
exercise — `ft_filter.py` first, then `filterstring.py`. Each step adds one more
requirement from the subject, ending with the two complete, rule-compliant files.

**Practice 1 (Easiest — list comprehension warm-up):**
Given `numbers = [1, 2, 3, 4, 5, 6]`, use a list comprehension to extract numbers
greater than 3.

Expected output:

```python
print(greater)  # [4, 5, 6]
```

<details><summary>Solution</summary>

```python
numbers = [1, 2, 3, 4, 5, 6]
greater = [n for n in numbers if n > 3]
print(greater)  # [4, 5, 6]
```
</details>

**Practice 2 (A lambda on its own):**
Write a lambda `has_min_len` that takes a word and an integer `min_len`, returning
`True` if `len(word) >= min_len`.

Expected output:

| Call | Result |
|---|---|
| `has_min_len("data", 4)` | `True` |
| `has_min_len("ai", 4)` | `False` |

<details><summary>Solution</summary>

```python
has_min_len = lambda word, min_len: len(word) >= min_len
print(has_min_len("data", 4))  # True
print(has_min_len("ai", 4))    # False
```
</details>

**Practice 3 (Part 1 — build `ft_filter` itself):**
Now combine Practices 1 and 2: write `ft_filter(function, iterable)` using a list
comprehension, matching the behavior of the built-in `filter()` (including the
`function is None` case from section 4.3). This *is* the exercise's Part 1.

Expected output:

| Call | Result |
|---|---|
| `ft_filter(lambda x: x > 3, [1, 2, 3, 4, 5, 6])` | `[4, 5, 6]` |
| `ft_filter(None, [0, 1, "", "hi", None])` | `[1, "hi"]` |

<details><summary>Solution</summary>

```python
def ft_filter(function, iterable):
    """filter(function or None, iterable) --> filter object

Return an iterator yielding those items of iterable for which function(item)
is true. If function is None, return the items that are true.
"""
    if function is None:
        return [item for item in iterable if item]
    return [item for item in iterable if function(item)]
```
</details>

**Practice 4 (Part 2 — validate the two CLI arguments, no filtering yet):**
Before touching `ft_filter`, get argument validation right on its own. Write a
function that checks `sys.argv`: exactly 2 arguments, the first containing no
punctuation, and the second convertible with `int()`. On success, just print
`"OK"`; on any failure, raise `AssertionError("the arguments are bad")`.

Expected output:

| Command | Output |
|---|---|
| `python practice.py` | `AssertionError: the arguments are bad` |
| `python practice.py 3 'Hello the World'` | `AssertionError: the arguments are bad` |
| `python practice.py 'Hello the World' 4` | `OK` |

<details><summary>Solution</summary>

```python
import sys
import string


def validate_args() -> tuple:
    """Validate CLI arguments and return (text, n) if they're valid."""
    if len(sys.argv) != 3:
        raise AssertionError("the arguments are bad")

    text = sys.argv[1]
    for char in text:
        if char in string.punctuation:
            raise AssertionError("the arguments are bad")

    try:
        n = int(sys.argv[2])
    except ValueError:
        raise AssertionError("the arguments are bad")

    return text, n
```
</details>

**Practice 5 (Filter the words, using your own `ft_filter`):**
Now that Practice 4 gives you a clean `(text, n)` pair, split `text` into words
and use `ft_filter` from Practice 3 — combined with a `lambda` — to keep only
words longer than `n`.

Expected output:

```python
print(filter_words("Hello the World", 4))  # ['Hello', 'World']
print(filter_words("Hello the World", 99))  # []
```

<details><summary>Solution</summary>

```python
def filter_words(text: str, n: int) -> list:
    """Return words from text with length strictly greater than n."""
    is_longer = lambda word: len(word) > n
    return ft_filter(is_longer, text.split())
```
</details>

**Practice 6 (Hardest — the full, rule-compliant `filterstring.py`):**
Combine Practices 3, 4 and 5 into the final program: docstrings, everything inside
`main()`, and `AssertionError` caught cleanly.

Expected output — check all four against your solution:

| Command | Output |
|---|---|
| `python practice.py 'Hello the World' 4` | `['Hello', 'World']` |
| `python practice.py 'Hello the World' 99` | `[]` |
| `python practice.py 3 'Hello the World'` | `AssertionError: the arguments are bad` |
| `python practice.py` | `AssertionError: the arguments are bad` |

<details><summary>Solution</summary>

```python
import sys
import string


def ft_filter(function, iterable):
    """filter(function or None, iterable) --> filter object

Return an iterator yielding those items of iterable for which function(item)
is true. If function is None, return the items that are true.
"""
    if function is None:
        return [item for item in iterable if item]
    return [item for item in iterable if function(item)]


def validate_args() -> tuple:
    """Validate CLI arguments and return (text, n) if they're valid."""
    if len(sys.argv) != 3:
        raise AssertionError("the arguments are bad")

    text = sys.argv[1]
    for char in text:
        if char in string.punctuation:
            raise AssertionError("the arguments are bad")

    try:
        n = int(sys.argv[2])
    except ValueError:
        raise AssertionError("the arguments are bad")

    return text, n


def filter_words(text: str, n: int) -> list:
    """Return words from text with length strictly greater than n."""
    is_longer = lambda word: len(word) > n
    return ft_filter(is_longer, text.split())


def main():
    """Validate CLI arguments and print the filtered word list."""
    try:
        text, n = validate_args()
        print(filter_words(text, n))
    except AssertionError as error:
        print(f"AssertionError: {error}")


if __name__ == "__main__":
    main()
```
</details>

If all four Practice 6 outputs match, save `ft_filter` in `ft_filter.py` and the
rest in `filterstring.py` (importing `ft_filter` from the first file) — you're done.

---

## 8. Exercise-Specific Knowledge

- **`ft_filter.py` vs built-in `filter`:**
  Under no circumstance should the word `filter(` appear in your code (except for docstrings or in your own function name `ft_filter`).
- **Exact Error Message:**
  Every invalid input case (wrong number of arguments, integer in place of string, float in place of int) must print exactly:
  `AssertionError: the arguments are bad`
- **Printed Output:**
  `print(result)` prints lists in standard Python representation (e.g. `['Hello', 'World']`), matching the subject output.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Calling built-in `filter()` | Old habits | Use `[x for x in iterable if function(x)]` |
| Missing `lambda` in `filterstring.py` | Filtering inline inside the comprehension | Create `condition = lambda w: len(w) > n` |
| Accepting punctuation in `S` | Ignoring subject note on special characters | Reject strings containing `string.punctuation` |
| Wrong argument order | Passing integer first | Reject if arg 1 cannot be text or if arg 2 is not int |
| Traceback on bad input | Raising unhandled `AssertionError` | Wrap in `try ... except AssertionError:` in `main()` |

---

## 10. Debugging Guide

- **`NameError: name 'filter' is not defined`**: Ensure you named your custom function `ft_filter` and imported it properly.
- **`SyntaxError: invalid syntax` in list comprehension**: Remember the order: `[expression for item in iterable if condition]`.
- **`flake8` reports lambda assignment warning (`E731`)**: If flake8 warns against assigning a lambda (`E731 do not assign a lambda expression, use a def`), pass the lambda directly:
  `[w for w in text.split() if (lambda word: len(word) > n)(w)]` or define `condition = lambda ...` if your flake8 configuration allows it.

---

## 11. Cheat Sheet

### `ft_filter.py`
```python
def ft_filter(function, iterable):
    """filter(function or None, iterable) --> filter object

Return an iterator yielding those items of iterable for which function(item)
is true. If function is None, return the items that are true.
"""
    if function is None:
        return [item for item in iterable if item]
    return [item for item in iterable if function(item)]
```

### `filterstring.py`
```python
import sys
import string


def filter_words(text: str, n: int) -> list:
    """Filter words in text with length strictly greater than n."""
    is_longer = lambda w: len(w) > n
    return [w for w in text.split() if is_longer(w)]


def main():
    """Validate arguments and display filtered word list."""
    try:
        if len(sys.argv) != 3:
            raise AssertionError("the arguments are bad")

        text = sys.argv[1]
        for c in text:
            if c in string.punctuation:
                raise AssertionError("the arguments are bad")

        try:
            n = int(sys.argv[2])
        except ValueError:
            raise AssertionError("the arguments are bad")

        print(filter_words(text, n))
    except AssertionError as error:
        print(f"AssertionError: {error}")


if __name__ == "__main__":
    main()
```

---

## 12. Knowledge Checklist

- [ ] I can write a list comprehension with a filtering condition.
- [ ] I can write and invoke a `lambda` function.
- [ ] I understand how `ft_filter` works without using built-in `filter`.
- [ ] I can tokenize text into words using `str.split()`.
- [ ] I have validated argument count, types, and special characters, printing `AssertionError: the arguments are bad` when invalid.
- [ ] Both files pass `flake8` cleanly.
