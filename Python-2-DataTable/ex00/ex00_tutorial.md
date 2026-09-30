# Study Tutorial — Exercise 00: load_csv.py

## 1. Exercise Overview

**What it asks:**
Create a file `load_csv.py` in directory `ex00/` containing a function `load(path: str)` that:
1. Takes a **path** to a CSV file as argument.
2. Loads the file into a dataset (a `pandas.DataFrame` is the natural choice).
3. **Prints the dimensions** of the dataset: `Loading dataset of dimensions (195, 302)`
4. **Returns** the dataset.
5. Handles error cases (bad path, bad format, empty file...) and **returns `None`** instead of crashing.

**Tester from the subject:**
```python
from load_csv import load

print(load("life_expectancy_years.csv"))
```
```
$> python tester.py
Loading dataset of dimensions (195, 302)
country 1800 1801 1802 1803 ... 2096 2097 2098 2099 2100
Afghanistan 28.2 28.2 28.2 28.2 ... 76.2 76.4 76.5 76.6 76.8
...
```
The subject says the display format is **not restrictive**: any readable display of the dataset is fine.

**Rules and Constraints:**
- Allowed: `pandas` or any library for dataset manipulation.
- **No code in the global scope**, and **no global variables**. Everything goes in functions.
- The program must have a `main()` and the `if __name__ == "__main__":` guard.
- **Any uncaught exception invalidates the exercise**, even for an error you were asked to test.
- Every function needs a docstring (`__doc__`). Code must be `flake8` clean. Python 3.10+.
- Imports must be explicit (no `from pandas import *`: score of 0).

**Main concepts you'll learn:**
- Reading a CSV into a tabular structure with `pandas.read_csv`.
- Reading the dimensions of a table with `.shape`.
- Defensive programming: catching specific exceptions and returning `None`.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **Functions with type hints (Module 0):** `def f(x: str) -> int:`.
- **Exceptions (Module 0):** `try` / `except`, and catching several exception types.
- **Tuples:** a shape like `(195, 302)` is just a tuple `(rows, columns)`.
- **NumPy arrays (Data Science 1):** a DataFrame is conceptually a labelled 2D array.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `import pandas as pd` | Tabular data library | Explicit import only |
| `pd.read_csv(path)` | Reads a CSV file into a DataFrame | Raises exceptions on failure |
| `DataFrame.shape` | Returns `(rows, columns)` | A tuple, prints as `(195, 302)` |
| `try` / `except` | Catches errors | Catch specific types, not a bare `except:` |
| `pd.DataFrame \| None` | Return type annotation | `X \| None` syntax needs Python 3.10+ |

**Common pitfalls:**
- **Letting `read_csv` crash:** a wrong path raises `FileNotFoundError`. If it escapes, the exercise is invalidated.
- **Printing the dimensions even when loading failed:** only print dimensions after a successful load.
- **Returning something other than `None` on failure:** the subject explicitly says `None`.
- **Code in the global scope:** a stray `df = pd.read_csv(...)` at module level breaks the rules.
- **Wildcard import:** `from pandas import *` = score of 0.

---

## 4. Concepts You Need to Learn

### 4.1 What is a dataset / DataFrame?
A DataFrame is a 2D table with labelled rows and columns. For `life_expectancy_years.csv`:
- Each **row** is a country (195 of them).
- Each **column** is either `country` or a year from 1800 to 2100 (301 years, so 302 columns).

So `shape == (195, 302)`: 195 rows, 302 columns.

### 4.2 Reading a CSV
```python
data = pd.read_csv("life_expectancy_years.csv")
print(data.shape)   # (195, 302)
```
`read_csv` uses the first line as column names.

### 4.3 Which errors can happen?
| Situation | Exception raised |
|---|---|
| File does not exist | `FileNotFoundError` (subclass of `OSError`) |
| Path is a directory | `IsADirectoryError` (subclass of `OSError`) |
| No permission | `PermissionError` (subclass of `OSError`) |
| File is empty | `pd.errors.EmptyDataError` (subclass of `ValueError`) |
| Malformed CSV | `pd.errors.ParserError` (subclass of `ValueError`) |
| Binary/garbage file | `UnicodeDecodeError` (subclass of `ValueError`) |
| Path is not a string (e.g. `None`, `42`) | `TypeError` / `ValueError` |

Because of the class hierarchy, `except (OSError, ValueError, TypeError)` covers all of them.

### 4.4 Why return `None`?
The caller (the next exercises) can test `if data is None:` and stop cleanly. The function never crashes; it signals failure through its return value.

---

## 5. Syntax and Examples

### Minimal working version
```python
import pandas as pd

data = pd.read_csv("life_expectancy_years.csv")
print(f"Loading dataset of dimensions {data.shape}")
```
(Fine to experiment with, but **not** valid as a submission: it is global-scope code.)

### Safe version
```python
try:
    data = pd.read_csv(path)
except (OSError, ValueError, TypeError) as error:
    print(f"Error: {error}")
    return None
```

---

## 6. How to Think About the Exercise

1. **Step 1: Define `load(path: str)`** with a docstring and a return annotation `pd.DataFrame | None`.
2. **Step 2: Wrap `pd.read_csv` in `try`/`except`.** On failure, print a clear message and `return None`.
3. **Step 3: Sanity-check the result.** Optionally treat an empty DataFrame as a failure too.
4. **Step 4: Print the dimensions** with `data.shape`, then `return data`.
5. **Step 5: Add `main()`** that tests a good path and a few bad ones (missing file, directory, non-CSV).
6. **Step 6: Run `flake8`** and verify nothing runs at import time.

