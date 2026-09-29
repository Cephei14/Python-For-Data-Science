# Study Tutorial — Exercise 09: My First Package Creation

## 1. Exercise Overview

**What it asks:**
Turn your own Python code into a real, installable package named `ft_package`.
- When installed, the command `pip list` must show `ft_package`.
- The command `pip show -v ft_package` must display all its package metadata (Name, Version, Summary, Author, License, etc.).
- Both installation files must be built inside a `dist/` folder:
  1. `pip install ./dist/ft_package-0.0.1.tar.gz`
  2. `pip install ./dist/ft_package-0.0.1-py3-none-any.whl`
- Once installed, any Python program anywhere can import and run your code:
  ```python
  from ft_package import count_in_list

  print(count_in_list(["toto", "tata", "toto"], "toto"))  # 2
  print(count_in_list(["toto", "tata", "toto"], "tutu"))  # 0
  ```

**Files to submit:**
`*.py`, `*.toml`, `*.txt`, `README.md`, `LICENSE` (plus your `dist/` artifacts).

**Main concepts you'll learn:**
- The anatomy of a Python package (`__init__.py`).
- Modern packaging configuration using `pyproject.toml`.
- Source distributions (`.tar.gz`) vs Wheels (`.whl`).
- Building packages with the `build` tool and managing them with `pip`.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **Lists & Equality (ex00):** Finding matching elements in a list.
- **Importing Modules (ex01, ex02):** Using `import ...` and `from ... import ...`.
- **Functions & Docstrings (ex02, ex05):** Defining clear, documented functions.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `pyproject.toml` | The standard configuration file containing package metadata | Modern Python standard (PEP 517/518/621) |
| `__init__.py` | Marks a folder as an importable Python package | Exposes `count_in_list` at the package root |
| `python -m build` | Compiles your project into a `.tar.gz` and `.whl` in `dist/` | Requires `pip install build` |
| `pip install ./dist/...` | Installs your built package into your Python environment | Tested by evaluators |
| `pip show -v ft_package` | Displays installed package metadata | Evaluator checks this exact output |

Common pitfalls:
- Missing `__init__.py`: Without `__init__.py`, Python cannot treat the folder as a package.
- Field mismatch in metadata: If `Author`, `License`, or `Home-page` are missing from `pyproject.toml`, `pip show -v` will display empty values and fail the grading check.
- Not exposing `count_in_list` in `__init__.py`: If `__init__.py` is empty, users would have to write `from ft_package.core import count_in_list` instead of `from ft_package import count_in_list`.

---

## 4. Concepts You Need to Learn

### 4.1 Script vs. Module vs. Package

- **Script:** A standalone `.py` file run directly (`python whatis.py`).
- **Module:** A `.py` file imported by another file (`from find_ft_type import ...`).
- **Package:** A **directory** containing an `__init__.py` file and one or more modules that can be distributed and installed globally.

### 4.2 Project Folder Structure

A standard Python package project layout looks like this:

```
ex09/
├── pyproject.toml         <-- Package configuration & metadata
├── README.md              <-- Project documentation
├── LICENSE                <-- License file (e.g. MIT)
└── ft_package/            <-- The importable package folder
    ├── __init__.py        <-- Package initialization & public exports
    └── core.py            <-- Contains count_in_list()
```

### 4.3 Implementing `count_in_list`

The function must count how many times a target item appears in a list:
```python
def count_in_list(lst: list, item: str) -> int:
    """Count occurrences of an item within a list."""
    count = 0
    for elem in lst:
        if elem == item:
            count += 1
    return count
```
*(Or simply: `return lst.count(item)`).*

To make this function importable directly as `from ft_package import count_in_list`, expose it inside `ft_package/__init__.py`:
```python
# ft_package/__init__.py
from .core import count_in_list

__all__ = ["count_in_list"]
```
The `.` before `core` is a **relative import**, meaning *"import from the `core.py` module located in this same folder"*.

### 4.4 Configuring `pyproject.toml`

The `pyproject.toml` file tells build tools who made the package, its version, and what license it uses. Each field maps directly to `pip show -v`:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "ft_package"
version = "0.0.1"
authors = [
  { name = "eagle", email = "eagle@42.fr" },
]
description = "A sample test package"
readme = "README.md"
license = { text = "MIT" }
classifiers = []

