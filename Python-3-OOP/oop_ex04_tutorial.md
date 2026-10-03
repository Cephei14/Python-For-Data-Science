# Study Tutorial — OOP Module, Exercise 04: ft_calculator.py (dot product)

## 1. Exercise Overview

**What it asks:**
Create a file `ft_calculator.py` in directory `ex04/` with a class `calculator` whose methods work on **two vectors** (lists of numbers) **without creating an object first**:
- `dotproduct(V1, V2)`: the dot product of the two vectors,
- `add_vec(V1, V2)`: the element-wise sum,
- `sous_vec(V1, V2)`: the element-wise difference.

The subject says: *"It's up to you to find a decorator that can help you to use the methods of the calculator class without instantiating this class."*

**The subject's prototype:**
```python
class calculator:
    #your code here

    # decorator
    def dotproduct(V1: list[float], V2: list[float]) -> None:
        #your code here

    # decorator
    def add_vec(V1: list[float], V2: list[float]) -> None:
        #your code here

    # decorator
    def sous_vec(V1: list[float], V2: list[float]) -> None:
        #your code here
```
Notice: there is **no `self`** in these methods.

**The subject's tester and expected output:**
```python
from ft_calculator import calculator

a = [5, 10, 2]
b = [2, 4, 3]
calculator.dotproduct(a, b)
calculator.add_vec(a, b)
calculator.sous_vec(a, b)
```
```
Dot product is: 56
Add Vector is : [7.0, 14.0, 5.0]
Sous Vector is: [3.0, 6.0, -1.0]
```

Details hidden in this output:
- The lists contain **integers** (`[5, 10, 2]`), yet the vectors printed by `add_vec` and `sous_vec` are **floats** (`7.0`, `-1.0`).
- The dot product is printed as **`56`** (an integer, not `56.0`).
- The three messages are written slightly differently: `Dot product is:`, `Add Vector is :` (space before the colon) and `Sous Vector is:`. Copy them exactly.
- The methods **print** their result and return `None` (`-> None`).

**Rules and Constraints:**
- File to turn in: `ft_calculator.py`. Allowed functions: **None** (no `numpy`, no imports needed; plain Python only).
- **No error handling needed:** vectors always have identical sizes.
- Docstrings on the class and every method, no globals, `flake8` clean, Python 3.10+.
- Uncaught exceptions invalidate the exercise.

**Main concepts you'll learn:**
- `@staticmethod`: methods that belong to a class but need no object.
- Calling methods directly on the class (`calculator.dotproduct(a, b)`).
- `zip` to pair up two lists, and `sum` with a generator expression.
- Static methods vs class methods vs instance methods.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **ex00 - ex03:** classes, methods, `self`, docstrings, `@classmethod` (ex01), list comprehensions (ex03).
- Lists, loops, `print`, f-strings.
- Type hints such as `list[float]`.

---

## 3. Tools and Libraries

| Tool / Syntax | What it does | Scope / Notes |
|---|---|---|
| `class calculator:` | Defines the class (lowercase, as in the subject) | Never instantiated in this exercise |
| `@staticmethod` | Decorator: the method needs neither `self` nor `cls` | The "decorator" the subject asks you to find |
| `def dotproduct(V1: list[float], V2: list[float]) -> None:` | A static method with two list parameters | No `self` as first parameter |
| `calculator.dotproduct(a, b)` | Calls the method on the **class** | No object created |
| `zip(V1, V2)` | Pairs up elements of two lists | `zip([5, 10], [2, 4])` gives `(5, 2), (10, 4)` |
| `for x, y in zip(V1, V2)` | Loops over the pairs, unpacking each | `x` from `V1`, `y` from `V2` |
| `sum(x * y for x, y in zip(V1, V2))` | Sum of products (the dot product) | Generator expression inside `sum` |
| `[float(x + y) for x, y in zip(V1, V2)]` | Element-wise addition, as floats | List comprehension |
| `[float(x - y) for x, y in zip(V1, V2)]` | Element-wise subtraction, as floats | |
| `float(7)` | Converts an int to a float (`7.0`) | Needed so the output shows `7.0` |
| `print(f"Dot product is: {result}")` | Prints a label and a value | Exact wording and spacing matter |
| `@classmethod` | Receives the class (`cls`) | For comparison only, not used here |

