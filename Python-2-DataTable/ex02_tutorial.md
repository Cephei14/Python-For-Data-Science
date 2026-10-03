# Study Tutorial — Exercise 02: aff_pop.py

## 1. Exercise Overview

**What it asks:**
Create a program `aff_pop.py` (along with `load_csv.py`) in directory `ex02/` that:
1. Calls the `load` function from ex00.
2. Loads `population_total.csv`.
3. Plots the population of **your campus's country** versus **another country of your choice**, on the same graph.
4. Displays the years **from 1800 to 2050** only.
5. The graph must have a **title**, a **label on each axis** and a **legend for each curve**.

The subject's example: France (green) vs Belgium (blue), title `Population Projections`, x-axis `Year`, y-axis `Population` with ticks such as `20M`, `40M`, `60M`, and a legend in the bottom-right corner.

**Rules and Constraints:**
- Files to turn in: `load_csv.py`, `aff_pop.py`.
- Allowed: `matplotlib`, `seaborn` or any data-visualization library.
- No code in the global scope, no global variables, `main()` with error handling.
- Uncaught exceptions invalidate the exercise (including `NameError`, `IndexError`, `KeyError`...).
- Docstrings on every function, `flake8` clean (no unused variables, no missing final newline), explicit imports, Python 3.10+.

**What makes this exercise tricky (real-data problems):**
- Population cells can be **text** with a suffix, like `"28.4M"` or `"500k"`, instead of plain numbers.
- The file goes up to **2100**, but only **1800 to 2050** must be shown.
- You need **two curves** on the same graph, each with its own legend entry.
- `load()` can return `None`, and a country name can be missing from the file: the code must not crash.

**Main concepts you'll learn:**
- Converting text values such as `"28.4M"` into numbers (`decode`).
- Selecting rows **and** a range of columns at once with `.loc`.
- Looping over several countries and storing the results in a dictionary.
- Drawing several labelled curves and a legend on the same axes.
- Custom tick formatting with `EngFormatter` (`20M` instead of `20000000`).
- Safe error handling: checking for `None`, checking for a missing country, leaving early with `return`.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **`load()` from ex00:** returns a DataFrame or `None`.
- **Country extraction from ex01:** a mask `data["country"] == "Japan"` and `data[mask]`, `.empty`, `.iloc[0]`.
- **Line charts (ex01):** `plt.plot(x, y)`, `plt.title`, `plt.xlabel`, `plt.ylabel`, `plt.show`.
- **String handling (Module 0):** slicing (`text[-1]`, `text[:-1]`), dictionaries, `float()`.
- **`try/except` and `isinstance`** basics.

Everything else used below (`.loc` with a column range, `.columns`, `.items()`, `label=`, `plt.legend`, `plt.gca`, `EngFormatter`, ...) is explained in section 4.

---

## 3. Tools and Libraries

| Tool / Syntax | What it does | Scope / Notes |
|---|---|---|
| `from load_csv import load` | Loads a CSV safely | Same file as ex00; returns a DataFrame or `None` |
| `import matplotlib.pyplot as plt` | Plotting library | Explicit import |
| `from matplotlib.ticker import EngFormatter` | Formatter that writes `20000000` as `20M` | Explicit import; applied on the y-axis |
| `data is None` | Checks that `load` failed | Use `is None`; check it **before** using the DataFrame |
| `data["country"] == "Japan"` | Creates a boolean mask | Series of `True`/`False`, one per row |
| `data[mask]` | Filters rows by a mask | Keeps rows where the mask is `True` |
| `data.loc[mask, "1800":"2050"]` | Selects rows **and** a range of columns at once | Label-based; the column slice is **inclusive** on both ends |
| `row.empty` | Checks if a DataFrame has 0 rows | `True` if the country was not found |
| `row.iloc[0]` | Selects the first row by position | Returns a `pd.Series` (one value per year) |
| `row.columns` | The column names of a DataFrame | Here: the years as strings (`"1800"`, `"1801"`, ...) |
| `int(col)` | Converts the string `"1800"` to the integer `1800` | Needed for a numeric x-axis |
| `[f(v) for v in values]` | List comprehension | Builds a list by applying `f` to each value |
| `for country in ("Japan", "Morocco"):` | Loops over a tuple of names | Same code runs once per country |
| `curves = {}` / `curves[country] = ...` | Dictionary of results | Maps a country name to its list of values |
| `curves.items()` | Iterates over (key, value) pairs | `for country, values in curves.items():` |
| `isinstance(v, (int, float))` | Checks the type of a value | `True` if `v` is already a number |
| `text.strip()` | Removes spaces at both ends | `" 28.4M "` becomes `"28.4M"` |
| `text[-1]` / `text[:-1]` | Last character / everything except the last | `"28.4M"[-1]` is `"M"`, `"28.4M"[:-1]` is `"28.4"` |
| `float("nan")` | Creates a "not a number" value | Returned by `decode` for invalid text |
| `except KeyError as e` | Catches a missing column / key | `e` holds the missing name |
| `return` (inside `main`) | Leaves the function immediately | Stops the program cleanly after an error message |
| `plt.plot(x, y, label="Japan")` | Draws a line connecting coordinates | `x` and `y` must have equal length; `label` is the legend text |
| `plt.legend()` | Draws the legend box | Call it **after** the `plot` calls; only shows curves that have a `label` |
| `plt.gca()` | "Get current axes": returns the axes object of the plot | Gives access to axis-level settings |
| `.yaxis.set_major_formatter(...)` | Chooses how the y tick labels are written | Used with `EngFormatter(sep="")` |
| `plt.title("Population Projections")` | Sets the title of the plot | Required by subject |
| `plt.xlabel("Year")` | Labels the horizontal x-axis | Required by subject |
| `plt.ylabel("Population")` | Labels the vertical y-axis | Required by subject |
| `plt.show()` | Renders the visualization window | Blocks until the window is closed |

