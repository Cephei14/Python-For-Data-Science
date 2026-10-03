# Study Tutorial — OOP Module, Exercise 02: DiamondTrap.py

## 1. Exercise Overview

**What it asks:**
Create a file `DiamondTrap.py` in directory `ex02/` with a class `King` that inherits from **both** `Baratheon` and `Lannister` (Joffrey, the "false" king, who is risky because he mixes two families):
```python
from S1E7 import Baratheon, Lannister

class King(Baratheon, Lannister):
    ...
```
1. A `King` is created with a first name only: `King("Joffrey")`.
2. By default his traits are the **Baratheon** ones (`eyes='brown'`, `hairs='dark'`, `family_name='Baratheon'`).
3. You must use **Properties** to read and change his physical characteristics, through the methods `set_eyes`, `set_hairs`, `get_eyes` and `get_hairs`.

**The subject's tester and expected output:**
```python
from DiamondTrap import King

Joffrey = King("Joffrey")
print(Joffrey.__dict__)
Joffrey.set_eyes("blue")
Joffrey.set_hairs("light")
print(Joffrey.get_eyes())
print(Joffrey.get_hairs())
print(Joffrey.__dict__)
```
```
{'first_name': 'Joffrey', 'is_alive': True, 'family_name': 'Baratheon', 'eyes': 'brown', 'hairs': 'dark'}
blue
light
{'first_name': 'Joffrey', 'is_alive': True, 'family_name': 'Baratheon', 'eyes': 'blue', 'hairs': 'light'}
```

The subject's hint: *"Since Python 2.3 the language uses C3 linearization to counter the problem of inheritance in diamond."*

**Rules and Constraints:**
- Files to turn in: **files from previous exercises + `DiamondTrap.py`** (so `ex02/` contains `S1E9.py`, `S1E7.py` and `DiamondTrap.py`). Allowed functions: **None**.
- Docstrings on every class, method and property (getter **and** setter), `flake8` clean, no globals, Python 3.10+.
- Uncaught exceptions invalidate the exercise.

**Main concepts you'll learn:**
- Multiple inheritance and the "diamond problem".
- The Method Resolution Order (MRO) and C3 linearization.
- Cooperative `super()` calls and why the **order of assignments** decides which family's traits win.
- Properties (`@property`, `@x.setter`) and where they store their data.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **ex00 / ex01:** classes, inheritance, abstract classes, `super().__init__(...)`, `__dict__`, instance attributes, docstrings.
- Your `S1E9.py` (`Character`) and `S1E7.py` (`Baratheon`, `Lannister`) files, unchanged.
- `try/except` for testing error cases.

Multiple inheritance, MRO and properties are explained in section 4.

---

## 3. Tools and Libraries

| Tool / Syntax | What it does | Scope / Notes |
|---|---|---|
| `from S1E7 import Baratheon, Lannister` | Imports both parents | `S1E7.py` and `S1E9.py` must be in `ex02/` |
| `class King(Baratheon, Lannister):` | **Multiple inheritance**: one child, two parents | Order matters: the left parent has priority |
| `King.__mro__` | Tuple of classes Python searches, in order | MRO = Method Resolution Order |
| `King.mro()` | Same information as a list | Handy for printing |
| `[c.__name__ for c in King.__mro__]` | Readable MRO | `['King', 'Baratheon', 'Lannister', 'Character', 'ABC', 'object']` |
| `super().__init__(first_name, is_alive)` | Calls the **next class in the MRO** | Not necessarily the direct parent |
| `@property` | Turns a method into a read-only attribute | `obj.eyes` calls the method, no parentheses |
| `@eyes.setter` | Defines what happens on `obj.eyes = value` | Name must match the property name |
| `self.__dict__["eyes"]` | Reads/writes the instance dictionary directly | Used to keep the `eyes` key (not `_eyes`) |
| `def get_eyes(self) -> str:` | Plain getter method required by the tester | Returns `self.eyes` |
| `def set_eyes(self, color: str) -> None:` | Plain setter method required by the tester | Does `self.eyes = color` |
| `obj.__dict__` | Instance attributes dictionary | Checked by the tester before and after |
| `isinstance(obj, Baratheon)` | Checks the inheritance | `True` for a `King` (and also for `Lannister`) |