[project.urls]
Homepage = "https://github.com/eagle/ft_package"
```

Notice how these fields match the subject's expected output:
- `name = "ft_package"` $\rightarrow$ `Name: ft_package`
- `version = "0.0.1"` $\rightarrow$ `Version: 0.0.1`
- `description = "A sample test package"` $\rightarrow$ `Summary: A sample test package`
- `authors` $\rightarrow$ `Author: eagle` and `Author-email: eagle@42.fr`
- `Homepage` $\rightarrow$ `Home-page: https://github.com/eagle/ft_package`
- `license = { text = "MIT" }` $\rightarrow$ `License: MIT`

### 4.5 Source Distributions (`.tar.gz`) vs. Wheels (`.whl`)

When you build a package, Python creates two files in the `dist/` directory:
1. **`.tar.gz` (Source Distribution / sdist):** A compressed archive of the original source files.
2. **`.whl` (Wheel):** A pre-packaged, ready-to-install binary format that `pip` can install instantly.

The subject requires **both** formats to exist and be installable.

---

## 5. Syntax and Step-by-Step Build Workflow

### Step 1: Install the Build Tool
Make sure `build` is installed in your virtual environment:
```bash
pip install build
```

### Step 2: Build the Distributions
From inside the `ex09/` directory (where `pyproject.toml` is located), run:
```bash
python -m build
```
This generates a `dist/` folder containing:
- `dist/ft_package-0.0.1.tar.gz`
- `dist/ft_package-0.0.1-py3-none-any.whl`

### Step 3: Test Installation with `pip`
Test installing from the `.tar.gz`:
```bash
pip install ./dist/ft_package-0.0.1.tar.gz
```

Verify metadata:
```bash
pip show -v ft_package
```

### Step 4: Test in Python
Run Python and test the import:
```bash
python -c 'from ft_package import count_in_list; print(count_in_list(["toto", "tata", "toto"], "toto"))'
# Output: 2
```

---

## 6. How to Think About the Exercise

1. **Write the core logic first:**
   - Create `ft_package/core.py` with `count_in_list` and its docstring.
   - Create `ft_package/__init__.py` and re-export `count_in_list`.
2. **Create documentation & licensing files:**
   - Create a minimal `README.md` and `LICENSE`.
3. **Write `pyproject.toml`:**
   - Carefully copy the author, email, summary, version, and homepage from the subject.
4. **Build artifacts:**
   - Run `python -m build` to populate `dist/`.
5. **Verify with pip:**
   - Install via `pip install ./dist/...`, run `pip show -v ft_package`, and test the function.

---

## 7. Guided Practice

Unlike the previous exercises, this one isn't about algorithmic difficulty — it's
about assembling a project correctly, piece by piece. These five drills follow the
natural build order (easiest/most familiar first), ending with a fully installed,
verified package.

**Practice 1 (Easiest — the function itself, nothing package-related yet):**
Write `count_in_list(lst, item)` with a docstring, exactly as it will live in
`core.py`. This only reuses what you already know from ex00/ex02 — no packaging
concepts yet.

Expected output:

```python
print(count_in_list(["toto", "tata", "toto"], "toto"))  # 2
print(count_in_list(["toto", "tata", "toto"], "tutu"))  # 0
```

<details><summary>Solution</summary>

```python
def count_in_list(lst: list, item: str) -> int:
    """Count occurrences of item in list."""
    return lst.count(item)
```
</details>

**Practice 2 (Expose it through `__init__.py`):**
Given a folder `mypkg/` containing `__init__.py` and `math_tools.py` with
`def add(a, b): return a + b`, write the line(s) needed inside `__init__.py` so
that `from mypkg import add` works directly, instead of
`from mypkg.math_tools import add`.

Expected behavior:

```python
from mypkg import add
print(add(2, 3))  # 5
```

<details><summary>Solution</summary>

Inside `mypkg/__init__.py`:
```python
from .math_tools import add

__all__ = ["add"]
```
</details>

**Practice 3 (Apply Practice 2 to `ft_package`):**
Now do exactly the same thing for your real project: create
`ft_package/__init__.py` that re-exports `count_in_list` from `ft_package/core.py`
(the function you wrote in Practice 1).

Expected behavior once both files exist side by side:

```python
from ft_package import count_in_list
print(count_in_list(["toto", "tata", "toto"], "toto"))  # 2
```

<details><summary>Solution</summary>

```
ft_package/
├── __init__.py
└── core.py
```

`ft_package/core.py`:
```python
def count_in_list(lst: list, item: str) -> int:
    """Count occurrences of item in list."""
    return lst.count(item)
```

`ft_package/__init__.py`:
```python
from .core import count_in_list

__all__ = ["count_in_list"]
```
</details>

**Practice 4 (Write the metadata that `pip show` will display):**
Write a minimal `pyproject.toml` with just enough fields so that
`pip show -v ft_package` displays the six pieces of metadata the subject checks:
Name, Version, Summary, Home-page, Author, Author-email, and License.

