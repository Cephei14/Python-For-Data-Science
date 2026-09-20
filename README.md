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

## Track-wide rules

These apply to every module: Python 3.10, explicit imports only (`import numpy as np`, never `from x import *`), no global variables, and every function must have a docstring (`__doc__`). Code must pass `flake8` (aliased as `norminette`).

The `main()` + `if __name__ == "__main__":` requirement is **not** identical across modules — see each module's notes below.

---

## Module 0 — Starting: Exercise Breakdown

The `main()`-guard requirement kicks in from **Exercise 05 onward**; ex00–ex04 may run as flat scripts.

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
- [ ] `main()` + `if __name__ == "__main__":` present (ex05 onward — see Track-wide rules)
- [ ] All functions have docstrings
- [ ] Passes `flake8` (aliased as `norminette`)
- [ ] No global variables

---

## Module 1 — Array: Exercise Breakdown

Unlike Module 0, the `main()`-guard requirement applies from **Exercise 00** — every program in this module must be structured with `main()` + `if __name__ == "__main__":` from the start. All functions still need docstrings and must pass `flake8`.

| Ex | Directory | File(s) to turn in | Goal |
| :--- | :--- | :--- | :--- |
| 00 | `ex00/` | `give_bmi.py` | `give_bmi(height, weight) -> list`: pairwise BMI from two lists. `apply_limit(bmi, limit) -> list[bool]`: mask of values above a threshold. Handles mismatched sizes/types. |
| 01 | `ex01/` | `array2D.py` | `slice_me(family, start, end) -> list`: prints the shape of a 2D array, returns a slice of it using Python slicing (including negative indices). |
| 02 | `ex02/` | `load_image.py` | `ft_load(path) -> array`: loads a JPG/JPEG image into an array, prints its shape and pixel content, with clear error handling. |
| 03 | `ex03/` | `load_image.py`, `zoom.py` | Loads `animal.jpeg`, prints size/channels/pixel data, crops ("zooms") a region via multi-axis slicing, and displays it with axis scales. |
| 04 | `ex04/` | `load_image.py`, `rotate.py` | Crops a square region and **manually transposes** it (no library transpose allowed), printing the new shape/data and displaying the result. |
| 05 | `ex05/` | `load_image.py`, `pimp_image.py` | Five color-filter functions — `ft_invert`, `ft_red`, `ft_green`, `ft_blue`, `ft_grey` — each restricted to a specific operator subset (`=`, `+`, `-`, `*`, `/`), preserving image shape. |

### Progress checklist

- [ ] ex00 — give_bmi.py
- [ ] ex01 — array2D.py
- [ ] ex02 — load_image.py
- [ ] ex03 — load_image.py / zoom.py
- [ ] ex04 — load_image.py / rotate.py
- [ ] ex05 — load_image.py / pimp_image.py

Per-exercise definition of done:
- [ ] Output shape/format matches the subject exactly
- [ ] Bad input (mismatched sizes, wrong types, missing files) is handled with a clear message, not a crash
- [ ] `main()` + `if __name__ == "__main__":` present (from ex00 — see Track-wide rules)
- [ ] All functions have docstrings
- [ ] Passes `flake8` (aliased as `norminette`)
- [ ] No global variables
- [ ] ex04 specifically: transpose implemented manually, no `.T`/`.transpose()`

---

## Getting Started

### Prerequisites

* Python 3.10+
* A package manager (`pip` or `conda`)
* From Module 1 onward: `numpy`, `Pillow`, and `matplotlib` (`pip install numpy Pillow matplotlib`)

### Installation

```bash
git clone https://github.com/Cephei14/Python-For-Data-Science.git
cd Python-For-Data-Science
pip install flake8
alias norminette=flake8
```

### Running an exercise

Each exercise lives in its own `exXX/` directory under the relevant module folder. Example:

```bash
cd "Python - 0 - Starting/ex00"
python Hello.py | cat -e
```

```bash
cd "Python - 1 - Array/ex02"
python load_image.py
```

---

## License

See [LICENSE](LICENSE) for details.