**Common pitfalls:**
- **Defining the properties with a `_eyes` backing attribute.** `__dict__` would then contain `'_eyes'` instead of `'eyes'`, which doesn't match the expected output.
- **Infinite recursion in a property:** a getter written as `return self.eyes` (or a setter doing `self.eyes = x`) on the **same** property calls itself forever (`RecursionError`).
- **Assigning attributes before `super().__init__(...)`** in the parent classes: the other parent then overwrites them and Joffrey gets Lannister traits.
- **Calling `Character.__init__` directly** inside `Baratheon`: it works here but skips `Lannister` in the chain; use `super()`.
- **Parents listed in the wrong order** (`King(Lannister, Baratheon)`): the traits become Lannister's.
- **Forgetting the docstrings** on the property getter and setter methods.
- **Making `get_eyes` a property** (`@property def get_eyes`): then `Joffrey.get_eyes()` tries to call a string and fails.

---

## 4. Concepts You Need to Learn

### 4.1 Multiple inheritance and the diamond
```
        Character
        /       \
  Baratheon   Lannister
        \       /
          King
```
`King` inherits from two classes that both inherit from `Character`: a **diamond**. The risk: `Character.__init__` could run twice, or the wrong class's method could win. Python solves it with a clear, deterministic search order.

### 4.2 The MRO (C3 linearization)
Python builds a single ordered list of classes for `King` and searches it from left to right whenever you use `obj.attribute` or `super()`:
```python
print([c.__name__ for c in King.__mro__])
# ['King', 'Baratheon', 'Lannister', 'Character', 'ABC', 'object']
```
C3 linearization guarantees:
- Each class appears **once**.
- A class always comes **before its parents**.
- The order you wrote the bases in (`Baratheon, Lannister`) is respected.

That's why a `King` finds `Baratheon`'s methods before `Lannister`'s, and `Character` last, after both.

### 4.3 What `super()` really means
`super()` doesn't mean "my parent"; it means **"the next class in the MRO of the object"**. Inside `Baratheon.__init__`, `super().__init__(...)` for a `King` object goes to **`Lannister`**, not to `Character`:

```
King("Joffrey")           (King has no __init__, so Baratheon.__init__ runs)
 -> Baratheon.__init__    calls super().__init__  ->
    -> Lannister.__init__ calls super().__init__  ->
       -> Character.__init__  sets first_name, is_alive
    <- Lannister sets family_name='Lannister', eyes='blue', hairs='light'
 <- Baratheon sets family_name='Baratheon', eyes='brown', hairs='dark'   (overwrites!)
```
Result: `__dict__` keys are created in the order `first_name, is_alive, family_name, eyes, hairs` (insertion order of the first assignment), but the **values** end up being Baratheon's, because Baratheon's assignments run **last**. This is exactly the expected output, and your ex01 classes already behave this way **because they call `super().__init__(...)` first and assign their traits afterwards**.

If a family assigned its traits **before** calling `super().__init__`, the order of overwriting would flip and Joffrey would get Lannister's traits. See Practice 3.

### 4.4 Properties
A property lets you access a method like an attribute, with control over reading and writing:
```python
class Temperature:
    def __init__(self, celsius: float) -> None:
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """Return the temperature."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Set the temperature, refusing impossible values."""
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value
```
- `t.celsius` calls the getter; `t.celsius = 25` calls the setter.
- The usual convention stores the real data in `_celsius` (leading underscore = "internal").
- The setter can validate or transform values; that is the whole point of using a property instead of a plain attribute.

### 4.5 The twist: keep the key `eyes` in `__dict__`
The expected output shows the keys `eyes` and `hairs`, not `_eyes` and `_hairs`. With the usual `_eyes` convention, `__dict__` would contain `'_eyes'`, so the output would differ. The solution: the property stores its value **directly in the instance dictionary under the key `"eyes"`**:
```python
@property
def eyes(self) -> str:
    """Eye color of the king."""
    return self.__dict__["eyes"]

@eyes.setter
def eyes(self, color: str) -> None:
    """Change the eye color of the king."""
    self.__dict__["eyes"] = color
```
Why `self.__dict__[...]` and not `self.eyes`? Inside the property, `self.eyes` would call the property again, forever (`RecursionError`). Writing straight into `__dict__` bypasses the property.

Because `King` defines the property, even the assignments made in the **parents'** `__init__` (`self.eyes = "brown"`) go through the setter and end up in `__dict__["eyes"]`. The key order is preserved.

### 4.6 The required methods `get_eyes`, `set_eyes`, `get_hairs`, `set_hairs`
The tester calls methods, not properties:
```python
Joffrey.set_eyes("blue")
print(Joffrey.get_eyes())
```
So `King` offers both:
```python
def get_eyes(self) -> str:
    """Return the eye color."""
    return self.eyes

def set_eyes(self, color: str) -> None:
    """Set the eye color."""
    self.eyes = color
```
The simplest valid solution is to write **only** these four methods working on `self.eyes` / `self.hairs` (plain attributes). Because the subject says you **must use Properties**, the full solution also defines the `eyes` and `hairs` properties and lets the methods use them.

