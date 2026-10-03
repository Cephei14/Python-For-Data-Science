# Study Tutorial — OOP Module, Exercise 00: S1E9.py

## 1. Exercise Overview

**What it asks:**
Create a file `S1E9.py` in directory `ex00/` containing:
1. An **abstract class** `Character` that:
   - takes `first_name` as first (mandatory) parameter,
   - takes `is_alive` as second, **optional** parameter, `True` by default,
   - has a method that changes the health state: `is_alive` goes from `True` to `False`.
2. A class `Stark` that **inherits** from `Character`.

**The subject's tester and expected output:**
```python
from S1E9 import Character, Stark

Ned = Stark("Ned")
print(Ned.__dict__)          # {'first_name': 'Ned', 'is_alive': True}
print(Ned.is_alive)          # True
Ned.die()
print(Ned.is_alive)          # False
print(Ned.__doc__)           # docstring of the class
print(Ned.__init__.__doc__)  # docstring of the constructor
print(Ned.die.__doc__)       # docstring of the method
print("---")
Lyanna = Stark("Lyanna", False)
print(Lyanna.__dict__)       # {'first_name': 'Lyanna', 'is_alive': False}
```
And this must **fail**, because `Character` is abstract:
```python
from S1E9 import Character
hodor = Character("hodor")   # TypeError: Can't instantiate abstract class Character ...
```

**Rules and Constraints:**
- File to turn in: `S1E9.py`. Allowed functions: **None** (only `abc` from the standard library, which the prototype itself imports).
- No code in the global scope except imports and class/function definitions; no global variables.
- **Every** function, class and method needs a docstring (`__doc__`), including `__init__`.
- `flake8` clean, explicit imports, Python 3.10+.
- Any uncaught exception invalidates the exercise.

**Main concepts you'll learn:**
- Classes, instances, `__init__` and `self`.
- Instance attributes and `obj.__dict__`.
- Default parameter values.
- Inheritance (`class Stark(Character)`).
- Abstract classes with `ABC` and `@abstractmethod`.
- Docstrings as real data (`__doc__`).

---

## 2. Prerequisites (What You Know From Earlier Modules)

- Functions, parameters, default parameter values, `return`.
- `print`, f-strings, `try/except`.
- Dictionaries (`__dict__` is one).
- `if __name__ == "__main__":` and `main()`.

Everything about classes (`class`, `self`, `__init__`, inheritance, `ABC`) is explained in section 4.

---

## 3. Tools and Libraries

| Tool / Syntax | What it does | Scope / Notes |
|---|---|---|
| `from abc import ABC, abstractmethod` | Imports the tools for abstract classes | Explicit import (no `import *`) |
| `class Character(ABC):` | Defines a class that **cannot be instantiated directly** | `ABC` = "Abstract Base Class" |
| `class Stark(Character):` | Defines a class that **inherits** everything from `Character` | `Character` is the parent / base class |
| `def __init__(self, first_name, is_alive=True):` | Constructor: runs when an object is created | `self` is the new object; `is_alive=True` is a default value |
| `self.first_name = first_name` | Creates an **instance attribute** | Stored in the object's `__dict__` |
| `@abstractmethod` | Marks a method that **subclasses must implement** | Decorator placed on the line right above `def` |
| `def die(self) -> None:` | A method that changes the object's state | `-> None` means "returns nothing" |
| `Stark("Ned")` | Creates an instance (calls `__init__`) | Positional argument goes to `first_name` |
| `Stark("Lyanna", False)` | Creates an instance with `is_alive=False` | Second positional argument overrides the default |
| `obj.__dict__` | Dictionary of an object's instance attributes | Keys are in the order they were assigned |
| `obj.__doc__` | The docstring of the object's class | Class docstrings are **not** inherited |
| `Ned.__init__.__doc__` | Docstring of the constructor | Inherited from `Character` if `Stark` doesn't define `__init__` |
| `Ned.die.__doc__` | Docstring of the method | Comes from the class where `die` is defined |
| `isinstance(obj, Character)` | Checks if an object is an instance of a class (or subclass) | `True` for a `Stark` object |
| `try: ... except TypeError:` | Catches the error raised when instantiating an abstract class | Needed in your own tests so nothing crashes |