---

## 7. Guided Practice

**Practice 1 (Easiest — shape of a DataFrame):**
Build a DataFrame from `{"a": [1, 2, 3], "b": [4, 5, 6]}` and print its shape.

Expected output:
```
(3, 2)
```

<details><summary>Solution</summary>

```python
import pandas as pd

df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
print(df.shape)
```
</details>

**Practice 2 (Catching a missing file):**
Write a function that tries `pd.read_csv("nope.csv")` and prints `Error: ...` instead of crashing.

Expected output (message text varies):
```
Error: [Errno 2] No such file or directory: 'nope.csv'
```

<details><summary>Solution</summary>

```python
import pandas as pd


def try_read(path: str) -> None:
    """Try to read a CSV and print the error if it fails."""
    try:
        pd.read_csv(path)
    except OSError as error:
        print(f"Error: {error}")


try_read("nope.csv")
```
</details>

**Practice 3 (Return `None` on error):**
Modify the function so it returns the DataFrame on success and `None` on failure.

Expected behaviour: `try_read("nope.csv") is None` → `True`.

<details><summary>Solution</summary>

```python
import pandas as pd


def try_read(path: str) -> pd.DataFrame | None:
    """Return the DataFrame, or None if the file cannot be read."""
    try:
        return pd.read_csv(path)
    except (OSError, ValueError, TypeError) as error:
        print(f"Error: {error}")
        return None
```
</details>

**Practice 4 (Test the bad-format case):**
Create a file `empty.csv` (0 bytes) and confirm your function returns `None` without crashing.

Expected output:
```
Error: No columns to parse from file
None
```

<details><summary>Solution</summary>

```python
from pathlib import Path

Path("empty.csv").write_text("")
print(try_read("empty.csv"))
```
</details>

**Practice 5 (Hardest — the full, rule-compliant `load_csv.py`):**

Expected output when running `python tester.py`:
```
Loading dataset of dimensions (195, 302)
country 1800 1801 ... 2100
...
```

<details><summary>Solution</summary>

```python
"""Load a CSV file into a pandas DataFrame."""

import pandas as pd


def load(path: str) -> pd.DataFrame | None:
    """Load a CSV file, print its dimensions and return the dataset.

    Args:
        path: Path to the CSV file.

    Returns:
        The loaded DataFrame, or None if the path is bad or the
        content is not a valid CSV.
    """
    try:
        data = pd.read_csv(path)
    except (OSError, ValueError, TypeError) as error:
        print(f"Error: {error}")
        return None
    if data.empty:
        print("Error: the dataset is empty.")
        return None
    print(f"Loading dataset of dimensions {data.shape}")
    return data


def main() -> None:
    """Test the load function on good and bad inputs."""
    try:
        print(load("life_expectancy_years.csv"))
        print(load("does_not_exist.csv"))
        print(load("."))
        print(load(None))
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()
```
</details>

---

## 8. Exercise-Specific Knowledge

- **Every later exercise reuses this file.** ex01, ex02 and ex03 all list `load_csv.py` as a file to turn in, so keep it identical across folders.
- **`shape` is (rows, columns).** 195 countries × (1 + 301 years) = `(195, 302)`.
- **The `country` column** is a normal column, not the index. Later exercises filter with `data["country"] == "France"`.
- **Not every file has the same shape.** Other Gapminder files will print different dimensions; that is expected.
- **Wrong-path test during evaluation:** expect the evaluator to pass a bad path. You must print a message and return `None`, never a traceback.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Traceback on a bad path | No `try`/`except` | Wrap `read_csv` and return `None` |
| Bare `except:` | Lazy catch-all | Catch `(OSError, ValueError, TypeError)` |
| Top-level `df = pd.read_csv(...)` | Scripting habit | Move everything inside functions |
| Printing dimensions before the load | Wrong order | Print after a successful `read_csv` only |
| `from pandas import *` | Shortcut | `import pandas as pd` |
| Missing docstring | Forgetting | Add one to `load` **and** `main` |

---

## 10. Debugging Guide

- **`FileNotFoundError` traceback:** the CSV is not in the current directory, or you ran the tester from another folder. Check `pwd` and the file name.
- **`ModuleNotFoundError: pandas`:** run `pip install pandas`.
- **Shape is `(195, 1)`:** wrong delimiter; check the file really is comma-separated.
- **`flake8` complains `E501`:** line longer than 79 characters; wrap it.
- **`flake8` complains `F401`:** unused import; remove it.

---

## 11. Cheat Sheet

```python
import pandas as pd


def load(path: str) -> pd.DataFrame | None:
    """Load a CSV, print dimensions, return it (None on error)."""
    try:
        data = pd.read_csv(path)
    except (OSError, ValueError, TypeError) as error:
        print(f"Error: {error}")
        return None
    print(f"Loading dataset of dimensions {data.shape}")
    return data
```

---

## 12. Knowledge Checklist

- [ ] `load(path)` prints `Loading dataset of dimensions (rows, cols)` and returns the dataset.
- [ ] A bad path, a directory, an empty file and a non-CSV file all return `None` with no traceback.
- [ ] No global variables, no code in the global scope, explicit imports only.
- [ ] `main()` exists, is guarded by `if __name__ == "__main__":`, and catches exceptions.
- [ ] All functions have docstrings and the file passes `flake8`.