**Common pitfalls:**
- **Population values can be strings.** Cells like `"3.28M"`, `"16.1M"` or `"500k"` make `float("3.28M")` raise `ValueError`. Convert the suffixes (`k`, `M`, `B`) yourself with `decode`.
- **Not limiting the range:** the file goes up to 2100 but the subject demands **1800 to 2050**.
- **Selecting both countries with one mask and trusting the order.** `val[0]` is just the first matching row **in file order**. Labelling it "Japan" only works if Japan happens to come first. Select each country separately.
- **No legend / no label:** the subject asks for a legend for each curve.
- **Calling `plt.legend()` before any labelled plot:** you get an empty legend and a warning.
- **Wrapping each number in its own list** (`[[decode(i)] for i in val]`): it happens to plot, but each element becomes a 1-item list. Use `[decode(i) for i in val]`.
- **Unused variables** (for example an `idx` you computed but never used): flake8 reports `F841`, which breaks the norm.
- **Printing an error without stopping.** The code keeps running and crashes later with a `NameError`. Use `return`.
- **Mixed-up country spelling:** `"Japan"`, not `"japan"`.

---

## 4. Concepts You Need to Learn

### 4.1 Parsing suffixed numbers (`decode`)
| Text | Meaning | Value |
|---|---|---|
| `"500"` | plain | 500 |
| `"12.5k"` | thousands | 12 500 |
| `"3.28M"` | millions | 3 280 000 |
| `"1.4B"` | billions | 1 400 000 000 |

```python
def decode(text: str | float) -> float:
    """Convert values like '1.2k', '3M', '2B' to float. Invalid -> nan."""
    formats = {"k": 1e3, "M": 1e6, "B": 1e9}
    if isinstance(text, (int, float)):
        return float(text)
    text = text.strip()
    try:
        if text and text[-1] in formats:
            return float(text[:-1]) * formats[text[-1]]
        return float(text)
    except ValueError:
        return float("nan")
```
Read it line by line:
- `formats` is a dictionary mapping a suffix to its multiplier. `1e3` is `1000.0`, `1e6` is a million, `1e9` is a billion. It lives **inside** the function: a module-level dict would be a global variable, which is forbidden.
- `isinstance(text, (int, float))`: if the cell is **already a number** (this includes `NaN`, which is a float), return it as a float. Nothing to decode.
- `text.strip()` removes accidental spaces.
- `text and text[-1] in formats`: `text` alone is `False` for an empty string, which avoids an `IndexError` on `text[-1]`. If the last character is a known suffix:
  - `text[:-1]` is the number part (`"3.28"`), converted by `float(...)`,
  - `formats[text[-1]]` is the multiplier, so `"3.28M"` gives `3.28 * 1e6 = 3280000.0`.