**Common pitfalls:**
- **Using `+` on the lists directly:** `[5, 10, 2] + [2, 4, 3]` **concatenates** into a 6-element list `[5, 10, 2, 2, 4, 3]`; it does not add element by element.
- **Forgetting `@staticmethod`:** calling `calculator.dotproduct(a, b)` happens to work in Python 3 (a plain function accessed through the class is just a function), but calling it on an instance would pass the instance as `V1` and fail. The decorator is also what the subject asks for.
- **Adding `self`** to the signature: with `@staticmethod` there is no `self`; `calculator.dotproduct(a, b)` would then miss an argument.
- **Printing `56.0` instead of `56`:** don't convert the dot product to float.
- **Printing `[7, 14, 5]` instead of `[7.0, 14.0, 5.0]`:** convert each element with `float(...)`.
- **Wrong message text:** `Add Vector is :` has a space before the colon; the other two don't.
- **Returning instead of printing:** the tester doesn't print anything; the methods must `print`.
- **Mixing up exercises:** ex03 stores a vector in an object; ex04 has **no `__init__` and no stored state**.

---

## 4. Concepts You Need to Learn

### 4.1 Three kinds of methods
| Kind | Decorator | First parameter | Needs | Typical use |
|---|---|---|---|---|
| Instance method | none | `self` | an object | Work with one object's data (ex00-ex03) |
| Class method | `@classmethod` | `cls` | the class | Factories, class-level data (ex01) |
| Static method | `@staticmethod` | nothing special | nothing | A utility function that logically belongs in the class |

A **static method** is just a normal function placed inside a class for organization. It can't see `self` or `cls`. Here, `dotproduct`, `add_vec` and `sous_vec` only need their two list arguments, so they are static.

### 4.2 Using `@staticmethod`
```python
class calculator:
    """Static helpers for operations between two vectors."""

    @staticmethod
    def dotproduct(V1: list[float], V2: list[float]) -> None:
        """Print the dot product of two vectors."""
        result = sum(x * y for x, y in zip(V1, V2))
        print(f"Dot product is: {result}")
```
- The decorator goes on the line right above `def`.
- There is no `self`: the first parameter is `V1`.
- You call it on the class, as the tester does: `calculator.dotproduct(a, b)`.

### 4.3 Pairing lists with `zip`
`zip` walks two lists in parallel:
```python
list(zip([5, 10, 2], [2, 4, 3]))    # [(5, 2), (10, 4), (2, 3)]
```
Vectors always have the same length here (no error handling needed), so no element is lost. `zip` stops at the shorter list when sizes differ.

### 4.4 The dot product
Multiply the elements that share a position, then add everything up:
```
[5, 10, 2] . [2, 4, 3] = 5*2 + 10*4 + 2*3 = 10 + 40 + 6 = 56
```
In code:
```python
result = sum(x * y for x, y in zip(V1, V2))
```
`x * y for x, y in zip(...)` is a generator expression (like a list comprehension without brackets) that feeds `sum`. With integer inputs, the result is an integer, which is why the expected output is `56`.

