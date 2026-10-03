# Study Tutorial — OOP Module, Exercise 03: ft_calculator.py (vector and scalar)

## 1. Exercise Overview

**What it asks:**
Create a file `ft_calculator.py` in directory `ex03/` with a class `calculator` that stores a **vector** (a list of numbers) and can compute with a **scalar** (a single number):
- addition: `vector + 5`
- multiplication: `vector * 5`
- subtraction: `vector - 5`
- division: `vector / 5`

using Python's **operator methods** `__add__`, `__mul__`, `__sub__`, `__truediv__`.

**The subject's prototype:**
```python
class calculator:
    #your code here

    def __add__(self, object) -> None:
        #your code here
    def __mul__(self, object) -> None:
        #your code here
    def __sub__(self, object) -> None:
        #your code here
    def __truediv__(self, object) -> None:
        #your code here
```

**The subject's tester and expected output:**
```python
from ft_calculator import calculator

v1 = calculator([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
v1 + 5
print("---")
v2 = calculator([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
v2 * 5
print("---")
v3 = calculator([10.0, 15.0, 20.0])
v3 - 5
v3 / 5
```
```
[5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
---
[0.0, 5.0, 10.0, 15.0, 20.0, 25.0]
---
[5.0, 10.0, 15.0]
[1.0, 2.0, 3.0]
```

Look closely at the last two lines: `v3 - 5` gives `[5.0, 10.0, 15.0]`, and `v3 / 5` then gives `[1.0, 2.0, 3.0]`. That is `[5, 10, 15] / 5`, **not** `[10, 15, 20] / 5` (which would be `[2.0, 3.0, 4.0]`). So each operation **modifies the stored vector** and each operator **prints the result** (the methods return `None`, as in the prototype).

**Rules and Constraints:**
- File to turn in: `ft_calculator.py`. Allowed functions: **None** (no libraries such as `numpy`; no imports are needed).
- **Error handling:** none required, **except the division by 0**.
- Docstrings on the class and on every method (including `__init__`).
- No globals, `flake8` clean, Python 3.10+. Any uncaught exception invalidates the exercise.

**Main concepts you'll learn:**
- Operator overloading with "dunder" (double-underscore) methods.
- Storing state in the object and updating it in place.
- List comprehensions applied to a list.
- Handling `ZeroDivisionError`.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **ex00 / ex01:** classes, `__init__`, `self`, instance attributes, methods, docstrings.
- Lists, loops, list comprehensions, `print`.
- `try/except`.
- Type hints such as `list[float]`.

---

## 3. Tools and Libraries

| Tool / Syntax | What it does | Scope / Notes |
|---|---|---|
| `class calculator:` | Defines the class (lowercase name, as in the subject) | Keep the subject's name exactly |
| `def __init__(self, vector: list[float]) -> None:` | Constructor: receives the list | Stores it in `self.vector` |
| `self.vector = vector` | Instance attribute holding the numbers | Updated by every operation |
| `def __add__(self, object) -> None:` | Runs when you write `calc + something` | Dunder = "double underscore" |
| `def __mul__(self, object) -> None:` | Runs for `calc * something` | |
| `def __sub__(self, object) -> None:` | Runs for `calc - something` | |
| `def __truediv__(self, object) -> None:` | Runs for `calc / something` | `/` is `__truediv__`; `//` would be `__floordiv__` |
| `[x + object for x in self.vector]` | Builds a new list by applying an operation to each element | List comprehension |
| `self.vector = [...]` | Replaces the stored list with the new one | The in-place update the expected output needs |
| `print(self.vector)` | Prints the list, e.g. `[5.0, 6.0]` | Each operator prints its result |
| `try: ... except ZeroDivisionError:` | Catches a division by zero | Required only for `/` |
| `return` (inside a method) | Leaves the method early | Used after printing the error message |
| `list[float]` | Type hint for a list of floats | Python 3.9+ syntax |

**Common pitfalls:**
- **Not storing the result back:** `[x + object for x in self.vector]` alone changes nothing; assign it to `self.vector`, or `v3 / 5` will use the old values.
- **Returning the result instead of printing it:** the tester's statements (`v1 + 5`) don't print anything by themselves; the methods must `print`.
- **Printing before the division check:** on `/ 0`, don't print a vector; print an error message instead.
- **`v / 0` crashing** with `ZeroDivisionError`: an uncaught exception invalidates the exercise. Catch it.
- **Using `//` or `__div__`:** `/` is `__truediv__`. `__div__` only existed in Python 2.
- **Integer results:** `[x * object ...]` with float inputs stays float (`5.0`). Don't wrap in `int()`.
- **Modifying the list while iterating** (`for i in ...: self.vector[i] += ...` is fine, but a `for x in self.vector: x += 1` changes nothing, since `x` is a copy of the number).
- **Missing docstrings** on `__init__` or the operator methods.