**Common pitfalls:**
- **Forgetting `self`** as the first parameter of every method (`TypeError: ... takes 1 positional argument but 2 were given`).
- **Forgetting `self.`** when storing: `first_name = first_name` creates a local variable that disappears; use `self.first_name = first_name`.
- **No abstract method:** a class inheriting `ABC` but with no `@abstractmethod` can still be instantiated, so `Character("hodor")` would **not** fail.
- **`Stark` doesn't implement the abstract method:** then `Stark("Ned")` also fails with `TypeError`. `Stark` must define `die`.
- **Missing docstrings** on `__init__` or on a method: `print(Ned.__init__.__doc__)` prints `None` and the norm is violated.
- **Wrong attribute order:** the expected `__dict__` is `first_name` then `is_alive`; assign them in that order.
- **Mutable default argument habit:** here the default is a boolean (safe), but never write `def f(x=[])`.
- **Instantiating inside the global scope** of `S1E9.py`: importing the module must print nothing.

---

## 4. Concepts You Need to Learn

### 4.1 A class and its instances
A **class** is a blueprint; an **instance** (or object) is one thing built from it.
```python
class Person:
    """A very small class."""

    def __init__(self, name: str) -> None:
        """Store the name."""
        self.name = name


p = Person("Ned")      # creates an instance, calls __init__("Ned") for you
print(p.name)          # Ned
```
- `__init__` is the **constructor**. You never call it yourself; `Person("Ned")` does.
- `self` is the object being built. Python passes it automatically as the first argument, so you write `Person("Ned")` but define `__init__(self, name)`.
- `self.name = name` attaches data to **that** object.

### 4.2 Instance attributes and `__dict__`
Every object keeps its attributes in a dictionary:
```python
print(p.__dict__)      # {'name': 'Ned'}
```
The tester prints `__dict__`, so the **names** (`first_name`, `is_alive`) and the **order** (assignment order) are part of the expected output.

### 4.3 Default parameter values
```python
def __init__(self, first_name: str, is_alive: bool = True) -> None:
```
- `first_name` has no default: it is **mandatory**.
- `is_alive=True` is **optional**: `Stark("Ned")` gives `True`, `Stark("Lyanna", False)` gives `False`.
- Parameters with defaults must come **after** the mandatory ones.
- `: str`, `: bool` and `-> None` are **type hints**. They document intent; Python doesn't enforce them.

### 4.4 A method that changes the state
```python
def die(self) -> None:
    """Pass is_alive from True to False."""
    self.is_alive = False
```
A method is a function defined inside a class. It receives `self`, so it can read and modify the object's attributes. It returns nothing; it just changes the state.

### 4.5 Inheritance
```python
class Stark(Character):
    """Representing the Stark family."""
```
`Stark` automatically **has** everything `Character` defines: `__init__`, `first_name`, `is_alive`. That's why `Stark("Ned")` works even though `Stark` doesn't define `__init__`. A child class can add or **override** (replace) methods.

### 4.6 Abstract classes (`ABC` and `@abstractmethod`)
An abstract class is a **template that cannot be used directly**; it exists only to be inherited.
```python
from abc import ABC, abstractmethod


class Character(ABC):
    ...
    @abstractmethod
    def die(self) -> None:
        """Change the health state (each family must implement it)."""
```
Rules:
- To be abstract, the class must inherit `ABC` **and** have at least one `@abstractmethod`.
- Trying `Character("hodor")` raises `TypeError` right away.
- A subclass becomes instantiable only when it **implements every abstract method**. That's why `Stark` defines `die`.
- The abstract method's body can be just a docstring (a docstring alone is a valid body).

The error message depends on your Python version:
- Python 3.10 / 3.11: `Can't instantiate abstract class Character with abstract method die`
- Python 3.12+: `Can't instantiate abstract class Character without an implementation for abstract method 'die'`

Both are correct; the subject's picture shows the older wording.

