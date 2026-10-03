# Study Tutorial — OOP Module, Exercise 01: S1E7.py

## 1. Exercise Overview

**What it asks:**
Create a file `S1E7.py` in directory `ex01/` (next to `S1E9.py` from ex00) containing two families that inherit from `Character`:
1. `Baratheon(Character)` and `Lannister(Character)`.
2. Both must be **instantiable directly** (without going through `Character`), so each must implement the abstract method.
3. Each family sets its own traits:

| Family | `family_name` | `eyes` | `hairs` |
|---|---|---|---|
| Baratheon | `'Baratheon'` | `'brown'` | `'dark'` |
| Lannister | `'Lannister'` | `'blue'` | `'light'` |

4. `__str__` and `__repr__` must **return strings** (not tuples or other objects).
5. A **class method** `create_lannister` creates characters "in a chain" (a factory).

**The subject's tester and expected output:**
```python
from S1E7 import Baratheon, Lannister

Robert = Baratheon("Robert")
print(Robert.__dict__)
print(Robert.__str__)
print(Robert.__repr__)
print(Robert.is_alive)
Robert.die()
print(Robert.is_alive)
print(Robert.__doc__)
print("---")
Cersei = Lannister("Cersei")
print(Cersei.__dict__)
print(Cersei.__str__)
print(Cersei.is_alive)
print("---")
Jaine = Lannister.create_lannister("Jaine", True)
print(f"Name : {Jaine.first_name, type(Jaine).__name__}, Alive : {Jaine.is_alive}")
```
```
{'first_name': 'Robert', 'is_alive': True, 'family_name': 'Baratheon', 'eyes': 'brown', 'hairs': 'dark'}
<bound method Baratheon.__str__ of Vector: ('Baratheon', 'brown', 'dark')>
<bound method Baratheon.__repr__ of Vector: ('Baratheon', 'brown', 'dark')>
True
False
Representing the Baratheon family.
---
{'first_name': 'Cersei', 'is_alive': True, 'family_name': 'Lannister', 'eyes': 'blue', 'hairs': 'light'}
<bound method Lannister.__str__ of Vector: ('Lannister', 'blue', 'light')>
True
---
Name : ('Jaine', 'Lannister'), Alive : True
```

**Rules and Constraints:**
- Files to turn in: **files from previous exercises + `S1E7.py`** (so `ex01/` contains `S1E9.py` and `S1E7.py`). Allowed functions: **None**.
- Docstrings on every class, method and function (including `__init__`, `__str__`, `__repr__`).
- No globals, `flake8` clean, explicit imports, Python 3.10+.
- Uncaught exceptions invalidate the exercise.

**Main concepts you'll learn:**
- Calling the parent constructor with `super().__init__(...)`.
- Implementing an inherited abstract method in two sibling classes.
- `__str__` vs `__repr__`, and why they must return strings.
- Class methods (`@classmethod`, `cls`) used as factories.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **ex00:** classes, `__init__`, `self`, instance attributes, `__dict__`, inheritance, `ABC` / `@abstractmethod`, docstrings as `__doc__`.
- f-strings, tuples, list comprehensions.
- The way you test: a `tester.py` file next to your module.

---

## 3. Tools and Libraries