If the "Allowed functions: None" wording worries you, `zip` and `sum` are built-ins (and the day's rules allow built-ins unless forbidden). A plain loop is an equivalent alternative:
```python
result = 0
for i in range(len(V1)):
    result += V1[i] * V2[i]
```

### 4.5 Element-wise addition and subtraction
```python
[float(x + y) for x, y in zip(V1, V2)]    # [7.0, 14.0, 5.0]
[float(x - y) for x, y in zip(V1, V2)]    # [3.0, 6.0, -1.0]
```
`float(...)` turns each integer result into a float, matching `7.0`, `14.0`, `5.0` and `-1.0` in the expected output. If the input lists already hold floats, `float(...)` changes nothing.

### 4.6 Printing in the exact format
```python
print(f"Add Vector is : {result}")
```
`result` is a list; an f-string shows it like `print` would: `[7.0, 14.0, 5.0]`. The three label strings are:
- `Dot product is: ` + the number,
- `Add Vector is : ` + the list,
- `Sous Vector is: ` + the list.

### 4.7 Why a class at all?
The class acts as a **namespace**: `calculator.add_vec` groups related functions under one name. That is a legitimate use of static methods, and the one this exercise practices.

---

## 5. Syntax and Examples

### Step-by-step snippet
```python
class Tools:
    """A few helpers grouped in a class."""

    @staticmethod
    def double(x: float) -> float:
        """Return twice the given number."""
        return 2 * x

    @staticmethod
    def pairs(a: list[int], b: list[int]) -> list[tuple[int, int]]:
        """Return the elements of two lists paired by position."""
        return list(zip(a, b))


def main() -> None:
    """Call static methods directly on the class."""
    print(Tools.double(4))
    print(Tools.pairs([5, 10, 2], [2, 4, 3]))


if __name__ == "__main__":
    main()
```
Output:
```
8
[(5, 2), (10, 4), (2, 3)]
```
No `Tools()` object was ever created.

---

## 6. How to Think About the Exercise

1. **Step 1: Write the empty class** with a docstring.
2. **Step 2: Add `dotproduct`** as a static method; use `zip` and `sum`; print `Dot product is: 56`.
3. **Step 3: Add `add_vec`**: element-wise sum with `float(...)`; print `Add Vector is : [7.0, 14.0, 5.0]`.
4. **Step 4: Add `sous_vec`**: element-wise difference with `float(...)`; print `Sous Vector is: [3.0, 6.0, -1.0]`.
5. **Step 5: Run the subject's tester** and compare each character of the output, including the spacing before the colons.
6. **Step 6: Try other vectors** (floats, negative numbers) to make sure nothing is hard-coded.
7. **Step 7: Docstrings and `flake8`.**

---

## 7. Guided Practice

**Practice 1 (Easiest, static vs instance methods):**
Create `Tools` with an instance method `hello` and a static method `double(x)`. Call `double` on the class, call `hello` on an instance, and show that calling `Tools.hello()` on the class fails (catch the `TypeError`).

Expected output:
```
8
hello from an instance
TypeError caught
```

<details><summary>Solution</summary>

```python
class Tools:
    """A few helpers."""

    def hello(self) -> None:
        """Say hello (needs an instance)."""
        print("hello from an instance")

    @staticmethod
    def double(x: float) -> float:
        """Return twice the given number (needs no instance)."""
        return 2 * x


def main() -> None:
    """Compare instance and static methods."""
    print(Tools.double(4))
    Tools().hello()
    try:
        Tools.hello()
    except TypeError:
        print("TypeError caught")


if __name__ == "__main__":
    main()
```
</details>

**Practice 2 (Pair two lists with `zip`):**
Print the list of pairs of `[5, 10, 2]` and `[2, 4, 3]`.

Expected output:
```
[(5, 2), (10, 4), (2, 3)]
```

<details><summary>Solution</summary>

```python
def main() -> None:
    """Pair two lists by position."""
    a = [5, 10, 2]
    b = [2, 4, 3]
    print(list(zip(a, b)))


if __name__ == "__main__":
    main()
```
</details>

**Practice 3 (Dot product, and the `+` trap):**
With `a = [5, 10, 2]` and `b = [2, 4, 3]`, print `a + b` (to see the concatenation trap), then the dot product.

Expected output:
```
[5, 10, 2, 2, 4, 3]
56
```

<details><summary>Solution</summary>

```python
def main() -> None:
    """Show that + concatenates lists, then compute a dot product."""
    a = [5, 10, 2]
    b = [2, 4, 3]
    print(a + b)
    print(sum(x * y for x, y in zip(a, b)))


if __name__ == "__main__":
    main()
```
</details>

**Practice 4 (Element-wise sum and difference as floats):**
Print the element-wise sum and difference of `[5, 10, 2]` and `[2, 4, 3]` with float elements.

Expected output:
```
[7.0, 14.0, 5.0]
[3.0, 6.0, -1.0]
```

<details><summary>Solution</summary>

```python
def main() -> None:
    """Compute element-wise operations on two lists."""
    a = [5, 10, 2]
    b = [2, 4, 3]
    print([float(x + y) for x, y in zip(a, b)])
    print([float(x - y) for x, y in zip(a, b)])


if __name__ == "__main__":
    main()
```
</details>

**Practice 5 (Class method vs static method):**
Create `Counter` with a class attribute `count = 0`, a `@classmethod` `increment` that adds 1 to `cls.count`, and a `@staticmethod` `double(x)`. Call `increment` twice, then print `Counter.count` and `Counter.double(5)`.

Expected output:
```
2
10
```

<details><summary>Solution</summary>

```python
class Counter:
    """Show the difference between class and static methods."""

    count = 0

    @classmethod
    def increment(cls) -> None:
        """Add 1 to the class-level counter."""
        cls.count += 1

    @staticmethod
    def double(x: float) -> float:
        """Return twice the given number (no class data needed)."""
        return 2 * x


def main() -> None:
    """Use both kinds of methods."""
    Counter.increment()
    Counter.increment()
    print(Counter.count)
    print(Counter.double(5))


if __name__ == "__main__":
    main()
```

`increment` needs the class (it changes `cls.count`), so it is a class method. `double` needs nothing, so it is static.
</details>

**Practice 6 (Hardest, the full rule-compliant `ft_calculator.py`):**

Expected output with the subject's tester: see section 1.

<details><summary>Solution</summary>

```python
class calculator:
    """Operations between two vectors, usable without an instance."""

    @staticmethod
    def dotproduct(V1: list[float], V2: list[float]) -> None:
        """Print the dot product of two vectors."""
        result = sum(x * y for x, y in zip(V1, V2))
        print(f"Dot product is: {result}")

    @staticmethod
    def add_vec(V1: list[float], V2: list[float]) -> None:
        """Print the element-wise sum of two vectors."""
        result = [float(x + y) for x, y in zip(V1, V2)]
        print(f"Add Vector is : {result}")

    @staticmethod
    def sous_vec(V1: list[float], V2: list[float]) -> None:
        """Print the element-wise difference of two vectors."""
        result = [float(x - y) for x, y in zip(V1, V2)]
        print(f"Sous Vector is: {result}")
```
</details>

---

## 8. Exercise-Specific Knowledge

- **The "decorator" is `@staticmethod`.** It lets you write `calculator.dotproduct(a, b)` with no `calculator()` object, and no `self`.
- **No `__init__`, no stored data.** Everything the methods need arrives through their two parameters.
- **Output format is part of the grade:** `Dot product is: 56`, `Add Vector is : [7.0, 14.0, 5.0]`, `Sous Vector is: [3.0, 6.0, -1.0]`.
- **Types matter:** the dot product of integer lists stays an integer (`56`), but `add_vec` and `sous_vec` print floats.
- **"Sous" is French** for "under/minus": the method name `sous_vec` must be spelled exactly like that.
- **Same file name as ex03, different folder and content.** Don't copy the ex03 `ft_calculator.py` into `ex04/`.
- **No error handling required:** the subject guarantees equal sizes. (`zip` would silently cut the longer list otherwise.)
- **Parameter names `V1`, `V2` are uppercase** in the prototype; `flake8` accepts them, so keep the subject's names.
- **Be ready to explain** in the defence what `@staticmethod` does, how it differs from `@classmethod` and from a normal method, and what `zip` does.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `[5, 10, 2, 2, 4, 3]` from `add_vec` | Used `V1 + V2` | Pair with `zip` and add element by element |
| Output `[7, 14, 5]` | No `float(...)` | `float(x + y)` |
| Output `56.0` | Converted the dot product to float | Leave `sum(...)` as is |
| `TypeError: dotproduct() takes 2 positional arguments but 3 were given` | Called on an instance of a method without `@staticmethod` | Add the decorator |
| `TypeError: dotproduct() missing 1 required positional argument` | Added `self` to a static method | Remove `self` |
| Nothing printed | Method returns the value | Use `print(f"...")` |
| `Add Vector is: ...` (no space) | Typo | `Add Vector is : ` |
| `NameError: name 'calculator' is not defined` | Wrong class name or file name | Class `calculator` in `ft_calculator.py` |
| Used the ex03 file | Folders mixed up | Write the ex04 version in `ex04/` |
| Missing docstring | Forgot on one method or on the class | Document everything |
| flake8 `E501` | Docstring or f-string line too long | Shorten or wrap |

---

## 10. Debugging Guide

- **Compare output character by character:** copy the three expected lines into a file and `diff` them with your output (`python tester.py | diff - expected.txt`).
- **Check the types:** `print(type(result))` inside a method; the dot product should be `int` for integer inputs, the vectors should be `list` of `float`.
- **`TypeError` on call:** read it carefully: "missing" means you have one parameter too many (probably `self`), "were given" means one too few.
- **Test with floats and negatives:** `calculator.dotproduct([1.5, -2.0], [2.0, 4.0])` should print `Dot product is: -5.0`.
- **Static method check:** `type(calculator.__dict__["dotproduct"])` should be `<class 'staticmethod'>`.
- **Exact spacing:** print `repr` of a message if you suspect hidden spaces: `print(repr("Add Vector is : "))`.

---

## 11. Cheat Sheet

```python
class calculator:
    """Operations between two vectors, usable without an instance."""

    @staticmethod
    def dotproduct(V1: list[float], V2: list[float]) -> None:
        """Print the dot product of two vectors."""
        result = sum(x * y for x, y in zip(V1, V2))
        print(f"Dot product is: {result}")

    @staticmethod
    def add_vec(V1: list[float], V2: list[float]) -> None:
        """Print the element-wise sum of two vectors."""
        result = [float(x + y) for x, y in zip(V1, V2)]
        print(f"Add Vector is : {result}")

    @staticmethod
    def sous_vec(V1: list[float], V2: list[float]) -> None:
        """Print the element-wise difference of two vectors."""
        result = [float(x - y) for x, y in zip(V1, V2)]
        print(f"Sous Vector is: {result}")
```

---

## 12. Knowledge Checklist

- [ ] `ex04/ft_calculator.py` defines `calculator` with `dotproduct`, `add_vec` and `sous_vec`, all decorated with `@staticmethod` and without `self`.
- [ ] `calculator.dotproduct(a, b)` etc. work without creating an object.
- [ ] The output is exactly `Dot product is: 56`, `Add Vector is : [7.0, 14.0, 5.0]`, `Sous Vector is: [3.0, 6.0, -1.0]`.
- [ ] The vectors are added and subtracted element by element, never with `+` or `-` on the lists.
- [ ] No imports, no `numpy`, no globals, nothing printed on import.
- [ ] The class and each method have a docstring, `flake8` is clean, final newline present.
- [ ] I can explain `@staticmethod` vs `@classmethod` vs instance methods, and what `zip` does.
