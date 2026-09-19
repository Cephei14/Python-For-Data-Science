# Python for Data Science

A collection of 5 sequential modules covering core Python mechanics, vectorized numerical computing, data analysis, object-oriented design, and data-oriented architectural patterns.

---

## Overview

This repository contains my solutions for the **Python for Data Science** track following the 42 Common Core. The series transitions from low-level C paradigms to high-level Python abstractions, focusing on writing clean, idiomatic, and performance-aware code for data engineering and analytical pipelines.

---

## Project Structure

| Module | Focus Area | Key Concepts & Technologies |
| :--- | :--- | :--- |
| **Python - 0 - Starting** | Language Fundamentals | Syntax, built-in data structures, error/exception handling, environment configuration, standard library tools. |
| **Python - 1 - Array** | Vectorized Computing | Matrix operations, multidimensional arrays, slicing, numerical optimization, image processing via array representations using **NumPy**. |
| **Python - 2 - DataTable** | Data Analysis & Visualization | Loading CSV/JSON data, indexing, missing data handling, aggregation, plotting trends, and exploratory data analysis using **Pandas**, **Matplotlib**, and **Seaborn**. |
| **Python - 3 - OOP** | Object-Oriented Design | Classes, inheritance, polymorphism, abstract base classes (ABCs), encapsulation, magic/dunder methods (`__init__`, `__str__`, operator overloading). |
| **Python - 4 - DoD** | Data-Oriented Design | Memory efficiency, functional programming, decorators, wrappers, `dataclasses`, and scalable pipeline design patterns. |

---

## Module 0 — Starting: Exercise Breakdown

General rules that apply throughout: Python 3.10, explicit imports only (`import numpy as np`, never `from x import *`), no global variables, and — from Exercise 05 onward — every script must be wrapped in a `main()` guarded by `if __name__ == "__main__":`, with full docstring coverage (`__doc__`) and `flake8` compliance.

| Ex | Directory | File(s) to turn in | Goal |
| :--- | :--- | :--- | :--- |
| 00 | `ex00/` | `Hello.py` | Mutate list/tuple/set/dict in place to print custom "Hello X" greetings. |
| 01 | `ex01/` | `format_ft_time.py` | Use `time`/`datetime` to print seconds since epoch (with commas + scientific notation) and a formatted date string. |
| 02 | `ex02/` | `find_ft_type.py` | `all_thing_is_obj(object) -> int`: print the object's type in a readable sentence, return `42`. No code runs when the file is executed directly. |
| 03 | `ex03/` | `NULL_not_found.py` | `NULL_not_found(object) -> int`: identify all "null-like" values (`None`, `NaN`, `0`, `""`, `False`), return `0`/`1` for success/error. |
| 04 | `ex04/` | `whatis.py` | CLI script: odd/even check on a single int arg via `sys.argv`; `AssertionError` on wrong arg count or non-integer input. |
| 05 | `ex05/` | `building.py` | First real `main()`-based program: count upper/lower/punctuation/space/digit chars in a string arg (or prompt if none given). |
| 06 | `ex06/` | `ft_filter.py`, `filterstring.py` | Part 1: reimplement `filter()` using a list comprehension. Part 2: CLI program filtering words by length, using list comprehension **and** lambda. |
| 07 | `ex07/` | `sos.py` | Encode a string arg into Morse code using a dictionary lookup table. |
| 08 | `ex08/` | `Loading.py` | Reimplement `tqdm`-style progress bar as a generator (`ft_tqdm`) using `yield`. |
| 09 | `ex09/` | `*.py`, `*.txt`, `*.toml`, `README.md`, `LICENSE` | Build and package `ft_package` so it's pip-installable and importable (`pip show -v ft_package` must work). |

### Progress checklist

- [ ] ex00 — Hello.py
- [ ] ex01 — format_ft_time.py
- [ ] ex02 — find_ft_type.py
- [ ] ex03 — NULL_not_found.py
- [ ] ex04 — whatis.py
- [ ] ex05 — building.py
- [ ] ex06 — ft_filter.py / filterstring.py
- [ ] ex07 — sos.py
- [ ] ex08 — Loading.py
- [ ] ex09 — ft_package

Per-exercise definition of done:
- [ ] Output matches the subject exactly (including `cat -e` line-ending checks where specified)
- [ ] Invalid input triggers the correct `AssertionError` message
- [ ] `main()` + `if __name__ == "__main__":` present (ex05 onward)
- [ ] All functions have docstrings
- [ ] Passes `flake8` (aliased as `norminette`)
- [ ] No global variables

---

## Getting Started

### Prerequisites

* Python 3.10+
* A package manager (`pip` or `conda`)

### Running an exercise

Each exercise lives in its own `exXX/` directory under the relevant module folder. Example:

```bash
cd "Python - 0 - Starting/ex00"
python Hello.py | cat -e
```