| Tool / Syntax | What it does | Scope / Notes |
|---|---|---|
| `from S1E9 import Character` | Imports the parent class from your ex00 file | The file `S1E9.py` must be in the same folder |
| `class Baratheon(Character):` | A family that inherits from `Character` | Gets `first_name`, `is_alive` for free |
| `super().__init__(first_name, is_alive)` | Calls the **parent's** constructor | Do it **first**, so the parent attributes come first in `__dict__` |
| `self.family_name = "Baratheon"` | Adds an attribute specific to the family | Assigned after `super().__init__` |
| `def die(self) -> None:` | Implements the abstract method | Without it the family stays abstract and can't be instantiated |
| `def __str__(self) -> str:` | Text for `print(obj)` / `str(obj)` | **Must return a `str`** |
| `def __repr__(self) -> str:` | Unambiguous text for `repr(obj)`, the REPL, lists, and bound-method display | **Must return a `str`** |
| `f"Vector: {(a, b, c)}"` | An f-string that formats a tuple | The tuple prints as `('a', 'b', 'c')` |
| `@classmethod` | Decorator: the method receives the **class** instead of an instance | First parameter is named `cls` |
| `cls(first_name, is_alive)` | Creates an instance of the class the method was called on | Works for subclasses too |
| `Lannister.create_lannister("Jaine", True)` | Calls the class method on the class | No instance needed |
| `type(obj).__name__` | The name of an object's class, as a string | Used in the subject's last print |
| `obj.__str__` (no parentheses) | The **bound method object**, not its result | Its display includes `repr(obj)` |
| `[Lannister.create_lannister(n) for n in names]` | Creates several characters in a chain | List comprehension |

**Common pitfalls:**
- **`__str__` or `__repr__` returning a tuple:** `print(obj)` then fails with `TypeError: __str__ returned non-string (type tuple)`. Always return a `str`.
- **Printing `obj.__str__` expecting text:** without `()` you get the bound method. The expected output shows exactly that (`<bound method Baratheon.__str__ of Vector: ...>`).
- **Forgetting `super().__init__(...)`:** `first_name` and `is_alive` never get assigned.
- **Setting the family attributes before `super().__init__`:** the `__dict__` order becomes wrong (family attributes first).
- **Forgetting `die` in a family:** `Baratheon("Robert")` fails with `TypeError: Can't instantiate abstract class`.
- **Class method written like a normal method:** forgetting `@classmethod` means `Lannister.create_lannister("Jaine")` gets `"Jaine"` as `self` and fails.
- **Hard-coding `Lannister(...)` inside the class method** instead of `cls(...)`: works, but a subclass would get a `Lannister` instead of itself.
- **Missing docstrings** on `__str__`, `__repr__`, `__init__`, or the class method.

---

## 4. Concepts You Need to Learn

### 4.1 Calling the parent constructor with `super()`
The parent already knows how to store `first_name` and `is_alive`. Don't copy that code, **delegate** to it:
```python
class Baratheon(Character):
    """Representing the Baratheon family."""

    def __init__(self, first_name: str, is_alive: bool = True) -> None:
        """Initialize a Baratheon with the family traits."""
        super().__init__(first_name, is_alive)   # parent attributes first
        self.family_name = "Baratheon"
        self.eyes = "brown"
        self.hairs = "dark"
```
- `super()` gives access to the parent class.
- After this, `__dict__` is `{'first_name': ..., 'is_alive': ..., 'family_name': ..., 'eyes': ..., 'hairs': ...}`, the exact order of the expected output.
- The subclass `__init__` keeps the same signature `(first_name, is_alive=True)` so `Baratheon("Robert")` works.

### 4.2 Making each family instantiable
`Character.die` is abstract, so each family has to implement it:
```python
def die(self) -> None:
    """Pass is_alive from True to False."""
    self.is_alive = False
```
This subject says "that we can instantiate **without going through the Character class**": the families are complete classes, not abstract ones.

### 4.3 `__str__` vs `__repr__`
Python has two ways to turn an object into text:

| Method | Called by | Meant for |
|---|---|---|
| `__str__` | `print(obj)`, `str(obj)` | Readable text for users |
| `__repr__` | `repr(obj)`, the REPL, objects **inside lists**, debugging | Unambiguous text for developers |

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"
```
`print(Point(1, 2))` shows `(1, 2)`; `print([Point(1, 2)])` shows `[Point(1, 2)]`.

**Both must return a `str`.** The subject's sentence "return strings and not objects" refers to this: if you return a tuple (like `(self.family_name, self.eyes, self.hairs)`), Python raises `TypeError: __str__ returned non-string (type tuple)`. Format it into a string instead:
```python
def __str__(self) -> str:
    """Return the family traits as text."""
    return f"Vector: {(self.family_name, self.eyes, self.hairs)}"