Expected output once built and installed (see Practice 5):

```
Name: ft_package
Version: 0.0.1
Summary: A sample test package
Home-page: https://github.com/eagle/ft_package
Author: eagle
Author-email: eagle@42.fr
License: MIT
```

<details><summary>Solution</summary>

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "ft_package"
version = "0.0.1"
authors = [
  { name = "eagle", email = "eagle@42.fr" },
]
description = "A sample test package"
readme = "README.md"
license = { text = "MIT" }
classifiers = []

[project.urls]
Homepage = "https://github.com/eagle/ft_package"
```
</details>

**Practice 5 (Hardest — build, install, and verify the whole thing):**
With `core.py`, `__init__.py`, and `pyproject.toml` from Practices 1–4 in place
(plus a minimal `README.md` and `LICENSE`), run the actual build-and-install
workflow from section 5 and confirm every check the subject cares about.

Expected results — check all four:

| Command | Expected result |
|---|---|
| `python -m build` | creates `dist/ft_package-0.0.1.tar.gz` and `dist/ft_package-0.0.1-py3-none-any.whl` |
| `pip install ./dist/ft_package-0.0.1.tar.gz` | installs without errors |
| `pip show -v ft_package` | prints the metadata block from Practice 4 |
| `python -c 'from ft_package import count_in_list; print(count_in_list(["toto","tata","toto"], "toto"))'` | prints `2` |

<details><summary>Solution</summary>

Final project layout:
```
ex09/
├── LICENSE
├── README.md
├── pyproject.toml
└── ft_package/
    ├── __init__.py
    └── core.py
```

Build and verify:
```bash
pip install build
python -m build
pip install ./dist/ft_package-0.0.1.tar.gz
pip show -v ft_package
pip list | grep ft_package
python -c 'from ft_package import count_in_list; print(count_in_list(["toto", "tata", "toto"], "toto"))'
```

If you want to double-check the wheel installs too:
```bash
pip uninstall -y ft_package
pip install ./dist/ft_package-0.0.1-py3-none-any.whl
pip show -v ft_package
```
</details>

If all four Practice 5 checks pass, your `ex09/` submission is complete.

---

## 8. Exercise-Specific Knowledge

- **Exact Subject Metadata Check:**
  Running `pip show -v ft_package` should display:
  ```
  Name: ft_package
  Version: 0.0.1
  Summary: A sample test package
  Home-page: https://github.com/eagle/ft_package
  Author: eagle
  Author-email: eagle@42.fr
  License: MIT
  ```
- **Both formats must install:**
  Test uninstalling with `pip uninstall -y ft_package` and reinstalling with the `.whl` file to verify both formats succeed.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `ImportError: cannot import name 'count_in_list'` | `__init__.py` is empty | Add `from .core import count_in_list` to `__init__.py` |
| `pip show -v` shows blank `Summary` | Missing `description` in `[project]` | Set `description = "A sample test package"` in `pyproject.toml` |
| Missing `dist/` files | Forgot to run `python -m build` | Run `python -m build` inside `ex09/` |
| Files outside project root | Running build from wrong folder | Run `python -m build` in the folder containing `pyproject.toml` |

---

## 10. Debugging Guide

- **`ERROR: Package 'ft_package' requires a different Python`**: Check that your `pyproject.toml` does not specify an incompatible `requires-python` version.
- **`WARNING: No files were found in ...` during build**: Ensure your package folder `ft_package/` has an `__init__.py` so setuptools discovers it automatically.

---

## 11. Cheat Sheet

### Directory Structure
```
ex09/
├── LICENSE
├── README.md
├── pyproject.toml
└── ft_package/
    ├── __init__.py
    └── core.py
```

### `ft_package/core.py`
```python
def count_in_list(lst: list, item: str) -> int:
    """Count occurrences of item in list."""
    return lst.count(item)
```

### `ft_package/__init__.py`
```python
from .core import count_in_list

__all__ = ["count_in_list"]
```

### Build & Verify Commands
```bash
python -m build
pip install ./dist/ft_package-0.0.1.tar.gz
pip show -v ft_package
pip list | grep ft_package
```

---

## 12. Knowledge Checklist

- [ ] I can describe the directory layout of an installable Python package.
- [ ] I understand the purpose of `__init__.py` and relative imports.
- [ ] I can configure `pyproject.toml` with accurate metadata.
- [ ] I can build both `.tar.gz` and `.whl` artifacts using `python -m build`.
- [ ] I have verified that `pip show -v ft_package` matches the subject's requirements.