### 4.7 Why no `__init__` in `King`
`King("Joffrey")` works as is: Python finds `__init__` in `Baratheon` first (MRO), and its `super()` chain takes care of the rest. `die`, `__str__`, `__repr__` are inherited from `Baratheon` too, so `King` is a concrete class.

---

## 5. Syntax and Examples

### Step-by-step snippet
```python
class A:
    """Grandparent."""

    def __init__(self) -> None:
        """Say hello."""
        print("A init")


class B(A):
    """Left parent."""

    def __init__(self) -> None:
        """Say hello, then continue the chain."""
        print("B start")
        super().__init__()
        print("B end")


class C(A):
    """Right parent."""

    def __init__(self) -> None:
        """Say hello, then continue the chain."""
        print("C start")
        super().__init__()
        print("C end")


class D(B, C):
    """Child of both."""


def main() -> None:
    """Show the order of the cooperative super() calls."""
    D()
    print([c.__name__ for c in D.__mro__])


if __name__ == "__main__":
    main()
```
Output:
```
B start
C start
A init
C end
B end
['D', 'B', 'C', 'A', 'object']
```
`B`'s `super()` went to **`C`**, not to `A`: that is the MRO at work, and `A` runs only once.

---

## 6. How to Think About the Exercise

1. **Step 1: Copy `S1E9.py` and `S1E7.py`** into `ex02/` (unchanged, from ex00 and ex01).
2. **Step 2: Print `King.__mro__`** after declaring `class King(Baratheon, Lannister)` and understand the order.
3. **Step 3: Check the default traits:** `King("Joffrey").__dict__` must show Baratheon's values (this should already work if your ex01 classes call `super().__init__` first).
4. **Step 4: Write the four methods** `get_eyes`, `set_eyes`, `get_hairs`, `set_hairs` and compare with the expected output.
5. **Step 5: Add the `eyes` and `hairs` properties** (getter + setter, stored in `__dict__`) and let the methods use them.
6. **Step 6: Docstrings everywhere**, including each property getter and setter.
7. **Step 7: Run the subject's tester and `flake8`.**

---

## 7. Guided Practice

**Practice 1 (The MRO of a diamond):**
Create `A`, `B(A)`, `C(A)`, `D(B, C)` with no content and print the names in `D`'s MRO.

Expected output:
```
['D', 'B', 'C', 'A', 'object']
```

<details><summary>Solution</summary>

```python
class A:
    """Grandparent."""


class B(A):
    """Left parent."""


class C(A):
    """Right parent."""


class D(B, C):
    """Child of both."""


def main() -> None:
    """Print the method resolution order of D."""
    print([c.__name__ for c in D.__mro__])


if __name__ == "__main__":
    main()
```
</details>

**Practice 2 (Cooperative `super()`):**
Use the classes of section 5. Run `D()` and observe that `B`'s `super()` calls `C`. Expected output: see section 5.

<details><summary>Solution</summary>

The snippet in section 5 is the solution. Remove the `main()` print of the MRO if you only want the five lines of constructor output.
</details>

**Practice 3 (Who wins: the order of assignment):**
Create `Base` setting `color = "base"`. `Left(Base)` and `Right(Base)` each call `super().__init__()` **first** and then set their own color (`"left"` / `"right"`). `Both(Left, Right)`. Then create `LeftBad(Base)` that sets its color **before** calling `super().__init__()`, and `BothBad(LeftBad, Right)`. Print the color of `Both()` and `BothBad()`.

Expected output:
```
left
right
```

<details><summary>Solution</summary>

```python
class Base:
    """Root class."""

    def __init__(self) -> None:
        """Set the default color."""
        self.color = "base"


class Left(Base):
    """Calls super() first, then sets its own color."""

    def __init__(self) -> None:
        """Initialize the chain, then set the color."""
        super().__init__()
        self.color = "left"


class Right(Base):
    """Calls super() first, then sets its own color."""

    def __init__(self) -> None:
        """Initialize the chain, then set the color."""
        super().__init__()
        self.color = "right"


class Both(Left, Right):
    """Left has priority."""


class LeftBad(Base):
    """Sets its color BEFORE calling super()."""

    def __init__(self) -> None:
        """Set the color, then initialize the chain."""
        self.color = "left"
        super().__init__()


class BothBad(LeftBad, Right):
    """The next class in the chain overwrites the color."""


def main() -> None:
    """Show how the order of assignment decides the result."""
    print(Both().color)
    print(BothBad().color)


if __name__ == "__main__":
    main()
```