def __repr__(self) -> str:
    """Return the same text for repr()."""
    return self.__str__()
```
The f-string formats the tuple inside the text, giving `Vector: ('Baratheon', 'brown', 'dark')`.

### 4.4 Why the expected output looks odd (`bound method ... of Vector: ...`)
`print(Robert.__str__)` has no parentheses, so it prints the **method object**. A bound method's text is `<bound method Class.method of {repr(instance)}>`. The part after `of` is the **`repr` of the instance**. Because your `__repr__` returns `Vector: ('Baratheon', 'brown', 'dark')`, the output matches the subject exactly. If you don't define `__repr__`, you'd see something like `<__main__.Baratheon object at 0x7f...>` instead.

### 4.5 Class methods and factories
A normal method receives the **instance** (`self`). A class method receives the **class** (`cls`):
```python
class Lannister(Character):
    ...
    @classmethod
    def create_lannister(
        cls, first_name: str, is_alive: bool = True
    ) -> "Lannister":
        """Create a Lannister and return it."""
        return cls(first_name, is_alive)
```
- `@classmethod` is the "decorator" the prototype comment mentions.
- Call it on the class: `Lannister.create_lannister("Jaine", True)`; no existing object needed.
- `cls(first_name, is_alive)` is the same as `Lannister(first_name, is_alive)`, but it adapts to subclasses (a subclass calling it gets an instance of the subclass).
- The return type is written as the string `"Lannister"` because the class isn't fully defined yet while its own methods are being read.
- **"In a chain"** means you can produce several characters by calling the factory repeatedly:
  ```python
  names = ["Jaime", "Tyrion", "Tywin"]
  family = [Lannister.create_lannister(n) for n in names]
  ```

### 4.6 Testing your own `S1E7.py`
Keep the subject's tester as your `tester.py`. Also test: `Baratheon.__mro__` (parents), `str(Robert)`, `repr(Robert)`, and that `isinstance(Robert, Character)` is `True`.

---

## 5. Syntax and Examples

### Step-by-step snippet
```python
from abc import ABC, abstractmethod


class Animal(ABC):
    """Abstract animal."""

    def __init__(self, name: str) -> None:
        """Store the name."""
        self.name = name

    @abstractmethod
    def sound(self) -> str:
        """Return the sound (to implement)."""


class Dog(Animal):
    """A dog."""

    def __init__(self, name: str) -> None:
        """Initialize a dog."""
        super().__init__(name)
        self.legs = 4

    def sound(self) -> str:
        """Return the dog sound."""
        return "Woof"

    def __repr__(self) -> str:
        """Return an unambiguous text."""
        return f"Dog: {(self.name, self.legs)}"

    @classmethod
    def puppy(cls, name: str) -> "Dog":
        """Create a dog named after the given name."""
        return cls(name + " Jr")


def main() -> None:
    """Show super(), __repr__ and a class method."""
    d = Dog.puppy("Rex")
    print(d.__dict__)
    print(d)
    print(d.sound)


if __name__ == "__main__":
    main()