---

## 4. Concepts You Need to Learn

### 4.1 Operator overloading ("dunder" methods)
When Python sees `a + b`, it actually calls `a.__add__(b)`. If your class defines `__add__`, you decide what `+` means for your objects:

| Expression | Method called |
|---|---|
| `a + b` | `a.__add__(b)` |
| `a - b` | `a.__sub__(b)` |
| `a * b` | `a.__mul__(b)` |
| `a / b` | `a.__truediv__(b)` |

In `v1 + 5`: `self` is `v1` and the second parameter (`object` in the prototype) is `5`.

> The prototype names the second parameter `object`, which hides Python's built-in `object`. It works and `flake8` accepts it, but if you rename it (for example `scalar`), nothing else changes. Keeping the prototype's name is the safest for the defence.

### 4.2 Storing the vector
```python
class calculator:
    """Apply scalar operations to a vector."""

    def __init__(self, vector: list[float]) -> None:
        """Store the vector."""
        self.vector = vector
```
The tester creates `calculator([0.0, 1.0, ...])`, so the constructor receives the list and keeps it on the object.

### 4.3 Applying an operation to every element
A list comprehension builds a new list from an old one:
```python
[x + 5 for x in [0.0, 1.0, 2.0]]    # [5.0, 6.0, 7.0]
```
Inside the class, the scalar is the method's parameter:
```python
def __add__(self, object: float) -> None:
    """Add a scalar to every element, then print the vector."""
    self.vector = [x + object for x in self.vector]
    print(self.vector)
```
Three things happen: compute the new list, **store it** in `self.vector`, **print** it. The same pattern applies to `*` and `-`.

### 4.4 Why the vector must be updated in place
The tester chains two operations on `v3` without storing anything:
```python
v3 = calculator([10.0, 15.0, 20.0])
v3 - 5     # prints [5.0, 10.0, 15.0]   -> v3.vector is now [5.0, 10.0, 15.0]
v3 / 5     # prints [1.0, 2.0, 3.0]     -> computed from [5.0, 10.0, 15.0]
```
The expected `[1.0, 2.0, 3.0]` proves the subtraction changed `v3` itself. If your `__sub__` printed the right numbers but didn't update `self.vector`, `v3 / 5` would print `[2.0, 3.0, 4.0]`.