- Otherwise it's plain text like `"500"`, so `float(text)` is enough.
- If the text is garbage (`"abc"`), `float` raises `ValueError`; we catch it and return `float("nan")`. The program doesn't crash on bad data, and matplotlib simply skips `NaN` points.

### 4.2 Selecting rows and a range of years with `.loc`
```python
row = data.loc[data["country"] == "Japan", "1800":"2050"]
```
`.loc[rows, columns]` selects rows and columns **at the same time**, using labels:
- The first part (`data["country"] == "Japan"`) is the boolean mask that picks the row(s).
- The second part (`"1800":"2050"`) is a **label slice** of columns. Unlike normal Python slices, it **includes both ends**, so 2050 is kept. This one expression solves the "1800 to 2050 only" requirement.
- It relies on the columns being in chronological order, as they are in this file.
- The result is a small DataFrame with 1 row (or 0 rows if the country doesn't exist) and 251 columns.

Then:
```python
if row.empty:
    print("Error: country 'Japan' not found.")
    return
years = [int(col) for col in row.columns]      # [1800, 1801, ..., 2050]
values = [decode(v) for v in row.iloc[0]]      # one float per year
```
- `row.columns` are the year names as strings; `int(col)` makes them numbers.
- `row.iloc[0]` is the first (and only) row as a Series; iterating over it gives the cell values in order.
- Building `years` from `row.columns` instead of `range(1800, 2051)` guarantees that `years` and `values` always have the **same length**, which `plt.plot` requires.

### 4.3 Why select each country separately
A first approach is to select both countries with one mask:
```python
mask = (data["country"] == "Japan") | (data["country"] == "Morocco")
val = data.loc[mask, "1800":"2050"].values.tolist()
# val[0] is "Japan" and val[1] is "Morocco"... only if the file lists them in that order
```
(`|` means "or" between two masks; each mask needs its own parentheses.) This is fragile:
- If the file order changes, the labels silently swap.
- If one country is missing, `val[1]` raises an `IndexError`.
- Unused helpers (like an `idx` list) get flagged by flake8.

A loop over the names avoids all three problems and is easier to read:
```python
curves = {}
for country in ("Japan", "Morocco"):
    row = data.loc[data["country"] == country, "1800":"2050"]
    if row.empty:
        print(f"Error: country '{country}' not found.")
        return
    curves[country] = [decode(v) for v in row.iloc[0]]
```
`curves` becomes `{"Japan": [...251 floats...], "Morocco": [...]}`: every list is attached to its own name.

### 4.4 Several curves and a legend
```python
for country, values in curves.items():
    plt.plot(years, values, label=country)
plt.legend()
```
- `curves.items()` gives `("Japan", [...])`, then `("Morocco", [...])`.
- Each `label=` becomes one legend entry.
- `plt.legend()` must come **after** the `plot` calls, otherwise there is nothing to list.
- Matplotlib picks a different color for each `plot` call automatically.
- Optional: `plt.legend(loc="lower right")` moves the box (the subject's picture has it in the bottom-right corner).

### 4.5 Formatting ticks as `20M`
```python
from matplotlib.ticker import EngFormatter

plt.gca().yaxis.set_major_formatter(EngFormatter(sep=""))
```
- Without it, large values appear as `1e7` or `10000000`.
- `plt.gca()` returns the "current axes" (the drawing area). Through it you can change axis-level details.
- `yaxis.set_major_formatter(...)` chooses how the **y** tick labels are written.
- `EngFormatter` writes numbers the engineering way: `20000000` becomes `20M`, `1000` becomes `1k`. `sep=""` removes the space between number and suffix (`20M`, not `20 M`).

### 4.6 Safe error handling
Problems that appear when the code only prints an error and continues:

1. **`load` returns `None` on failure.** Check it first, and leave:
   ```python
   data = load("population_total.csv")
   if data is None:
       return
   ```
   (`load` already prints the reason.)
2. **A missing country** gives an empty selection: test `row.empty`, print a message and `return`.
3. **A missing column** (for example no `"2050"`) raises `KeyError` in `.loc`. Catch only that, around the part that can fail:
   ```python
   try:
       ...
   except KeyError as e:
       print(f"Error: missing column {e}")
       return
   ```
4. **Always `return` after an error message.** Printing alone lets `main` continue, and later lines crash with `NameError` (variables never created), which invalidates the exercise.

---

## 5. Syntax and Examples

### Step-by-step snippet
```python
import pandas as pd

data = pd.DataFrame(
    {
        "country": ["Japan", "Morocco"],
        "1799": ["1M", "1M"],
        "1800": ["25M", "3M"],
        "1801": ["25.5M", "3.1M"],
        "2050": ["70M", "40M"],
        "2051": ["71M", "41M"],
    }
)

row = data.loc[data["country"] == "Japan", "1800":"2050"]
print(row.columns.tolist())   # ['1800', '1801', '2050']  (1799 and 2051 are cut)
print(row.iloc[0].tolist())   # ['25M', '25.5M', '70M']  (still text, needs decode)
```
Notice that the label slice keeps only the columns between `"1800"` and `"2050"` **in the file's column order**. The values are still text, so `decode` is applied next. If the `"2050"` column did not exist, `.loc` would raise a `KeyError`, which is why the solution catches it.

---

## 6. How to Think About the Exercise

1. **Step 1: Inspect the data.** Load the file and look at `dtypes` and the first few cells to see whether suffixes like `M` are present.
2. **Step 2: Write `decode`.** Convert any cell to a `float`, handling `k`, `M`, `B` and invalid text.
3. **Step 3: Load** with `load`; if it returns `None`, `return`.
4. **Step 4: For each of the two countries**, select its row and the columns `"1800":"2050"` with `.loc`; if empty, print a message and `return`; convert with `decode`; store in a dictionary. Wrap in `try/except KeyError`.
5. **Step 5: Plot both curves** with `label=`.
6. **Step 6: Decorate.** Title, x label, y label, `EngFormatter` on the y-axis, `plt.legend()`.
7. **Step 7: Show** with `plt.show()`.

---

## 7. Guided Practice

**Practice 1 (Easiest, suffix parsing):**
Convert `"3.28M"` to a float using a dictionary.

Expected output:
```
3280000.0
```

<details><summary>Solution</summary>

```python
def main() -> None:
    """Convert one suffixed string to a float."""
    text = "3.28M"
    formats = {"k": 1e3, "M": 1e6, "B": 1e9}
    print(float(text[:-1]) * formats[text[-1]])


if __name__ == "__main__":
    main()
```
</details>

**Practice 2 (A complete converter):**
Write `decode(value)` that accepts an int, a float, `"500"`, `"12.5k"`, `"3.28M"`, `"1.4B"` and invalid text.

Expected output for `["500", "12.5k", "3.28M", "1.4B", 7, "abc"]`:
```
500.0
12500.0
3280000.0
1400000000.0
7.0
nan
```

<details><summary>Solution</summary>

```python
def decode(text: str | float) -> float:
    """Convert values like '1.2k', '3M', '2B' to float. Invalid -> nan."""
    formats = {"k": 1e3, "M": 1e6, "B": 1e9}
    if isinstance(text, (int, float)):
        return float(text)
    text = text.strip()
    try:
        if text and text[-1] in formats:
            return float(text[:-1]) * formats[text[-1]]
        return float(text)
    except ValueError:
        return float("nan")


def main() -> None:
    """Test decode on several inputs."""
    for value in ["500", "12.5k", "3.28M", "1.4B", 7, "abc"]:
        print(decode(value))


if __name__ == "__main__":
    main()
```
</details>

**Practice 3 (`.loc` with a mask and a column range):**
Given the table below, select only Japan's columns from `"1800"` to `"2050"` (so `1799` and `2051` are dropped) and print the years as integers.

```python
data = pd.DataFrame(
    {
        "country": ["Japan", "Morocco"],
        "1799": [1, 1],
        "1800": [25, 3],
        "2050": [100, 40],
        "2051": [101, 41],
    }
)
```

Expected output:
```
[1800, 2050]
```

<details><summary>Solution</summary>

```python
import pandas as pd


def main() -> None:
    """Select one country and a range of year columns."""
    data = pd.DataFrame(
        {
            "country": ["Japan", "Morocco"],
            "1799": [1, 1],
            "1800": [25, 3],
            "2050": [100, 40],
            "2051": [101, 41],
        }
    )
    row = data.loc[data["country"] == "Japan", "1800":"2050"]
    if row.empty:
        print("Error: country not found.")
        return
    print([int(col) for col in row.columns])


if __name__ == "__main__":
    main()
```
</details>

**Practice 4 (Loop over countries into a dictionary):**
Using the same table, build `curves = {"Japan": [...], "Morocco": [...]}` with the values of columns `"1800":"2050"`, and print it. Print an error and `return` if a country is missing (test with `"Atlantis"` too).

Expected output:
```
{'Japan': [25, 100], 'Morocco': [3, 40]}
```

<details><summary>Solution</summary>

```python
import pandas as pd


def main() -> None:
    """Collect the values of two countries in a dictionary."""
    data = pd.DataFrame(
        {
            "country": ["Japan", "Morocco"],
            "1799": [1, 1],
            "1800": [25, 3],
            "2050": [100, 40],
            "2051": [101, 41],
        }
    )
    curves = {}
    for country in ("Japan", "Morocco"):
        row = data.loc[data["country"] == country, "1800":"2050"]
        if row.empty:
            print(f"Error: country '{country}' not found.")
            return
        curves[country] = row.iloc[0].tolist()
    print(curves)


if __name__ == "__main__":
    main()
```
</details>

**Practice 5 (Two curves with a legend):**
Plot `[1, 2, 3]` labelled `"A"` and `[3, 2, 1]` labelled `"B"` from a dictionary, with a title, axis labels and a legend.

Expected output: a window with two lines and a legend showing A and B.

<details><summary>Solution</summary>

```python
import matplotlib.pyplot as plt


def main() -> None:
    """Draw two labelled curves from a dictionary."""
    years = [1, 2, 3]
    curves = {"A": [1, 2, 3], "B": [3, 2, 1]}
    for name, values in curves.items():
        plt.plot(years, values, label=name)
    plt.title("Demo")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
```
</details>

**Practice 6 (Tick formatting with `EngFormatter`):**
Plot `years = [1800, 1900, 2000]`, `values = [3000000, 20000000, 60000000]` and make the y ticks read like `20M`, `40M`, `60M`.

Expected output: a rising line with y ticks written with `M`.

<details><summary>Solution</summary>

```python
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter


def main() -> None:
    """Plot with engineering-style y ticks."""
    plt.plot([1800, 1900, 2000], [3e6, 20e6, 60e6], label="demo")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.title("Demo")
    plt.gca().yaxis.set_major_formatter(EngFormatter(sep=""))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
```
</details>

**Practice 7 (Hardest, the full rule-compliant `aff_pop.py`):**

Expected output when running `python aff_pop.py`: a window titled `Population Projections`, x-axis `Year` (1800 to 2050), y-axis `Population` with `M` ticks, two labelled curves and a legend. Replace `"Japan"` with your campus's country, and `"Morocco"` with any other country.

<details><summary>Solution</summary>

```python
from load_csv import load
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter


def decode(text: str | float) -> float:
    """Convert values like '1.2k', '3M', '2B' to float. Invalid -> nan."""
    formats = {"k": 1e3, "M": 1e6, "B": 1e9}
    if isinstance(text, (int, float)):
        return float(text)
    text = text.strip()
    try:
        if text and text[-1] in formats:
            return float(text[:-1]) * formats[text[-1]]
        return float(text)
    except ValueError:
        return float("nan")


def main():
    """Plot the population of Japan versus Morocco from 1800 to 2050."""
    data = load("population_total.csv")
    if data is None:
        return
    curves = {}
    years = []
    try:
        for country in ("Japan", "Morocco"):
            row = data.loc[data["country"] == country, "1800":"2050"]
            if row.empty:
                print(f"Error: country '{country}' not found.")
                return
            years = [int(col) for col in row.columns]
            curves[country] = [decode(v) for v in row.iloc[0]]
    except KeyError as e:
        print(f"Error: missing column {e}")
        return
    for country, values in curves.items():
        plt.plot(years, values, label=country)
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.title("Population Projections")
    plt.gca().yaxis.set_major_formatter(EngFormatter(sep=""))
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
```
</details>

---

## 8. Exercise-Specific Knowledge

- **Two countries required:** yours and one of your choice. Pick one whose population scale is visible next to yours (the subject uses Belgium).
- **Years 1800 to 2050 only.** The file contains projections up to 2100; the `"1800":"2050"` column slice cuts them (and includes 2050).
- **Legend for each graph:** every `plt.plot` needs a `label`, and `plt.legend()` must be called after them.
- **Axis labels and title from the subject picture:** `Year` (x), `Population` (y), title `Population Projections`.
- **The `M`-tick formatting matches the subject picture.** `EngFormatter(sep="")` works whether the cells were text or plain numbers.
- **`decode` is harmless on plain numbers:** if cells are already floats it returns them unchanged.
- **One country can dwarf the other.** A flat-looking curve is a real scale difference, not a bug.
- **`load` can return `None`**, and a country can be missing: handle both without a traceback.
- **Global variable rule:** keep the conversion factors inside `decode` (a local dict), never at module level.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `ValueError: could not convert string to float: '3.28M'` | Suffixed text passed to `float` directly | Use `decode` |
| Plot runs to 2100 | Range not restricted | `.loc[mask, "1800":"2050"]` |
| Curves labelled with the wrong country | One mask for both countries, relied on file order | Loop over the names, one `.loc` per country |
| `IndexError: list index out of range` | A country is missing and `val[1]` doesn't exist | Check `row.empty` for each country |
| `NameError` after an error message | Error printed but code kept running | `return` after each error |
| `AttributeError: 'NoneType'...` | `load` returned `None` and the code kept going | `if data is None: return` |
| Each number wrapped in a list | `[[decode(i)] for i in val]` | `[decode(i) for i in val]` |
| flake8 `F841` | Variable computed but never used (e.g. `idx`) | Delete it |
| flake8 `W292` | No newline at end of file | Add a blank line at the end |
| Legend empty or warning | No `label=` or `legend()` called too early | Label each `plot`, call `legend()` after |
| `x` and `y` lengths differ | `years` built independently of the data | Build `years` from `row.columns` |
| Y ticks like `1e7` | No formatter | `EngFormatter(sep="")` on `yaxis` |
| Global `FORMATS` dict | Constant habit | Put it inside `decode` |

---

## 10. Debugging Guide

- **`ValueError: x and y must have same first dimension`:** `years` and `values` have different lengths; print `len(years)` and `len(values)`. Building `years` from `row.columns` prevents this.
- **`KeyError: '2050'` (or similar):** the file's columns might stop earlier or later; print `data.columns[-3:]`.
- **"Country not found" message:** print `data["country"].tolist()` to see valid names and spelling.
- **Both curves identical:** the loop variable isn't used in the mask; check `data["country"] == country`.
- **`TypeError` when plotting:** values are still strings; print `type(curves["Japan"][0])` and check that `decode` is applied.
- **Legend empty or warning:** `label=` is missing or `plt.legend()` runs before the `plot` calls.
- **Legend covers the curves:** move it with `plt.legend(loc="lower right")` or `"upper left"`.
- **Y ticks look like `1e7`:** the formatter wasn't applied; check `yaxis` (not `xaxis`) and the parentheses of `EngFormatter(sep="")`.
- **Quick data inspection:**
  ```python
  print(data.dtypes.head())
  print(data.iloc[0, :5])
  print(data.columns[-3:])
  ```

---

## 11. Cheat Sheet

```python
data = load("population_total.csv")
if data is None:
    return

curves = {}
for country in ("Japan", "Morocco"):
    row = data.loc[data["country"] == country, "1800":"2050"]
    if row.empty:
        print(f"Error: country '{country}' not found.")
        return
    years = [int(col) for col in row.columns]
    curves[country] = [decode(v) for v in row.iloc[0]]

for country, values in curves.items():
    plt.plot(years, values, label=country)
plt.xlabel("Year")
plt.ylabel("Population")
plt.title("Population Projections")
plt.gca().yaxis.set_major_formatter(EngFormatter(sep=""))
plt.legend()
plt.show()
```

---

## 12. Knowledge Checklist

- [ ] I load `population_total.csv` through my own `load` function and check `is None` right after.
- [ ] `decode` converts `k`/`M`/`B` suffixes, passes numbers through, and returns `nan` for invalid text.
- [ ] I select each country separately with `.loc[mask, "1800":"2050"]` and check `row.empty`.
- [ ] The graph shows my country and another one, from 1800 to 2050 only.
- [ ] Title, x label, y label and a legend entry for each curve are present, and `plt.legend()` comes after the plots.
- [ ] The y-axis uses `EngFormatter(sep="")` to show `20M`-style ticks.
- [ ] Missing file, missing country and missing column print a clear message and `return` instead of crashing.
- [ ] I can explain what `.loc`, `.iloc`, `.columns`, `.items()`, `plt.gca()` and `EngFormatter` do.
- [ ] No globals, `main()` present, docstrings everywhere, no unused variables, final newline, `flake8` clean.