```
Output:
```
{'name': 'Rex Jr', 'legs': 4}
Dog: ('Rex Jr', 4)
<bound method Dog.sound of Dog: ('Rex Jr', 4)>
```
(`print(d)` falls back on `__repr__` when `__str__` isn't defined.)

---

## 6. How to Think About the Exercise

1. **Step 1: Import** `Character` from `S1E9` (copy `S1E9.py` into `ex01/`).
2. **Step 2: Write `Baratheon`**: docstring `"Representing the Baratheon family."`, `__init__` with `super().__init__`, the three traits, `die`, `__str__`, `__repr__`.
3. **Step 3: Write `Lannister`** the same way with its own traits, plus the `@classmethod create_lannister`.
4. **Step 4: Check** that both `__str__` and `__repr__` return a `str`.
5. **Step 5: Run the subject's tester** and compare line by line, especially `__dict__` order and the `bound method` lines.
6. **Step 6: Check** `Lannister.create_lannister("Jaine", True)` gives a `Lannister` with the right name and state.
7. **Step 7: `flake8`** on both files.

---

## 7. Guided Practice

**Practice 1 (`__str__` vs `__repr__`):**
Create `Point(x, y)` with `__str__` returning `"(1, 2)"` style and `__repr__` returning `"Point(1, 2)"` style. Print the object, its `repr`, and a list containing it.

Expected output:
```
(1, 2)
Point(1, 2)
[Point(1, 2)]
```

<details><summary>Solution</summary>

```python
class Point:
    """A point in 2D."""

    def __init__(self, x: int, y: int) -> None:
        """Store the coordinates."""
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """Return a readable text."""
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        """Return an unambiguous text."""
        return f"Point({self.x}, {self.y})"


def main() -> None:
    """Compare str, repr and a list display."""
    p = Point(1, 2)
    print(p)
    print(repr(p))
    print([p])


if __name__ == "__main__":
    main()
```
</details>

**Practice 2 (The classic error: returning an object):**
Create a class whose `__str__` returns a tuple, then catch the error and print its message.

Expected output:
```
__str__ returned non-string (type tuple)
```

<details><summary>Solution</summary>

```python
class Bad:
    """A class with a wrong __str__."""

    def __str__(self):
        """Wrongly return a tuple."""
        return ("a", "b")


def main() -> None:
    """Show the error raised by a non-string __str__."""
    try:
        print(Bad())
    except TypeError as e:
        print(e)


if __name__ == "__main__":
    main()
```
</details>

**Practice 3 (What `print(obj.__str__)` really prints):**
Using `Point` from Practice 1, print `p.__str__` (no parentheses).

Expected output:
```
<bound method Point.__str__ of Point(1, 2)>
```

<details><summary>Solution</summary>

```python
class Point:
    """A point in 2D."""

    def __init__(self, x: int, y: int) -> None:
        """Store the coordinates."""
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """Return a readable text."""
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        """Return an unambiguous text."""
        return f"Point({self.x}, {self.y})"


def main() -> None:
    """Print a bound method: its text contains repr(instance)."""
    p = Point(1, 2)
    print(p.__str__)


if __name__ == "__main__":
    main()
```
</details>

**Practice 4 (Two siblings of one abstract parent, with `super()`):**
Create the abstract `Base(name)` with an abstract `trait`. Make `Red(Base)` and `Blue(Base)`, each adding a `color` attribute after `super().__init__` and implementing `trait`. Print both `__dict__`.

Expected output:
```
{'name': 'A', 'color': 'red'}
{'name': 'B', 'color': 'blue'}
```

<details><summary>Solution</summary>

```python
from abc import ABC, abstractmethod


class Base(ABC):
    """Abstract parent."""

    def __init__(self, name: str) -> None:
        """Store the name."""
        self.name = name

    @abstractmethod
    def trait(self) -> str:
        """Return a trait (to implement)."""


class Red(Base):
    """A red child."""

    def __init__(self, name: str) -> None:
        """Initialize with the parent constructor first."""
        super().__init__(name)
        self.color = "red"

    def trait(self) -> str:
        """Return the trait."""
        return "warm"


class Blue(Base):
    """A blue child."""

    def __init__(self, name: str) -> None:
        """Initialize with the parent constructor first."""
        super().__init__(name)
        self.color = "blue"

    def trait(self) -> str:
        """Return the trait."""
        return "cold"


def main() -> None:
    """Create both children and show their attributes."""
    print(Red("A").__dict__)
    print(Blue("B").__dict__)


if __name__ == "__main__":
    main()