In `BothBad`, `LeftBad` sets `left`, then its `super()` runs `Right`, which sets `right` afterwards. That is the trap to avoid with `Baratheon` and `Lannister`.
</details>

**Practice 4 (A basic property):**
Create `Temperature` with a `celsius` property that refuses values below `-273.15` (raise `ValueError`). Print the value, change it to 25, print it, try `-300` (catch the error), and print the `__dict__`.

Expected output:
```
20
25
ValueError caught
{'_celsius': 25}
```

<details><summary>Solution</summary>

```python
class Temperature:
    """A temperature in Celsius."""

    def __init__(self, celsius: float) -> None:
        """Store the temperature."""
        self._celsius = celsius

    @property
    def celsius(self) -> float:
        """Return the temperature."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float) -> None:
        """Set the temperature, refusing impossible values."""
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value


def main() -> None:
    """Use the getter and the setter."""
    t = Temperature(20)
    print(t.celsius)
    t.celsius = 25
    print(t.celsius)
    try:
        t.celsius = -300
    except ValueError:
        print("ValueError caught")
    print(t.__dict__)


if __name__ == "__main__":
    main()
```

Notice `__dict__` holds `_celsius`, not `celsius`. This is the behavior the exercise wants to avoid for `eyes`.
</details>

**Practice 5 (A property that keeps its key name, and the recursion trap):**
Create `Bad` with a property `eyes` whose getter returns `self.eyes`, and catch the `RecursionError`. Then create `Good` with a property `eyes` stored in `__dict__["eyes"]`; set it to `"brown"` in `__init__`, change it to `"blue"` and print the `__dict__` after each.

Expected output:
```
RecursionError caught
{'eyes': 'brown'}
{'eyes': 'blue'}
```

<details><summary>Solution</summary>

```python
class Bad:
    """A property that calls itself."""

    @property
    def eyes(self) -> str:
        """Wrongly return the property itself."""
        return self.eyes


class Good:
    """A property stored under the key 'eyes' of __dict__."""

    def __init__(self) -> None:
        """Set the default eye color through the setter."""
        self.eyes = "brown"

    @property
    def eyes(self) -> str:
        """Return the eye color."""
        return self.__dict__["eyes"]

    @eyes.setter
    def eyes(self, color: str) -> None:
        """Change the eye color."""
        self.__dict__["eyes"] = color


def main() -> None:
    """Show the recursion trap and the fix."""
    try:
        print(Bad().eyes)
    except RecursionError:
        print("RecursionError caught")
    g = Good()
    print(g.__dict__)
    g.eyes = "blue"
    print(g.__dict__)


if __name__ == "__main__":
    main()
```
</details>

**Practice 6 (Hardest, the full rule-compliant `DiamondTrap.py`):**

Needs `S1E9.py` (ex00) and `S1E7.py` (ex01) in the same folder. Expected output: the subject's expected output (section 1).

<details><summary>Solution</summary>

```python
from S1E7 import Baratheon, Lannister


class King(Baratheon, Lannister):
    """Joffrey, the false king: Baratheon traits that can be changed."""

    @property
    def eyes(self) -> str:
        """Return the eye color of the king."""
        return self.__dict__["eyes"]

    @eyes.setter
    def eyes(self, color: str) -> None:
        """Change the eye color of the king."""
        self.__dict__["eyes"] = color

    @property
    def hairs(self) -> str:
        """Return the hair color of the king."""
        return self.__dict__["hairs"]

    @hairs.setter
    def hairs(self, color: str) -> None:
        """Change the hair color of the king."""
        self.__dict__["hairs"] = color

    def get_eyes(self) -> str:
        """Return the eye color."""
        return self.eyes

    def set_eyes(self, color: str) -> None:
        """Set the eye color."""
        self.eyes = color

    def get_hairs(self) -> str:
        """Return the hair color."""
        return self.hairs

    def set_hairs(self, color: str) -> None:
        """Set the hair color."""
        self.hairs = color
```

Minimal alternative (only plain methods, no properties): keep just the four `get_*`/`set_*` methods, working on `self.eyes` and `self.hairs`. It passes the tester, but doesn't "use Properties" as the subject asks.
</details>

---

## 8. Exercise-Specific Knowledge