### 4.7 Docstrings are data
A docstring is the first string inside a class or function. Python stores it in `__doc__`:
- `Ned.__doc__` is `Stark`'s docstring. **Class docstrings are not inherited**: if `Stark` had none, it would print `None`, even though `Character` has one.
- `Ned.__init__.__doc__` is the docstring of whichever `__init__` runs. `Stark` has none of its own, so it's the one from `Character`, which therefore **must** have a docstring.
- `Ned.die.__doc__` is the docstring of `Stark.die`.

### 4.8 Testing the failing case safely
The subject says `Character("hodor")` must fail, but **an uncaught exception invalidates the exercise**. In your own test, catch it:
```python
try:
    Character("hodor")
except TypeError as e:
    print(f"TypeError: {e}")
```

---

## 5. Syntax and Examples

### Step-by-step snippet
```python
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract shape."""

    @abstractmethod
    def area(self) -> float:
        """Return the area (each shape must implement it)."""


class Square(Shape):
    """A square."""

    def __init__(self, side: float) -> None:
        """Store the side."""
        self.side = side

    def area(self) -> float:
        """Return the area of the square."""
        return self.side ** 2


def main() -> None:
    """Show that Shape is abstract and Square is not."""
    try:
        Shape()
    except TypeError:
        print("Shape cannot be instantiated")
    print(Square(3).area())


if __name__ == "__main__":
    main()
```
Output:
```
Shape cannot be instantiated
9
```

---

## 6. How to Think About the Exercise

1. **Step 1: Import** `ABC` and `abstractmethod` from `abc`.
2. **Step 2: Write `Character(ABC)`** with a docstring.
3. **Step 3: Add `__init__(self, first_name, is_alive=True)`** with a docstring; assign `first_name` first, then `is_alive`.
4. **Step 4: Add an abstract method** `die` (decorated with `@abstractmethod`) with a docstring.
5. **Step 5: Write `Stark(Character)`** with a class docstring and a concrete `die` (with its own docstring) that sets `self.is_alive = False`.
6. **Step 6: Test** with the subject's tester, then test that `Character("hodor")` raises `TypeError` (inside `try/except`).
7. **Step 7: Run `flake8`.**

---

## 7. Guided Practice

**Practice 1 (Easiest, a class with a constructor):**
Create `Person` with a `name` attribute; print the name and the `__dict__`.

Expected output:
```
Ned
{'name': 'Ned'}
```

<details><summary>Solution</summary>

```python
class Person:
    """A very small class."""

    def __init__(self, name: str) -> None:
        """Store the name."""
        self.name = name


def main() -> None:
    """Create one object and look at its attributes."""
    p = Person("Ned")
    print(p.name)
    print(p.__dict__)


if __name__ == "__main__":
    main()
```
</details>

**Practice 2 (Default value and a method that changes the state):**
Add an optional `is_alive` (default `True`) and a method `die`. Print the state before and after `die`, then create `Lyanna` with `is_alive=False` and print her `__dict__`.

Expected output:
```
True
False
{'name': 'Lyanna', 'is_alive': False}
```

<details><summary>Solution</summary>

```python
class Person:
    """A person who can die."""

    def __init__(self, name: str, is_alive: bool = True) -> None:
        """Store the name and the health state."""
        self.name = name
        self.is_alive = is_alive

    def die(self) -> None:
        """Pass is_alive from True to False."""
        self.is_alive = False


def main() -> None:
    """Test the default value and the method."""
    ned = Person("Ned")
    print(ned.is_alive)
    ned.die()
    print(ned.is_alive)
    lyanna = Person("Lyanna", False)
    print(lyanna.__dict__)


if __name__ == "__main__":
    main()
```
</details>

**Practice 3 (Inheritance):**
Create `Animal` (with `name` and `speak`) and `Dog(Animal)` that defines nothing new. Create a `Dog`, call `speak`, print its `__dict__` and `isinstance(d, Animal)`.

Expected output:
```
Rex makes a sound
{'name': 'Rex'}
True
```

<details><summary>Solution</summary>