```
</details>

**Practice 5 (A class method factory and a chain):**
Create `Family(name, is_alive=True)` with a class method `create` returning `cls(...)`. Create `Sub(Family)` with no changes. Show that `Family.create` builds a `Family` and `Sub.create` builds a `Sub`, then build three families in a chain.

Expected output:
```
Family Sub
['A', 'B', 'C']
```

<details><summary>Solution</summary>

```python
class Family:
    """A family member."""

    def __init__(self, name: str, is_alive: bool = True) -> None:
        """Store the name and the state."""
        self.name = name
        self.is_alive = is_alive

    @classmethod
    def create(cls, name: str, is_alive: bool = True) -> "Family":
        """Create an instance of the class it is called on."""
        return cls(name, is_alive)


class Sub(Family):
    """A subclass that inherits the factory."""


def main() -> None:
    """Show that cls adapts to the class used for the call."""
    a = Family.create("A")
    b = Sub.create("B")
    print(type(a).__name__, type(b).__name__)
    chain = [Family.create(n) for n in ("A", "B", "C")]
    print([m.name for m in chain])


if __name__ == "__main__":
    main()
```
</details>

**Practice 6 (Hardest, the full rule-compliant `S1E7.py`):**

Needs `S1E9.py` from ex00 in the same folder. Expected output: the subject's expected output (section 1).

<details><summary>Solution</summary>

```python
from S1E9 import Character


class Baratheon(Character):
    """Representing the Baratheon family."""

    def __init__(self, first_name: str, is_alive: bool = True) -> None:
        """Initialize a Baratheon with the family traits."""
        super().__init__(first_name, is_alive)
        self.family_name = "Baratheon"
        self.eyes = "brown"
        self.hairs = "dark"

    def die(self) -> None:
        """Pass is_alive from True to False."""
        self.is_alive = False

    def __str__(self) -> str:
        """Return the family traits as a string."""
        return f"Vector: {(self.family_name, self.eyes, self.hairs)}"

    def __repr__(self) -> str:
        """Return the same string for repr()."""
        return self.__str__()


class Lannister(Character):
    """Representing the Lannister family."""

    def __init__(self, first_name: str, is_alive: bool = True) -> None:
        """Initialize a Lannister with the family traits."""
        super().__init__(first_name, is_alive)
        self.family_name = "Lannister"
        self.eyes = "blue"
        self.hairs = "light"

    def die(self) -> None:
        """Pass is_alive from True to False."""
        self.is_alive = False

    def __str__(self) -> str:
        """Return the family traits as a string."""
        return f"Vector: {(self.family_name, self.eyes, self.hairs)}"

    def __repr__(self) -> str:
        """Return the same string for repr()."""
        return self.__str__()

    @classmethod
    def create_lannister(
        cls, first_name: str, is_alive: bool = True
    ) -> "Lannister":
        """Create a Lannister character and return it."""
        return cls(first_name, is_alive)