- **Why the traits are Baratheon's:** `King(Baratheon, Lannister)` puts `Baratheon` first in the MRO, and its `__init__` assigns its traits **last** (after the chain through `Lannister` and `Character` returned).
- **Why `__dict__` order is `first_name, is_alive, family_name, eyes, hairs`:** the deepest class (`Character`) assigns first, then `Lannister` creates the keys, then `Baratheon` overwrites the values (an overwritten key keeps its original position).
- **Your ex01 code must follow the same pattern** (`super().__init__` first, traits after). If `King("Joffrey").__dict__` already shows Baratheon traits before you write anything else, ex01 is right.
- **Properties on `King`, not on the parents:** the parents keep plain attributes; only `King` needs the controlled access. Assignments in the parents' `__init__` are routed through `King`'s setters automatically.
- **The tester only uses methods**, never `Joffrey.eyes` directly, but the properties must exist because the subject requires them.
- **`ex02/` must contain** `S1E9.py`, `S1E7.py`, `DiamondTrap.py`.
- **Be ready to explain** in the defence: what the diamond problem is, what the MRO is, what `super()` really does, and why `__dict__` is used inside the properties.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `__dict__` has `_eyes` / `_hairs` | Properties stored in `_eyes` | Store in `self.__dict__["eyes"]` |
| `RecursionError` | Getter/setter uses `self.eyes` of the same property | Use `self.__dict__["eyes"]` inside the property |
| Joffrey has blue eyes by default | Parents' traits assigned before `super().__init__`, or `King(Lannister, Baratheon)` | Call `super().__init__` first; keep the base order |
| `TypeError: 'str' object is not callable` | `get_eyes` was made a property | Keep `get_eyes` a normal method |
| `AttributeError: can't set attribute` | Property without a setter | Add `@eyes.setter` |
| Setter not working | Setter name differs from the property name | `@eyes.setter def eyes(...)` |
| `TypeError: Cannot create a consistent method resolution order` | Inconsistent base order in a diamond | Keep `King(Baratheon, Lannister)` |
| `ImportError` | Files missing in `ex02/` | Copy `S1E9.py` and `S1E7.py` there |
| Missing docstring on the setter | Each decorated method needs one | Document getters **and** setters |
| flake8 `E301`/`E303` | Wrong blank lines between methods | One blank line between methods |

---

## 10. Debugging Guide

- **Print the MRO:** `print([c.__name__ for c in King.__mro__])` should be `['King', 'Baratheon', 'Lannister', 'Character', 'ABC', 'object']`.
- **Trace the chain:** temporarily add `print("Baratheon init")` / `print("Lannister init")` to the constructors to see the order (remove afterwards).
- **Wrong default traits:** check that in both `Baratheon` and `Lannister`, `super().__init__(first_name, is_alive)` is the **first** line of `__init__`.
- **`KeyError: 'eyes'`:** a property getter was called before any value was stored; make sure `__init__` of the parents ran (they set `self.eyes`).
- **Property not used:** `print(type(King.eyes))` should print `<class 'property'>`.
- **`__dict__` mismatch with the subject:** compare the **keys and their order**, then the values.
- **Quick check:**
  ```python
  python -c "from DiamondTrap import King; k = King('J'); print(k.__dict__)"
  ```

---

## 11. Cheat Sheet

```python
from S1E7 import Baratheon, Lannister


class King(Baratheon, Lannister):
    """Joffrey, the false king: Baratheon traits that can be changed."""

    @property
    def eyes(self) -> str:
        """Return the eye color of the king."""
        return self.__dict__["eyes"]

    @eyes.setter
    def eyes(self, color: str) -> None:
        """Change the eye color of the king."""
        self.__dict__["eyes"] = color

    # same for hairs ...

    def get_eyes(self) -> str:
        """Return the eye color."""
        return self.eyes

    def set_eyes(self, color: str) -> None:
        """Set the eye color."""
        self.eyes = color

    # same for get_hairs / set_hairs ...
```

---

## 12. Knowledge Checklist

- [ ] `ex02/` contains `S1E9.py`, `S1E7.py` and `DiamondTrap.py`.
- [ ] `King` inherits from `Baratheon, Lannister` (in that order) and can be created with `King("Joffrey")`.
- [ ] The default `__dict__` shows the Baratheon traits in the expected key order.
- [ ] `set_eyes`, `set_hairs`, `get_eyes`, `get_hairs` work and the final `__dict__` matches the subject.
- [ ] Properties with getters and setters exist for `eyes` and `hairs`, storing under the keys `eyes` and `hairs`.
- [ ] Every class, method, getter and setter has a docstring.
- [ ] I can explain the diamond problem, the MRO (C3 linearization), what `super()` does in this chain, and why the properties use `__dict__`.
- [ ] No globals, nothing printed on import, `flake8` clean, final newline present.
