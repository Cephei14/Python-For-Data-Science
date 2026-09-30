# Anki Deck: Python for Data Science — Module 0 (Starting)

This deck is organized into **10 exercise-grouped subdecks**, focusing strictly on **foundational Python concepts, memory models, data types, and core Data Science essentials**.

- **Deck Hierarchy:** `42-Python-Data-Science::Python-0-Starting::<ex00..ex09>`
- **Total High-Yield Cards:** 74
- **Packages Generated:** `42-Python-Data-Science-reviewed.apkg`, `42-Python-Data-Science-Foundations.apkg`, `Python-0-Starting.apkg`

---

## Deck Architecture & Summary

| Subdeck | Core Concept Focus | Card Count |
|---|---|---|
| **ex00** | Core Collections (List, Tuple, Set, Dict), Mutability, Memory References, Identity vs Equality, Slicing | 8 |
| **ex01** | Types, Numbers & Time (Unix Epoch, F-String Formatting, strftime Directives, Float Precision & IEEE 754) | 7 |
| **ex02** | Type System & Functions (type() vs isinstance(), Boolean Inheritance Trap, Type Hints at Runtime, Dynamic vs Strong) | 7 |
| **ex03** | Nulls, Truthiness & IEEE 754 (Data Type of NaN, NaN != NaN Rule, Safe NaN Detection, Truthiness vs Falsiness, None vs NaN) | 8 |
| **ex04** | CLI, Validation & Control Flow (sys.argv, -5.isdigit() Trap, Modulo with Negatives, Division / vs //, EAFP vs LBYL) | 7 |
| **ex05** | Script Structure & Strings (if __name__ == "__main__", Character Methods, string.punctuation, String Immutability, LEGB Scope) | 7 |
| **ex06** | Comprehensions & Functional (List Comprehension Syntax, Memory of Lists vs Generators, filter(), Lambdas & E731) | 7 |
| **ex07** | Dictionaries & Hashing (Hash Maps O(1), Safe .get(), Iteration .items(), join() O(N) vs += O(N^2), defaultdict) | 7 |
| **ex08** | Generators & Memory Optimization (yield vs return, Lazy Evaluation, Iterator Protocol, Generator Exhaustion, \r Terminal UI) | 8 |
| **ex09** | Packaging, Pip & Environments (__init__.py, Project Structure, pyproject.toml, sdist vs Wheel, Editable Mode, venv) | 8 |

---

## Card Inventory by Subdeck

### Subdeck: `42-Python-Data-Science::Python-0-Starting::ex00`

#### Card 1: ex00 (Collections): What are the 4 core built-in Python collection types and their mutability?
> **Tags:** `ex00 collections mutability data-structures`  
>
> • **`list`** (`[...]`): Ordered sequence, **Mutable**, allows duplicates, indexed by integers.
> • **`tuple`** (`(...)`): Ordered sequence, **Immutable**, allows duplicates, indexed by integers.
> • **`set`** (`{...}`): Unordered collection, **Mutable**, **No duplicates**, no index access.
> • **`dict`** (`{k: v}`): Key-Value mapping, **Mutable**, keys must be unique &amp; hashable.

---

#### Card 2: ex00 (Collections): What happens if you execute my_tuple[1] = "new", and how do you "modify" a tuple?
> **Tags:** `ex00 tuple immutability errors`  
>
> Raises **`TypeError: 'tuple' object does not support item assignment`** because tuples are **immutable**.
> 
> **To update a tuple:** You cannot mutate the existing instance in-place. You must construct a **new tuple** and rebind the variable:
> `my_tuple = (my_tuple[0], "new") + my_tuple[2:]`

---

#### Card 3: ex00 (Collections): Why can't you access set elements by index (e.g. my_set[0]), and how do you replace an element?
> **Tags:** `ex00 set indexing hash-table complexity`  
>
> Sets are implemented as **hash tables without ordered positional slots** (indexing raises `TypeError: 'set' object is not subscriptable`).
> 
> **To replace an item in a set:**
> 1. `my_set.remove("old")` (raises `KeyError` if missing) or `my_set.discard("old")` (silently ignores if absent).
> 2. `my_set.add("new")`
> 
> *Data Science note:* Sets provide **$O(1)$ average-time membership testing** (`x in my_set`), compared to $O(N)$ linear scans for lists.

---

#### Card 4: ex00 (Collections): How does dictionary key assignment my_dict[key] = value behave when the key exists vs when it does not?
> **Tags:** `ex00 dict assignment mutation`  
>
> • **If the key exists:** Its existing value is overwritten in-place.
> • **If the key does not exist:** A new key-value pair is inserted into the dictionary.
> 
> *Note:* In Python 3.7+, dictionaries preserve **insertion order**.

---

#### Card 5: ex00 (Collections): What objects are valid dictionary keys or set elements in Python, and why is a tuple containing a list invalid?
> **Tags:** `ex00 hashable dict set immutability types`  
>
> Only **hashable** objects (objects whose hash value never changes during their lifetime, implementing `__hash__()` and `__eq__()`).
> 
> • **Valid (Immutable built-ins):** `int`, `float`, `str`, `bool`, `tuple` (if all elements are hashable), `frozenset`.
> • **Invalid (Mutable containers):** `list`, `dict`, `set` (raises `TypeError: unhashable type: 'list'`).
> 
> *The Tuple Trap:* `(1, [2, 3])` is a tuple, but because it contains a mutable `list`, the whole tuple is **unhashable** and cannot be a dict key or set element.

---

#### Card 6: ex00 (Memory & References): If a = [1, 2, 3] and b = a, what happens to a when you run b.append(4)? Why?
> **Tags:** `ex00 memory references assignment mutability`  
>
> **`a` also becomes `[1, 2, 3, 4]`!**
> 
> **Reason:** In Python, variables do not hold data values; they are **references (pointers) to objects in memory**. `b = a` does not duplicate the list; it binds `b` to the exact same list instance (`id(a) == id(b)`).
> 
> To create an independent copy, use a shallow copy: `b = a.copy()` or `b = list(a)`.

---

#### Card 7: ex00 (Identity vs Equality): What is the difference between a == b and a is b in Python?
> **Tags:** `ex00 identity equality is-operator memory`  
>
> • **`a == b` (Equality):** Invokes `a.__eq__(b)` to check if both objects have the **same value/content**.
> • **`a is b` (Identity):** Checks if `a` and `b` point to the **exact same memory address** (equivalent to `id(a) == id(b)`).
> 
> `x = [1, 2]
y = [1, 2]
x == y  # True (identical content)
x is y  # False (two distinct list instances in RAM)`

---

#### Card 8: ex00 (Slicing): What is the general syntax of Python slicing seq[start:stop:step], and what do seq[::-1] and seq[:3] do?
> **Tags:** `ex00 slicing sequences indexing`  
>
> **Syntax:** `seq[start:stop:step]` extracts elements from index `start` up to (not including) `stop`, incrementing by `step`.
> 
> • **`seq[::-1]`:** Reverses the sequence (starts from the end and steps backward by -1).
> • **`seq[:3]`:** Takes the first 3 items (indices 0, 1, 2).
> • **`seq[::2]`:** Takes every second item starting from index 0.
> 
> *Key rule:* Slicing a list or string returns a **new object** (shallow copy of that slice), leaving the original untouched.

---

### Subdeck: `42-Python-Data-Science::Python-0-Starting::ex01`

#### Card 9: ex01 (Time): What is Unix / Epoch time, and how do you retrieve it in Python?
> **Tags:** `ex01 time epoch datetime`  
>
> Unix epoch time is the number of seconds that have elapsed since **January 1, 1970 00:00:00 UTC**.
> 
> In Python:
> • **`time.time()`:** Returns the current epoch timestamp as a `float`.
> • **`datetime.now().timestamp()`:** Returns epoch seconds from a `datetime` object.

---

#### Card 10: ex01 (Formatting): In Python f-strings, what format specifier displays a number with thousands comma separators and 4 decimal places?
> **Tags:** `ex01 f-strings formatting numbers`  
>
> **`{val:,.4f}`**
> 
> Example:`val = 1666355857.362234
f"{val:,.4f}"  # '1,666,355,857.3622'`• `,` specifies comma as the thousands grouping character.
> • `.4f` formats the float with exactly 4 digits of precision after the decimal.

---

#### Card 11: ex01 (Formatting): In Python f-strings, what format specifier outputs a number in scientific notation with 2 decimal places?
> **Tags:** `ex01 f-strings formatting scientific-notation`  
>
> **`{val:.2e}`**
> 
> Example:`val = 1666355857.362234
f"{val:.2e}"  # '1.67e+09'`• `.2` specifies 2 digits after the decimal point.
> • `e` formats using exponential (scientific) notation.

---

#### Card 12: ex01 (Time): In strftime, what are the format codes for: (1) abbreviated month, (2) zero-padded day, (3) 4-digit year, (4) minutes?
> **Tags:** `ex01 datetime strftime formatting`  
>
> • **`%b`**: Abbreviated month name (e.g. `'Oct'`).
> • **`%d`**: Day of the month zero-padded (`'01'` to `'31'`).
> • **`%Y`**: 4-digit year (e.g. `'2022'`; lowercase `%y` is 2-digit).
> • **`%M`**: Minute zero-padded (`'00'` to `'59'`).
> 
> *Trap:* `%m` is **month number** (e.g. `'10'`), whereas `%M` is **minute**!

---

#### Card 13: ex01 (Numbers): Why does 0.1 + 0.2 == 0.3 evaluate to False in Python, and how should float equality be tested?
> **Tags:** `ex01 float ieee754 precision math`  
>
> **Reason:** Computers represent floats in base-2 binary (IEEE 754). Fractions like 0.1 and 0.2 cannot be represented exactly in binary and become repeating fractions, creating microscopic rounding discrepancies:`0.1 + 0.2  # 0.30000000000000004`**Solution:** Never test floats with `==`. Use **`math.isclose(a, b)`** or NumPy's `np.isclose(a, b)` with tolerance.

---

#### Card 14: ex01 (Time): What is the difference in purpose between Python's standard time module and datetime module?
> **Tags:** `ex01 time datetime standard-library`  
>
> • **`time` module:** Low-level, C-style time functions. Ideal for raw Unix epoch timestamps (`time.time()`), pausing execution (`time.sleep()`), and benchmarking (`time.perf_counter()`).
> • **`datetime` module:** High-level object-oriented dates and times. Represents calendar dates (`date`), times (`time`), combined (`datetime`), intervals (`timedelta`), and timezones.

---

#### Card 15: ex01 (Time): How do you convert a Unix epoch timestamp (float) into a human-readable datetime object, and vice versa?
> **Tags:** `ex01 datetime timestamp conversion`  
>
> • **Timestamp → Datetime:**
> `from datetime import datetime
dt = datetime.fromtimestamp(1666355857.36)`• **Datetime → Timestamp:**
> `ts = dt.timestamp()  # returns float seconds`

---

### Subdeck: `42-Python-Data-Science::Python-0-Starting::ex02`

#### Card 16: ex02 (Type System): How do you inspect an object's exact type in Python, and what does str(type(x)) produce?
> **Tags:** `ex02 type inspection types`  
>
> Use **`type(x)`**.
> 
> In Python, types are classes. Converting `type(x)` to a string outputs:
> `&lt;class 'list'&gt;`, `&lt;class 'str'&gt;`, `&lt;class 'int'&gt;`, `&lt;class 'dict'&gt;`.
> 
> You can test exact type equality with: `type(x) is list`.

---

#### Card 17: ex02 (Type Gotcha): Why does isinstance(True, int) return True, and how do you strictly verify an integer?
> **Tags:** `ex02 isinstance bool int inheritance gotchas`  
>
> In Python, **`bool` is a direct subclass of `int`** (`issubclass(bool, int) == True`), with `True == 1` and `False == 0`.
> 
> • `isinstance(True, int)` → **`True`** (because `isinstance` checks inheritance).
> • `type(True) is int` → **`False`** (exact type comparison).
> 
> **Takeaway:** If you must strictly exclude booleans when validating integers, check `type(x) is int` or `if isinstance(x, int) and not isinstance(x, bool):`.

---

#### Card 18: ex02 (Type System): What is the architectural difference between type(obj) is Class and isinstance(obj, Class)?
> **Tags:** `ex02 type isinstance polymorphism oop`  
>
> • **`isinstance(obj, Class)`:** Checks if `obj` is an instance of `Class` OR **any subclass** derived from it. Preferred in idiomatic Python because it supports **polymorphism and inheritance**.
> • **`type(obj) is Class`:** Checks for the **exact identity** of the class, ignoring subclasses.
> 
> Use `isinstance()` by default; use `type() is` only when subclass behavior must be deliberately avoided.

---

#### Card 19: ex02 (Type Hints): Are Python function type hints (e.g. def func(x: int) -&gt; str:) enforced by Python at runtime?
> **Tags:** `ex02 type-hints runtime static-analysis typing`  
>
> **No.** Python is dynamically typed. Type annotations are purely metadata stored in `func.__annotations__`.
> 
> CPython does NOT raise an error if you pass a string to an `int` parameter at runtime. Type hints exist for IDE autocompletion, documentation, and static type checkers like **mypy** or **pyright**.

---

#### Card 20: ex02 (Type System): Python is described as both dynamically typed and strongly typed. What does each term mean?
> **Tags:** `ex02 dynamic-typing strong-typing type-system`  
>
> • **Dynamically typed:** Variable types are resolved at runtime rather than compile-time. A variable name can bind to an `int`, and later be reassigned to a `str`.
> • **Strongly typed:** Python does **not** implicitly coerce incompatible types in operations. For example, `'5' + 5` raises `TypeError` (unlike JavaScript, which implicitly coerces to `'55'`).

---

#### Card 21: ex02 (Functions): What do *args and **kwargs do in a Python function definition?
> **Tags:** `ex02 functions args kwargs unpacking`  
>
> • **`*args`:** Collects any number of excess **positional arguments** into a **`tuple`**.
> • **`**kwargs`:** Collects any number of excess **keyword arguments** into a **`dict`**.
> 
> `def func(*args, **kwargs):
    print(args)    # (1, 2)
    print(kwargs)  # {'name': 'Alice'}

func(1, 2, name='Alice')`

---

#### Card 22: ex02 (Function Gotchas): Why is def append_item(val, items=[]) a dangerous bug, and what is the Pythonic fix?
> **Tags:** `ex02 functions default-arguments gotchas mutability`  
>
> **Reason:** Default argument expressions are evaluated **once when the function is defined**, NOT every time the function is called! The same mutable list is reused across every subsequent call.
> 
> **The Pythonic fix:** Use `None` as the default sentinel value:
> `def append_item(val, items=None):
    if items is None:
        items = []
    items.append(val)
    return items`

---

### Subdeck: `42-Python-Data-Science::Python-0-Starting::ex03`

#### Card 23: ex03 (Nulls &amp; Types): What is the exact data type of NaN (Not a Number) in Python, and how is it created in standard Python?
> **Tags:** `ex03 nan float ieee754 types data-science`  
>
> The data type of `NaN` is **`float`**!
> `type(float('nan'))  # &lt;class 'float'&gt;``NaN` is defined by the **IEEE 754 floating-point standard** to represent an undefined or unrepresentable numerical result (such as `0.0 / 0.0`). In Python, it is a standard floating-point value, **not** a distinct null type.

---

#### Card 24: ex03 (IEEE 754): Why does float('nan') == float('nan') evaluate to False, and why will x == float('nan') never detect NaN?
> **Tags:** `ex03 nan ieee754 equality math gotchas`  
>
> According to the **IEEE 754 standard**, **NaN is never equal to anything, including itself**:
> `float('nan') == float('nan')  # False`
> 
> Because of this rule, `x == float('nan')` always evaluates to `False`, even when `x` is NaN!
> 
> *Consequence:* Testing `x == float('nan')` is completely useless. Since NaN is the only float where `x != x` is `True`, some code checks `x != x`, but standard functions like `math.isnan()` are preferred.

---

#### Card 25: ex03 (NaN Detection): How do you safely check if a variable x is NaN in standard Python and in Data Science (NumPy/Pandas)?
> **Tags:** `ex03 nan math isnan numpy pandas data-science`  
>
> • **Standard Python:** Use **`math.isnan(x)`**.
> *Guard required:* `math.isnan('hello')` raises `TypeError: must be real number, not str`, so verify it is a float first:
> `isinstance(x, float) and math.isnan(x)`• **Data Science (NumPy / Pandas):**
> Use **`np.isnan(x)`** for NumPy arrays or **`pd.isna(x)`** for Pandas Series/DataFrames (which handles both `NaN` and `None`).

---

#### Card 26: ex03 (Truthiness): What does bool(float('nan')) evaluate to, and why does this cause major bugs in data cleaning?
> **Tags:** `ex03 nan truthiness bool gotchas data-cleaning`  
>
> **`bool(float('nan'))` evaluates to `True`!**
> 
> Unlike `None`, `0`, or `""`, `NaN` is **truthy**. Therefore, testing `if not x:` will **fail to detect missing NaN values**!
> 
> Always use `math.isnan(x)` or `pd.isna(x)` when cleaning missing numeric data.

---

#### Card 27: ex03 (Truthiness): What values in Python evaluate to False (Falsy) in a boolean context?
> **Tags:** `ex03 truthiness falsy bool nulls`  
>
> Everything in Python evaluates to **`True`** except:
> 1. Constants: **`None`**, **`False`**
> 2. Numeric zeros: **`0`**, **`0.0`**, **`0j`**, `Decimal(0)`, `Fraction(0, 1)`
> 3. Empty sequences &amp; collections: **`''`** (empty string), **`[]`**, **`()`**, **`{}`**, **`set()`**, **`range(0)`**
> 
> *Reminder:* `float('nan')` is **truthy**!

---

#### Card 28: ex03 (Data Science): What is the fundamental difference between None and NaN in Python and Pandas/NumPy?
> **Tags:** `ex03 none nan data-science pandas numpy`  
>
> • **`None`:** Python's native singleton object of type `NoneType`. It represents the absence of a value. In NumPy, putting `None` in an array forces the array's dtype to slow Python `object`.
> • **`NaN`:** A 64-bit floating-point value (`float`). In NumPy and Pandas, numeric columns use `NaN` for missing data so the array remains a compact C-level float array, enabling fast vectorized computation.

---

#### Card 29: ex03 (Best Practice): Why should you always check for None using x is None rather than x == None?
> **Tags:** `ex03 none identity comparison pep8`  
>
> 1. **Identity check:** `None` is a singleton; exactly one `None` object exists in memory. `is` compares pointer addresses directly (fastest possible operation).
> 2. **Immune to class overrides:** A custom class can override `__eq__()` to return bizarre results, but `is` cannot be overridden.
> 3. **PEP 8 Standard:** PEP 8 explicitly mandates `if x is None:`.

---

#### Card 30: ex03 (Gotchas): Why does if x == 0: match when x = False, and how do you prevent this bug?
> **Tags:** `ex03 bool int equality gotchas types`  
>
> Because `bool` subclasses `int`, **`False == 0` evaluates to `True`** (and `True == 1` is `True`).
> 
> If your logic needs to distinguish between the integer `0` and the boolean `False`, check:
> `if type(x) is int and x == 0:`or check `isinstance(x, bool)` first.

---

### Subdeck: `42-Python-Data-Science::Python-0-Starting::ex04`

#### Card 31: ex04 (CLI): In Python's sys.argv, what is sys.argv[0], and what data type are all argument elements?
> **Tags:** `ex04 sys argv cli strings`  
>
> • **`sys.argv[0]`:** The name or path of the script being executed.
> • **`sys.argv[1:]`:** Slices out the user-supplied command-line arguments.
> 
> *Crucial fact:* **All elements in `sys.argv` are strings (`str`)**. Even if the user passes numbers (e.g. `python script.py 42`), `sys.argv[1]` is the string `'42'`.

---

#### Card 32: ex04 (Validation): Why does '-5'.isdigit() return False, and how should you validate if a CLI string is an integer?
> **Tags:** `ex04 isdigit int validation strings exceptions`  
>
> `str.isdigit()` checks if **every character** is a digit. The minus sign `'-'` is punctuation, not a digit, so all negative integers return `False`!
> 
> **Robust Pythonic validation (EAFP):**
> `try:
    val = int(arg)
except ValueError:
    # Not a valid integer (e.g. 'abc' or '3.14')`

---

#### Card 33: ex04 (Math): What is the result of -5 % 2 in Python, and how does Python's modulo rule differ from C/C++?
> **Tags:** `ex04 math modulo division gotchas`  
>
> In Python, **`-5 % 2 == 1`** (odd).
> 
> **The Rule:** In Python, the modulo operator `%` always takes the **sign of the divisor** (here divisor `2` is positive, so remainder is positive `+1`). Python uses **flooring division** (`-5 // 2 == -3`, and `-3 * 2 + 1 == -5`).
> 
> In C/C++, division truncates toward zero, making `-5 % 2 == -1`. Python's behavior guarantees `n % 2 == 0` is always even for both positive and negative numbers!

---

#### Card 34: ex04 (Math): What is the difference between true division / and floor division // in Python?
> **Tags:** `ex04 division math operators`  
>
> • **`/` (True division):** **Always returns a `float`**, even if the division is exact (e.g. `4 / 2 == 2.0`).
> • **`//` (Floor division):** Divides and rounds down to the nearest smaller integer (towards negative infinity). If both operands are integers, it returns an `int` (e.g. `7 // 2 == 3`, but `-7 // 2 == -4`).

---

#### Card 35: ex04 (Architecture): What do the programming philosophies EAFP and LBYL stand for, and why is EAFP preferred in Python?
> **Tags:** `ex04 eafp lbyl pythonic exceptions architecture`  
>
> • **EAFP:** *"Easier to Ask for Forgiveness than Permission"*. Assume the operation will succeed and wrap it in a `try...except` block.
> • **LBYL:** *"Look Before You Leap"*. Explicitly test preconditions with `if` statements before performing the operation.
> 
> **Why EAFP is preferred:** It is more readable, handles edge cases cleanly, and prevents **race conditions** (TOCTOU: Time of Check to Time of Use).

---

#### Card 36: ex04 (Best Practice): Why is using assert condition, "Error" dangerous for validating user input in production code?
> **Tags:** `ex04 assert exceptions optimization best-practices`  
>
> When Python is executed with the **`-O` (optimize) flag** or with `PYTHONOPTIMIZE=1`, **all `assert` statements are completely stripped from bytecode**!
> 
> If you use `assert` to validate user input or permissions, running in optimized mode will skip all checks silently. In production, always use: `if not condition: raise ValueError(...)`.

---

#### Card 37: ex04 (Exceptions): Why is writing a bare except: or except BaseException: considered a severe anti-pattern in Python?
> **Tags:** `ex04 exceptions error-handling best-practices`  
>
> A bare `except:` catches **everything**, including:
> • `KeyboardInterrupt` (user pressing Ctrl+C)
> • `SystemExit` (`sys.exit()`)
> 
> This makes your program impossible to terminate via the terminal and hides typos (e.g. `NameError`). Always catch the most specific exception (e.g. `except ValueError:`) or at most `except Exception:`.

---

### Subdeck: `42-Python-Data-Science::Python-0-Starting::ex05`

#### Card 38: ex05 (Script Structure): What does if __name__ == "__main__": do and why is it standard practice in Python scripts?
> **Tags:** `ex05 script-structure entry-point modules`  
>
> Whenever Python runs a file directly (e.g. `python script.py`), it sets the special variable `__name__ = '__main__'`. When a file is **imported** into another module, Python sets `__name__` to the file's module name.
> 
> The guard ensures that CLI execution code (such as argument parsing or testing) only runs when the file is executed directly, preventing accidental execution when the module is imported.

---

#### Card 39: ex05 (Strings): What built-in string methods test if characters are: (1) uppercase, (2) lowercase, (3) alphabetic, (4) digits, (5) whitespace?
> **Tags:** `ex05 string-methods character-classification strings`  
>
> • **`s.isupper()`**: True if all cased characters are uppercase.
> • **`s.islower()`**: True if all cased characters are lowercase.
> • **`s.isalpha()`**: True if all characters are alphabetic letters.
> • **`s.isdigit()`**: True if all characters are digits.
> • **`s.isspace()`**: True if all characters are whitespace (space, tab, newline).

---

#### Card 40: ex05 (Strings): How do you check if a character is a punctuation symbol in Python without writing a custom regex?
> **Tags:** `ex05 string punctuation standard-library`  
>
> Import the standard library **`string`** module and use membership testing with **`string.punctuation`**:
> `import string

if char in string.punctuation:
    print('Punctuation mark!')``string.punctuation` contains all standard ASCII punctuation symbols: `!"#$%&'()*+,-./:;&lt;=&gt;?@[\]^_`{|}~`.

---

#### Card 41: ex05 (Strings): Are Python strings mutable or immutable? What happens when you do text = text.upper()?
> **Tags:** `ex05 strings immutability memory`  
>
> Python strings are **immutable**. You cannot modify an existing string in memory.
> 
> Calling `text.upper()` does not modify the original string; it allocates memory for an **entirely new string object** and returns it. The variable `text` is simply rebound to point to the new object.

---

#### Card 42: ex05 (Namespaces): In what order does Python search for variable names? What is the LEGB rule?
> **Tags:** `ex05 scope legb namespaces variables`  
>
> Python resolves variable names by searching scopes in this exact order:
> 1. **L (Local):** Inside the current function.
> 2. **E (Enclosing):** Inside any outer enclosing functions (closures).
> 3. **G (Global):** At the top level of the current module file.
> 4. **B (Built-in):** Built-in Python names (`len`, `range`, `int`).

---

#### Card 43: ex05 (I/O): What is the key difference between input() and sys.stdin.readline() regarding newline characters?
> **Tags:** `ex05 io stdin input strings`  
>
> • **`input(prompt)`:** Reads a line from standard input and **strips the trailing newline character (`\n`)**.
> • **`sys.stdin.readline()`:** Reads a line from standard input and **retains the trailing newline (`\n`)** (except for the last line if EOF is reached without a newline).

---

#### Card 44: ex05 (Strings): What do strip(), lstrip(), and rstrip() do, and what do they strip by default?
> **Tags:** `ex05 strings strip formatting`  
>
> • **`strip()`:** Strips characters from **both ends** of the string.
> • **`lstrip()`:** Strips characters from the **left (start)** only.
> • **`rstrip()`:** Strips characters from the **right (end)** only.
> 
> By default, they strip all whitespace characters (spaces, tabs, newlines). If passed an argument (e.g. `s.strip(',.')`), they strip any characters in that set.

---

### Subdeck: `42-Python-Data-Science::Python-0-Starting::ex06`

#### Card 45: ex06 (Comprehensions): What is the general syntax of a list comprehension with filtering, and what is its loop equivalent?
> **Tags:** `ex06 list-comprehension syntax loops`  
>
> **Syntax:** `[expression for item in iterable if condition]`
> 
> **Equivalent loop:**`result = []
for item in iterable:
    if condition:
        result.append(expression)`List comprehensions are generally faster than standard loops because the appending is performed at C-speed in Python's bytecode.

---

#### Card 46: ex06 (Data Science Memory): What is the difference in syntax and memory between [x for x in data] and (x for x in data)?
> **Tags:** `ex06 list-comprehension generator-expression memory data-science`  
>
> • **`[...]` (List Comprehension):** Allocates memory and evaluates **all elements immediately** into a complete list. If `data` has 100M items, this may crash RAM.
> • **`(...)` (Generator Expression):** Does **not** allocate elements in memory upfront. It returns a lazy generator that yields items one by one on-demand ($O(1)$ memory usage).

---

#### Card 47: ex06 (Functional): How does Python's built-in filter(func, iterable) work, and what does passing None as the function do?
> **Tags:** `ex06 filter functional truthiness iterators`  
>
> `filter(func, iterable)` returns a **lazy iterator** that yields only items for which `func(item)` evaluates to truthy.
> 
> • **When `func is None`:** It filters by **truthiness**, dropping all falsy values (`0`, `False`, `''`, `None`).
> • In Python 3, `filter()` returns an iterator; convert to list with `list(filter(...))`.

---

#### Card 48: ex06 (Lambdas): What is a lambda in Python, what is its syntax, and what are its strict limitations?
> **Tags:** `ex06 lambda functional functions`  
>
> A `lambda` is an anonymous, inline function.
> 
> **Syntax:** `lambda arg1, arg2: expression`
> 
> **Limitations:**
> 1. Can only contain a **single expression**; no statements (no `if/else` statements without ternary, no `return`, no loops).
> 2. It implicitly returns the result of the expression.
> 3. Intended for short, disposable helper functions passed to higher-order functions like `sorted()`, `map()`, or `filter()`.

---

#### Card 49: ex06 (Functional): How do you sort a list of dictionaries by a specific key using sorted() and a lambda?
> **Tags:** `ex06 sorted lambda functional sorting`  
>
> Pass a lambda to the **`key`** parameter of `sorted()`:
> `users = [
    {'name': 'Alice', 'age': 30},
    {'name': 'Bob', 'age': 25}
]
sorted_users = sorted(users, key=lambda u: u['age'])`The lambda extracts the comparison value for each element. To sort descending, add `reverse=True`.

---

#### Card 50: ex06 (Style &amp; Lints): Why does PEP 8 (flake8 error E731) forbid assigning a lambda to a variable (e.g. f = lambda x: x * 2)?
> **Tags:** `ex06 lambda pep8 flake8 e731 style`  
>
> Because assigning a lambda defeats the purpose of an anonymous function and damages debugging!
> 
> 1. A named function defined with `def f(x):` has `f.__name__ == 'f'`, which appears cleanly in tracebacks and error messages.
> 2. A lambda's `__name__` is always `'&lt;lambda&gt;'`, making debugging tracebacks ambiguous.
> 
> Always use `def` for named functions; keep lambdas inline.

---

#### Card 51: ex06 (Strings): How does str.split() (no argument) differ from str.split(' ') (with a space)?
> **Tags:** `ex06 strings split whitespace gotchas`  
>
> • **`s.split()` (Default):** Treats any consecutive sequence of whitespace (spaces, tabs, newlines) as a single delimiter, and automatically strips leading/trailing whitespace. Never returns empty strings.
> • **`s.split(' ')`:** Splits strictly on single space characters. Consecutive spaces produce empty string elements `''` in the resulting list.

---

### Subdeck: `42-Python-Data-Science::Python-0-Starting::ex07`

#### Card 52: ex07 (Dictionaries): What data structure powers Python dictionaries, and what is the average time complexity for lookups, insertions, and deletions?
> **Tags:** `ex07 dict hash-table complexity performance`  
>
> Dictionaries are implemented as **hash tables** with open addressing.
> 
> • **Average Time Complexity:** **$O(1)$ constant time** for lookup, insertion, and deletion.
> • Python hashes the key using `hash(key)` to locate its bucket in the table.
> 
> This is why dictionary lookups are vastly superior to linear scans ($O(N)$) through lists or if/elif chains.

---

#### Card 53: ex07 (Dictionaries): What happens if you access a missing key using d['missing'] vs d.get('missing', default)?
> **Tags:** `ex07 dict get keyerror safe-access`  
>
> • **`d['missing']`:** Raises an unhandled **`KeyError`**.
> • **`d.get('missing', default)`:** Returns the `default` value (or `None` if omitted) without raising an error.
> 
> Use `d.get()` whenever keys may be absent and you want a clean fallback.

---

#### Card 54: ex07 (Dictionaries): How do you iterate through both keys and values of a dictionary simultaneously?
> **Tags:** `ex07 dict items iteration`  
>
> Use the **`.items()`** method with tuple unpacking:
> `for key, value in my_dict.items():
    print(f"{key}: {value}")`• `my_dict.keys()` iterates keys only (same as `for k in my_dict:`).
> • `my_dict.values()` iterates values only.

---

#### Card 55: ex07 (Performance): Why is s += char in a loop an $O(N^2)$ anti-pattern, and why is ''.join(list) $O(N)$?
> **Tags:** `ex07 strings join immutability complexity performance`  
>
> Because Python strings are **immutable**:
> • `s += char` allocates a new string and copies all previous characters over and over on every iteration, leading to **quadratic $O(N^2)$ time**.
> • **`''.join(iterable)`:** Pre-calculates the exact total memory required for the final string in a single pass, allocates the buffer once, and copies all elements at C-speed in **linear $O(N)$ time**.

---

#### Card 56: ex07 (Dictionaries): Why must string keys be normalized (e.g. .upper() or .lower()) when performing dictionary lookups?
> **Tags:** `ex07 dict normalization case-sensitive strings`  
>
> Dictionary string hashing is strictly **case-sensitive**:
> `'A'` and `'a'` have completely different hash values.
> 
> If a dictionary has uppercase keys (`{'SOS': '...'}`), looking up `'sos'` raises `KeyError`. Always normalize input before lookup: `key = user_input.strip().upper()`.

---

#### Card 57: ex07 (Comprehensions): How do you write a dictionary comprehension in Python, and how do you invert a dictionary's keys and values?
> **Tags:** `ex07 dict-comprehension syntax dictionary`  
>
> **Syntax:** `{key_expr: value_expr for item in iterable}`
> 
> **Inverting a dictionary (swapping keys and values):**
> `original = {'a': 1, 'b': 2}
inverted = {v: k for k, v in original.items()}  # {1: 'a', 2: 'b'}`*Note:* Inverting requires all values in the original dict to be unique and hashable!

---

#### Card 58: ex07 (Data Structures): What is collections.defaultdict and how does it prevent KeyError when grouping data?
> **Tags:** `ex07 collections defaultdict standard-library`  
>
> A `defaultdict` automatically initializes missing keys with a default factory function (such as `list`, `int`, or `set`):
> `from collections import defaultdict

groups = defaultdict(list)
# No need to check 'if key not in groups:'
groups['fruits'].append('apple')`If a key is accessed for the first time, `defaultdict` invokes `list()` to create an empty list and returns it.

---

### Subdeck: `42-Python-Data-Science::Python-0-Starting::ex08`

#### Card 59: ex08 (Generators): What is the difference between return and yield in a Python function?
> **Tags:** `ex08 generators yield return functions`  
>
> • **`return`:** Terminates function execution completely and passes a single value back to the caller.
> • **`yield`:** Pauses function execution, saves all local variables and execution frame state, and yields a value to the caller. When the caller asks for the next value, execution resumes immediately after the `yield` statement.
> 
> Any function containing `yield` is a **generator function**.

---

#### Card 60: ex08 (Data Science): What is lazy evaluation and why is it essential when processing large datasets?
> **Tags:** `ex08 generators lazy-evaluation memory data-science`  
>
> Lazy evaluation means values are **computed on-demand one at a time**, rather than all at once in memory upfront.
> 
> **Why it matters:** When training machine learning models or analyzing datasets that exceed physical RAM (e.g. 100GB of video, logs, or genomic data), generators stream data item-by-item or batch-by-batch in $O(1)$ memory instead of causing an Out-Of-Memory (OOM) crash.

---

#### Card 61: ex08 (Iterators): What is the difference between an Iterable and an Iterator in Python?
> **Tags:** `ex08 iterators iter next iterator-protocol`  
>
> • **Iterable:** Any object you can loop over (lists, tuples, dicts, strings). Implements `__iter__()` which returns an iterator.
> • **Iterator:** The stateful object that produces the sequence of values. Implements `__next__()` (returns next item or raises `StopIteration` when finished) and `__iter__()` (returns self).

---

#### Card 62: ex08 (Generators): Can you iterate over the same generator instance twice? What happens if you try?
> **Tags:** `ex08 generators exhaustion gotchas`  
>
> **No. Generators are single-use streams.**
> 
> Once a generator yields its final value and raises `StopIteration`, it is **exhausted**. Iterating over it a second time immediately yields nothing:
> `g = (x for x in range(3))
list(g)  # [0, 1, 2]
list(g)  # [] (empty!)`To iterate again, you must construct a fresh generator instance.

---

#### Card 63: ex08 (Terminal I/O): How does print(..., end='\r', flush=True) update a progress bar in-place on a single terminal line?
> **Tags:** `ex08 terminal-ui carriage-return flush io`  
>
> • **`\r` (Carriage Return):** Moves the terminal cursor back to the beginning of the current line without advancing down to a new line.
> • **`flush=True`:** Forces Python to flush the stdout buffer immediately to the screen. By default, terminal output is line-buffered (waits for `\n`). Without `flush=True`, live updates appear delayed or all at once.

---

#### Card 64: ex08 (System): How do you get terminal width in Python, and why must you wrap it in a try...except OSError?
> **Tags:** `ex08 os terminal-size exceptions cli`  
>
> Use **`os.get_terminal_size().columns`**.
> 
> **The Trap:** If output is redirected to a file, piped to another process (`| cat`), or executed in CI/headless environments, stdout is not a TTY terminal and `os.get_terminal_size()` raises **`OSError`**.
> 
> Always provide a fallback:
> `import os
try:
    cols = os.get_terminal_size().columns
except OSError:
    cols = 80  # Default fallback width`

---

#### Card 65: ex08 (Benchmarking): Why should you use time.perf_counter() instead of time.time() when measuring code execution speed?
> **Tags:** `ex08 time benchmarking perf-counter performance`  
>
> • **`time.perf_counter()`:** A **monotonic clock** designed specifically for benchmarking. It has nanosecond resolution and **cannot go backwards**.
> • **`time.time()`:** Reads system wall-clock time. If system time is adjusted (e.g. NTP synchronization or daylight saving), `time.time()` can jump backwards or forwards, producing inaccurate or negative durations.

---

#### Card 66: ex08 (Generators): How can a generator function produce an infinite sequence (e.g. streaming sensor data) without crashing memory?
> **Tags:** `ex08 generators infinite-series streaming memory`  
>
> Because generator execution is paused at each `yield`, an infinite loop consumes **$O(1)$ constant memory**:
> `def infinite_counter():
    n = 0
    while True:
        yield n
        n += 1`Values are only generated when requested by `next()`. Python does not pre-compute the infinite series.

---

### Subdeck: `42-Python-Data-Science::Python-0-Starting::ex09`

#### Card 67: ex09 (Packaging): What file makes a folder an importable Python package, and what is its role?
> **Tags:** `ex09 packaging init modules packages`  
>
> An **`__init__.py`** file.
> 
> • It tells Python that the directory should be treated as a regular package.
> • It executes automatically when the package is imported.
> • It defines the package's public API by importing and exposing functions, and setting **`__all__`**.

---

#### Card 68: ex09 (Project Architecture): What is the difference between a project's root directory and the package directory?
> **Tags:** `ex09 packaging project-structure architecture`  
>
> • **Project Root:** The top-level repository directory. Contains configuration files (`pyproject.toml`), documentation (`README.md`), tests, and license files.
> • **Package Directory:** The subdirectory (e.g. `my_package/`) containing `__init__.py` and the actual importable Python source code.

---

#### Card 69: ex09 (Packaging): What is pyproject.toml and what are its two core tables in modern Python packaging?
> **Tags:** `ex09 packaging pyproject-toml pep517 pep621`  
>
> `pyproject.toml` is the modern declarative configuration file for building and packaging Python projects (PEP 517/518/621).
> 
> 1. **`[build-system]`:** Declares the build engine (e.g. `requires = ["setuptools>=61.0"]`, `build-backend = "setuptools.build_meta"`).
> 2. **`[project]`:** Declares package metadata (`name`, `version`, `description`, `dependencies`).

---

#### Card 70: ex09 (Packaging): What is the difference between a Source Distribution (.tar.gz) and a Wheel (.whl)?
> **Tags:** `ex09 packaging wheel sdist pip`  
>
> • **Source Distribution (sdist, `.tar.gz`):** Uncompiled source code and build configs. When installed via pip, the user's machine must execute a build backend to compile and package it.
> • **Wheel (bdist_wheel, `.whl`):** A ready-to-use, pre-built distribution format. `pip` installs wheels by simply extracting them into `site-packages`. Wheels install vastly faster and require no build tools or C compilers.

---

#### Card 71: ex09 (Development Workflow): What does pip install -e . do, and why is it essential during package development?
> **Tags:** `ex09 pip editable-mode packaging development`  
>
> It installs the package in **editable (development) mode**.
> 
> Instead of copying files to `site-packages`, pip adds a reference (or `.pth` link) to your local source code directory. Any edits you make to the code are **immediately active without needing to rebuild or reinstall**!

---

#### Card 72: ex09 (Environments): Why are Python virtual environments (venv) essential, and where are packages installed inside them?
> **Tags:** `ex09 venv virtual-environments pip site-packages`  
>
> **Why:** Different projects often require different, conflicting versions of libraries. A virtual environment isolates dependencies per project, preventing conflicts and avoiding polluting the system-wide Python.
> 
> **Location:** Packages installed via pip inside a venv are stored in: `&lt;venv_dir&gt;/lib/python3.X/site-packages/`.

---

#### Card 73: ex09 (Modules): What is the purpose of defining __all__ = ['func1', 'Class2'] in a module or __init__.py?
> **Tags:** `ex09 init all packaging public-api flake8`  
>
> 1. **Controls wild-card imports:** Dictates exactly which symbols are imported when a user runs `from my_package import *`.
> 2. **Declares public API:** Explicitly communicates to developers and IDEs which functions are intended for external use.
> 3. **Linters:** Prevents linters (like flake8 `F401`) from complaining about unused re-exports.

---

#### Card 74: ex09 (Modules): What is the difference between an absolute import and a relative import, and when do relative imports fail?
> **Tags:** `ex09 imports relative-imports modules packaging`  
>
> • **Absolute:** `from mypackage.module import func`. Resolves from the project root or `sys.path`. Unambiguous and preferred by PEP 8.
> • **Relative:** `from .module import func`. Resolves relative to the current module's position in the package hierarchy.
> 
> *Trap:* Relative imports fail with `ImportError: attempted relative import with no known parent package` if you try to run the file directly as a script (`python file.py`).

---