```
</details>

---

## 8. Exercise-Specific Knowledge

- **File layout:** `ex01/S1E9.py` (unchanged from ex00) and `ex01/S1E7.py`. The import `from S1E9 import Character` must work from inside `ex01/`.
- **`__dict__` order matters:** parent attributes first (`first_name`, `is_alive`), then `family_name`, `eyes`, `hairs`.
- **Traits:** Baratheon is `brown`/`dark`, Lannister is `blue`/`light`.
- **`__repr__` drives the `bound method ... of Vector: ...` lines.** The `Vector: (...)` text comes from the instance's `repr`.
- **Docstring check:** `Robert.__doc__` prints `Representing the Baratheon family.`, so the class docstring is what the subject expects (the wording may differ).
- **`create_lannister` takes `is_alive` as 2nd parameter** (`Lannister.create_lannister("Jaine", True)`); giving it a default of `True` keeps the one-argument call working too.
- **The last print** uses `{Jaine.first_name, type(Jaine).__name__}` inside an f-string: the comma makes a tuple, which is why the expected output shows `('Jaine', 'Lannister')`.
- **Duplicated `die`/`__str__`/`__repr__` in two classes is acceptable here.** It keeps `S1E9.py` unchanged; ex02 will inherit from both classes at once.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `TypeError: __str__ returned non-string (type tuple)` | Returned a tuple | Format it into an f-string |
| `TypeError: Can't instantiate abstract class Baratheon` | `die` not implemented | Add `die` to each family |
| `__dict__` shows family keys before `first_name` | Attributes set before `super().__init__` | Call `super().__init__` first |
| `AttributeError: ... has no attribute 'first_name'` | Forgot `super().__init__(...)` | Call it |
| Output shows `<__main__.Baratheon object at 0x...>` | No `__repr__` | Define `__repr__` returning a string |
| `TypeError: create_lannister() missing ...` | Missing `@classmethod` or `cls` | Decorate and use `cls` as first parameter |
| Created object is the wrong type | Returned something else than `cls(...)` | `return cls(first_name, is_alive)` |
| `ImportError: cannot import name 'Character'` | `S1E9.py` not in `ex01/` | Copy it there |
| `print(Robert.__str__())` instead of `__str__` | Added parentheses in the tester | Keep the subject's tester as is |
| Missing docstring on `__str__`, `__repr__` or the class method | Forgot them | Document every method |
| flake8 `E501` | Line over 79 characters | Format the f-string / signature on several lines |

---

## 10. Debugging Guide

- **Look at the object:** `print(Robert.__dict__)`, `print(type(Robert).__mro__)`.
- **`TypeError: __repr__ returned non-string`:** the method returns something that isn't a `str`; print `type(...)` of what you return.
- **Method output looks wrong:** call `str(Robert)` and `repr(Robert)` separately to see which one is incorrect.
- **Class method not found:** make sure the call is `Lannister.create_lannister(...)` (on the class) and that the method is indented inside the class.
- **Factory returns `None`:** you forgot `return`.
- **Infinite recursion in `__repr__`:** if `__str__` calls `str(self)` and `__repr__` calls `str(self)`, they call each other forever. Return the f-string in one of them and have the other return `self.__str__()`, like the solution does.
- **Run the checks:** `python -c "from S1E7 import Lannister; print(Lannister.create_lannister('Jaine'))"`.

---

## 11. Cheat Sheet

```python
class Baratheon(Character):
    """Representing the Baratheon family."""

    def __init__(self, first_name: str, is_alive: bool = True) -> None:
        """Initialize a Baratheon with the family traits."""
        super().__init__(first_name, is_alive)       # parent first
        self.family_name = "Baratheon"
        self.eyes = "brown"
        self.hairs = "dark"

    def die(self) -> None:
        """Pass is_alive from True to False."""
        self.is_alive = False

    def __str__(self) -> str:
        """Return the family traits as a string."""
        return f"Vector: {(self.family_name, self.eyes, self.hairs)}"

    def __repr__(self) -> str:
        """Return the same string for repr()."""
        return self.__str__()


@classmethod
def create_lannister(cls, first_name, is_alive=True):
    return cls(first_name, is_alive)       # inside class Lannister
```

---

## 12. Knowledge Checklist

- [ ] `S1E9.py` and `S1E7.py` are both in `ex01/`.
- [ ] `Baratheon` and `Lannister` inherit from `Character`, implement `die`, and can be instantiated directly.
- [ ] `__dict__` has the five keys in the expected order with the correct family traits.
- [ ] `__str__` and `__repr__` return strings (never tuples), and the `bound method ... of Vector: ...` lines match.
- [ ] `Lannister.create_lannister("Jaine", True)` returns a `Lannister` created through `cls(...)`.
- [ ] Every class and method has a docstring, and the class docstrings match the family names.
- [ ] I can explain `super()`, `__str__` vs `__repr__`, and `@classmethod` vs a normal method.
- [ ] No globals, nothing printed on import, `flake8` clean, final newline present.