```python
class Animal:
    """A generic animal."""

    def __init__(self, name: str) -> None:
        """Store the name."""
        self.name = name

    def speak(self) -> None:
        """Print a generic sound."""
        print(f"{self.name} makes a sound")


class Dog(Animal):
    """A dog: it inherits everything from Animal."""


def main() -> None:
    """Show that Dog inherits the constructor and the method."""
    d = Dog("Rex")
    d.speak()
    print(d.__dict__)
    print(isinstance(d, Animal))


if __name__ == "__main__":
    main()
```
</details>

**Practice 4 (Docstrings and inheritance):**
Create a class `A` with a class docstring `"Base class doc"` and a method `m` with docstring `"Method doc"`. Create `B(A)` with **no** docstring. Print `A.__doc__`, `B.__doc__`, `B().m.__doc__`.

Expected output:
```
Base class doc
None
Method doc
```

<details><summary>Solution</summary>

```python
class A:
    """Base class doc"""

    def m(self) -> None:
        """Method doc"""


class B(A):
    pass


def main() -> None:
    """Show which docstrings are inherited."""
    print(A.__doc__)
    print(B.__doc__)
    print(B().m.__doc__)


if __name__ == "__main__":
    main()
```

(Class `B` has no docstring here on purpose, to show the behavior. In your exercise, `Stark` **must** have one.)
</details>

**Practice 5 (An abstract class):**
Create the abstract `Shape` with an abstract `area`, and `Square(Shape)` implementing it. Show that `Shape()` raises `TypeError` (catch it) and print the area of `Square(3)`.

Expected output:
```
TypeError caught
9
```

<details><summary>Solution</summary>

```python
from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract shape."""

    @abstractmethod
    def area(self) -> float:
        """Return the area (each shape must implement it)."""


class Square(Shape):
    """A square."""

    def __init__(self, side: float) -> None:
        """Store the side."""
        self.side = side

    def area(self) -> float:
        """Return the area of the square."""
        return self.side * self.side


def main() -> None:
    """Show that Shape is abstract and Square is not."""
    try:
        Shape()
    except TypeError:
        print("TypeError caught")
    print(Square(3).area())


if __name__ == "__main__":
    main()
```
</details>

**Practice 6 (Hardest, the full rule-compliant `S1E9.py`):**

Expected output when running the subject's `tester.py` (docstrings can differ):
```
{'first_name': 'Ned', 'is_alive': True}
True
False
Representing the Stark family.
Initialize a character with a first name and a health state.
Pass is_alive from True to False.
---
{'first_name': 'Lyanna', 'is_alive': False}
```

<details><summary>Solution</summary>

```python
from abc import ABC, abstractmethod


class Character(ABC):
    """Abstract base class for a character."""

    def __init__(self, first_name: str, is_alive: bool = True) -> None:
        """Initialize a character with a first name and a health state."""
        self.first_name = first_name
        self.is_alive = is_alive

    @abstractmethod
    def die(self) -> None:
        """Change the health state of the character (to implement)."""


class Stark(Character):
    """Representing the Stark family."""

    def die(self) -> None:
        """Pass is_alive from True to False."""
        self.is_alive = False
```

Your own `tester.py` (the failing case is caught, so nothing crashes):
```python
from S1E9 import Character, Stark


def main() -> None:
    """Run the subject's tests."""
    ned = Stark("Ned")
    print(ned.__dict__)
    print(ned.is_alive)
    ned.die()
    print(ned.is_alive)
    print(ned.__doc__)
    print(ned.__init__.__doc__)
    print(ned.die.__doc__)
    print("---")
    lyanna = Stark("Lyanna", False)
    print(lyanna.__dict__)
    try:
        Character("hodor")
    except TypeError as e:
        print(f"TypeError: {e}")


if __name__ == "__main__":
    main()
```
</details>

---

## 8. Exercise-Specific Knowledge