(In real life, returning a **new** calculator would be cleaner, because operators usually don't mutate. This exercise explicitly asks for print + `None`, so follow the subject.)

### 4.5 Division by zero
`x / 0` raises `ZeroDivisionError`, even for floats (`1.0 / 0` too). The subject asks you to handle it, so the exercise doesn't crash:
```python
def __truediv__(self, object: float) -> None:
    """Divide every element by a scalar, then print the vector."""
    try:
        self.vector = [x / object for x in self.vector]
    except ZeroDivisionError:
        print("Error: division by zero")
        return
    print(self.vector)
```
- The assignment happens only if the whole list comprehension succeeded, so after an error the vector is **unchanged**.
- You print a clear message and return; you don't re-raise. A tester that calls `v / 0` without a `try` would otherwise crash, and "any exception not caught will invalidate the exercise".

### 4.6 What each operator returns
Per the prototype, every operator method returns `None` (`-> None`). A consequence: `v1 + 5 + 1` fails, because `(v1 + 5)` is `None` and `None + 1` is an error. That's fine for this exercise: the tester uses one operation per line.

---

## 5. Syntax and Examples

### Step-by-step snippet
```python
class Box:
    """A bag of numbers."""

    def __init__(self, values: list[float]) -> None:
        """Store the values."""
        self.values = values

    def __add__(self, n: float) -> None:
        """Add n to every value, then print them."""
        self.values = [v + n for v in self.values]
        print(self.values)


def main() -> None:
    """Show that the operation updates the object."""
    b = Box([1.0, 2.0])
    b + 5
    b + 5


if __name__ == "__main__":
    main()
```
Output:
```
[6.0, 7.0]
[11.0, 12.0]
```
The second `b + 5` starts from the updated values.

---

## 6. How to Think About the Exercise

1. **Step 1: Write the class and `__init__`** that stores the list in `self.vector`.
2. **Step 2: Write `__add__`**: comprehension, store, print. Test with `v1 + 5`.
3. **Step 3: Copy the same pattern** for `__mul__` and `__sub__`.
4. **Step 4: Write `__truediv__`** with `try/except ZeroDivisionError`.
5. **Step 5: Run the subject's tester** and check the four result lines, especially the last two.
6. **Step 6: Test the error case yourself:** `calculator([1.0, 2.0]) / 0` prints a message and doesn't crash; the vector is unchanged.
7. **Step 7: Docstrings and `flake8`.**

---

## 7. Guided Practice

**Practice 1 (Easiest, an operator on your own class):**
Create `Money(amount)` with `__add__(self, other)` returning a new `Money`. Print the amount of `Money(10) + Money(5)`.

Expected output:
```
15
```

<details><summary>Solution</summary>

```python
class Money:
    """An amount of money."""

    def __init__(self, amount: float) -> None:
        """Store the amount."""
        self.amount = amount

    def __add__(self, other: "Money") -> "Money":
        """Return a new Money with the sum of the two amounts."""
        return Money(self.amount + other.amount)


def main() -> None:
    """Use the + operator on two Money objects."""
    total = Money(10) + Money(5)
    print(total.amount)


if __name__ == "__main__":
    main()
```
</details>

**Practice 2 (Apply an operation to every element):**
Write a function `add_all(values, n)` that returns a new list with `n` added to each value, using a list comprehension. Test with `[0.0, 1.0, 2.0]` and `5`.

Expected output:
```
[5.0, 6.0, 7.0]
```

<details><summary>Solution</summary>

```python
def add_all(values: list[float], n: float) -> list[float]:
    """Return a new list with n added to every value."""
    return [v + n for v in values]


def main() -> None:
    """Test add_all."""
    print(add_all([0.0, 1.0, 2.0], 5))


if __name__ == "__main__":
    main()
```
</details>

**Practice 3 (An operator that updates the object and prints):**
Create `Box(values)` with `__add__` that updates `self.values` and prints them. Run `b + 5` twice on `Box([1.0, 2.0])`.

Expected output:
```
[6.0, 7.0]
[11.0, 12.0]
```

<details><summary>Solution</summary>

```python
class Box:
    """A bag of numbers."""

    def __init__(self, values: list[float]) -> None:
        """Store the values."""
        self.values = values

    def __add__(self, n: float) -> None:
        """Add n to every value, then print them."""
        self.values = [v + n for v in self.values]
        print(self.values)


def main() -> None:
    """Show that the operation updates the object."""
    b = Box([1.0, 2.0])
    b + 5
    b + 5


if __name__ == "__main__":
    main()
```
</details>

**Practice 4 (Safe division):**
Create `Box` with a `__truediv__` that prints the divided values, or prints `Error: division by zero` (and leaves the values unchanged) when the divisor is `0`. Run `b / 2`, `b / 0`, then `b / 2` again on `Box([8.0, 4.0])`.

Expected output:
```
[4.0, 2.0]
Error: division by zero
[2.0, 1.0]
```

<details><summary>Solution</summary>

```python
class Box:
    """A bag of numbers."""

    def __init__(self, values: list[float]) -> None:
        """Store the values."""
        self.values = values

    def __truediv__(self, n: float) -> None:
        """Divide every value by n, or report a division by zero."""
        try:
            self.values = [v / n for v in self.values]
        except ZeroDivisionError:
            print("Error: division by zero")
            return
        print(self.values)


def main() -> None:
    """Divide normally, then by zero, then normally again."""
    b = Box([8.0, 4.0])
    b / 2
    b / 0
    b / 2


if __name__ == "__main__":
    main()
```
</details>

**Practice 5 (Hardest, the full rule-compliant `ft_calculator.py`):**

Expected output with the subject's tester: see section 1.

<details><summary>Solution</summary>

```python
class calculator:
    """Apply scalar operations (+, *, -, /) to a vector."""

    def __init__(self, vector: list[float]) -> None:
        """Store the vector."""
        self.vector = vector

    def __add__(self, object: float) -> None:
        """Add a scalar to every element, then print the vector."""
        self.vector = [x + object for x in self.vector]
        print(self.vector)

    def __mul__(self, object: float) -> None:
        """Multiply every element by a scalar, then print the vector."""
        self.vector = [x * object for x in self.vector]
        print(self.vector)

    def __sub__(self, object: float) -> None:
        """Subtract a scalar from every element, then print the vector."""
        self.vector = [x - object for x in self.vector]
        print(self.vector)

    def __truediv__(self, object: float) -> None:
        """Divide every element by a scalar, then print the vector."""
        try:
            self.vector = [x / object for x in self.vector]
        except ZeroDivisionError:
            print("Error: division by zero")
            return
        print(self.vector)
```

Your own `tester.py`, including the division by zero:
```python
from ft_calculator import calculator


def main() -> None:
    """Run the subject's tests plus the division by zero."""
    v1 = calculator([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    v1 + 5
    print("---")
    v2 = calculator([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    v2 * 5
    print("---")
    v3 = calculator([10.0, 15.0, 20.0])
    v3 - 5
    v3 / 5
    print("---")
    v3 / 0


if __name__ == "__main__":
    main()
```
Last lines of output: `---` then `Error: division by zero`.
</details>

---

## 8. Exercise-Specific Knowledge

- **The class name is lowercase (`calculator`)**, as in the subject and the tester's import. Don't "fix" it to `Calculator`.
- **Each operator prints and updates.** `v3 - 5` followed by `v3 / 5` giving `[1.0, 2.0, 3.0]` is the proof.
- **Results stay floats** because the test vectors contain floats (`0.0`, `10.0`); `/` always returns a float in Python 3.
- **Only the division by 0 needs handling.** The subject says no other error handling is needed (no type checks, no empty list checks).
- **`ft_calculator.py` has no imports.** Everything is done with built-in features: classes, list comprehensions and `print`.
- **Same file name in ex04**, but a different content. Each folder has its own `ft_calculator.py`.
- **No `main()` needed in the module** (it is imported by the tester). If you write your own tests, keep them in a `tester.py` or inside `main()` guarded by `if __name__ == "__main__":`.
- **Be ready to explain** what `__add__` is, why `/` maps to `__truediv__`, and why the operators update `self.vector`.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Last line is `[2.0, 3.0, 4.0]` | Operators don't update `self.vector` | `self.vector = [...]` before printing |
| Nothing printed | The method returns the list instead of printing it | `print(self.vector)` |
| `ZeroDivisionError` traceback | Division by 0 not handled | `try/except ZeroDivisionError` |
| Vector changed after a failed division | Updated the list element by element before failing | Build the new list first, assign after success |
| Ints in the output (`5` instead of `5.0`) | Converted with `int()` or used `//` | Use `/`, keep floats |
| `TypeError: unsupported operand type(s) for /: 'calculator' and 'int'` | Method named `__div__` | Name it `__truediv__` |
| `AttributeError: 'calculator' object has no attribute 'vector'` | `__init__` doesn't store it | `self.vector = vector` |
| `TypeError: calculator() takes no arguments` | No `__init__` | Add the constructor |
| Output printed on import | Test code at module level | Keep tests in `tester.py` / `main()` |
| Missing docstring on an operator | Easy to forget | Document all five methods and the class |
| flake8 `E501` | Docstring line over 79 characters | Shorten the sentence |

---

## 10. Debugging Guide

- **Print the state:** after each operation, `print(v3.vector)` should equal what the subject shows next.
- **Wrong numbers after chaining:** the in-place update is missing; check the assignment `self.vector = ...` in the operator you used first.
- **`TypeError: unsupported operand type(s)`:** the operator method name is misspelled (`__mul__`, `__sub__`, `__add__`, `__truediv__`).
- **`None` appears:** you printed the return value of an operator (`print(v1 + 5)` prints the vector and then `None`). The tester doesn't do that; it only calls the operator.
- **Check division by zero:** `python -c "from ft_calculator import calculator; calculator([1.0]) / 0"` should print the error message without a traceback.
- **Check types:** `print(type(v1.vector[0]))` should be `<class 'float'>`.

---

## 11. Cheat Sheet

```python
class calculator:
    """Apply scalar operations (+, *, -, /) to a vector."""

    def __init__(self, vector: list[float]) -> None:
        """Store the vector."""
        self.vector = vector

    def __add__(self, object: float) -> None:
        """Add a scalar to every element, then print the vector."""
        self.vector = [x + object for x in self.vector]
        print(self.vector)

    # __mul__ and __sub__: same pattern with * and -

    def __truediv__(self, object: float) -> None:
        """Divide every element by a scalar, then print the vector."""
        try:
            self.vector = [x / object for x in self.vector]
        except ZeroDivisionError:
            print("Error: division by zero")
            return
        print(self.vector)
```

---

## 12. Knowledge Checklist

- [ ] The class is named `calculator` and takes the list in `__init__`.
- [ ] `+`, `*`, `-`, `/` are implemented with `__add__`, `__mul__`, `__sub__`, `__truediv__`.
- [ ] Each operator updates `self.vector` **and** prints the new vector, and the subject's output matches exactly (including `[1.0, 2.0, 3.0]` at the end).
- [ ] Division by zero prints a message instead of crashing, and leaves the vector unchanged.
- [ ] No imports, no `numpy`, no globals, nothing printed on import.
- [ ] The class and every method have a docstring, `flake8` is clean, final newline present.
- [ ] I can explain operator overloading, why `/` is `__truediv__`, and why the vector must be updated in place.