- **`die` must be the abstract method.** The subject's error message mentions "abstract method", and `Stark` must be instantiable, so the method that changes the health state is the one that is abstract in `Character` and concrete in `Stark`.
- **Attribute order:** `first_name` is assigned before `is_alive`, matching `{'first_name': 'Ned', 'is_alive': True}`.
- **`Stark` needs its own class docstring**, because `Ned.__doc__` prints it. `Stark` doesn't need its own `__init__`; it inherits the one from `Character` (and its docstring).
- **Only imports and definitions at module level.** Importing `S1E9` must print nothing.
- **A `main()` is not needed in `S1E9.py`**, because it is a module imported by the tester. If you add self-tests, put them in `main()` under `if __name__ == "__main__":` so importing stays silent.
- **Python version:** the `TypeError` text differs between 3.10/3.11 and 3.12+; both are valid.
- **Later exercises build on this file**, so keep it exactly as the tester expects: `S1E9.py` is copied into `ex01/` and `ex02/`.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `Character("hodor")` does not fail | No `@abstractmethod`, or `Character` doesn't inherit `ABC` | `class Character(ABC)` and decorate one method |
| `TypeError` when creating `Stark("Ned")` | `Stark` doesn't implement `die` | Define `die` in `Stark` |
| `TypeError: die() takes 0 positional arguments but 1 was given` | Forgot `self` | `def die(self):` |
| Attributes missing in `__dict__` | Wrote `first_name = first_name` without `self.` | `self.first_name = first_name` |
| `__dict__` shows `is_alive` first | Assigned in the wrong order | Assign `first_name` then `is_alive` |
| `Ned.__doc__` prints `None` | `Stark` has no class docstring (not inherited) | Add a docstring to `Stark` |
| `Ned.__init__.__doc__` prints `None` | `Character.__init__` has no docstring | Add one |
| Lyanna is alive | Default used instead of the second argument | Pass `False` as 2nd argument; check the parameter order |
| Output appears on import | Test code in the global scope | Move it to `main()` |
| flake8 `E302`/`E305` | Missing 2 blank lines around classes | Two blank lines between classes |
| flake8 `W292` | No newline at end of file | Add a blank line at the end |

---

## 10. Debugging Guide

- **`TypeError: Can't instantiate abstract class Stark ...`:** list the abstract methods it names; `Stark` hasn't implemented all of them (check the spelling of `die`).
- **`TypeError: __init__() takes from 2 to 3 positional arguments but 4 were given`:** you passed too many arguments; the signature is `(self, first_name, is_alive=True)`.
- **`AttributeError: 'Stark' object has no attribute 'is_alive'`:** `__init__` never ran or never assigned it; print `obj.__dict__`.
- **Wrong docstring text printed:** remember which class owns each docstring: `__doc__` is `Stark`'s, `__init__.__doc__` is `Character`'s, `die.__doc__` is `Stark`'s.
- **Check the inheritance chain:** `print(Stark.__mro__)` shows `Stark`, `Character`, `ABC`, `object`.
- **Check what is abstract:** `print(Character.__abstractmethods__)` shows `frozenset({'die'})`.

---

## 11. Cheat Sheet

```python
from abc import ABC, abstractmethod


class Character(ABC):
    """Abstract base class for a character."""

    def __init__(self, first_name: str, is_alive: bool = True) -> None:
        """Initialize a character with a first name and a health state."""
        self.first_name = first_name
        self.is_alive = is_alive

    @abstractmethod
    def die(self) -> None:
        """Change the health state of the character (to implement)."""


class Stark(Character):
    """Representing the Stark family."""

    def die(self) -> None:
        """Pass is_alive from True to False."""
        self.is_alive = False
```

---

## 12. Knowledge Checklist

- [ ] `Character` inherits `ABC` and has an `@abstractmethod`, so `Character("hodor")` raises `TypeError`.
- [ ] `Stark` inherits `Character` and implements `die`, so `Stark("Ned")` works.
- [ ] `first_name` is mandatory, `is_alive` defaults to `True`, and `__dict__` matches the expected output.
- [ ] `die()` turns `is_alive` from `True` to `False`.
- [ ] The class, `__init__` and `die` all have docstrings, and the three `__doc__` prints are not `None`.
- [ ] My own test catches the `TypeError` instead of crashing.
- [ ] I can explain: class vs instance, `self`, `__init__`, inheritance, what makes a class abstract.
- [ ] No globals, nothing printed on import, `flake8` clean, final newline present.
