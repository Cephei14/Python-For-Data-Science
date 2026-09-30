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
- Uncaught exceptions invalidate the exercise.
- Docstrings, `flake8`, explicit imports, Python 3.10+.

**Main concepts you'll learn:**
- Converting text values such as `"28.4M"` into numbers.
- Restricting a series to a range of years.
- Drawing several labelled curves and a legend on one axes.
- Custom tick formatting (`20M` instead of `20000000`).

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **`load()` from ex00:** returns a DataFrame or `None`.
- **Country extraction from ex01:** filter by `data["country"] == name`, drop `country`, convert years to `int`.
- **String handling (Module 0):** slicing (`text[-1]`, `text[:-1]`), dictionaries, `float()`.
- **Line charts (ex01):** `plt.plot`, title, axis labels.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `from load_csv import load` | Loads the dataset | Same file as ex00 |
| `import matplotlib.pyplot as plt` | Plotting | |
| `from matplotlib.ticker import FuncFormatter` | Custom tick labels | Gives `20M`-style ticks |
| `plt.plot(x, y, label="France")` | Curve with legend text | `label` feeds the legend |
| `plt.legend()` | Draws the legend | Call **after** the plots |
| `plt.gca().yaxis.set_major_formatter(...)` | Applies the formatter | |

**Common pitfalls:**
- **Population values can be strings.** In the usual Gapminder `population_total.csv`, many cells look like `"3.28M"`, `"16.1M"` or `"500k"`, not plain numbers. Check with `data.dtypes` and `data.iloc[0, :5]`. Calling `float("3.28M")` raises `ValueError`. Convert the suffixes (`k`, `M`, `B`) yourself.
- **Not limiting the range:** the file goes up to 2100 but the subject demands **1800 to 2050**.
- **No legend / no label:** the subject asks for "a legend for each graph" (each curve).
- **Mixed-up country spelling:** `"Belgium"`, not `"belgium"`.
- **Calling `plt.legend()` before any labelled plot:** you get an empty legend and a warning.
- **A global conversion table:** a module-level dict like `FACTORS = {...}` is a global variable. Keep it inside the function.

---

## 4. Concepts You Need to Learn

### 4.1 Parsing suffixed numbers
| Text | Meaning | Value |
|---|---|---|
| `"500"` | plain | 500 |
| `"12.5k"` | thousands | 12 500 |
| `"3.28M"` | millions | 3 280 000 |
| `"1.4B"` | billions | 1 400 000 000 |

Idea: look at the **last character**; if it is a known suffix, multiply the rest.
```python
factors = {"k": 1e3, "M": 1e6, "B": 1e9}
text = "3.28M"
if text[-1] in factors:
    number = float(text[:-1]) * factors[text[-1]]
```
Already-numeric cells (int/float) must be returned as they are.

### 4.2 Restricting to 1800–2050
After converting the column names to `int`, keep only the pairs with `1800 <= year <= 2050`:
```python
pairs = [(y, v) for y, v in zip(years, values) if 1800 <= y <= 2050]
```

### 4.3 Several curves and a legend
```python
plt.plot(years, france, label="France")
plt.plot(years, belgium, label="Belgium")
plt.legend(loc="lower right")
```
Each `label=` becomes one legend entry.

### 4.4 Formatting ticks as `20M`
```python
def millions(value: float, _: int) -> str:
    return f"{int(value / 1e6)}M"

plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
```
The formatter receives `(tick_value, tick_position)` and returns the text to display.

---

## 5. Syntax and Examples

### Step-by-step snippet
```python
import matplotlib.pyplot as plt
from load_csv import load

data = load("population_total.csv")
for name in ("France", "Belgium"):
    row = data[data["country"] == name].iloc[0].drop("country")
    years = [int(y) for y in row.index if int(y) <= 2050]
    values = [to_number(row[str(y)]) for y in years]   # to_number: see 4.1
    plt.plot(years, values, label=name)

plt.title("Population Projections")
plt.xlabel("Year")
plt.ylabel("Population")
plt.legend(loc="lower right")
plt.show()
```

---

## 6. How to Think About the Exercise

1. **Step 1: Inspect the data.** Load the file and look at `dtypes` and the first few cells to know whether suffixes like `M` are present.
2. **Step 2: Write `to_number`.** Convert any cell to a `float`, handling `k`, `M`, `B`.
3. **Step 3: Write `get_population(data, country)`.** Return `(years, values)` restricted to 1800–2050; raise `ValueError` if the country is missing.
4. **Step 4: Plot both countries** with `label=`.
5. **Step 5: Decorate.** Title, x label, y label, legend, optional `20M`-style formatter.
6. **Step 6: Wrap in `main()`** with `try`/`except`, and show.

---

## 7. Guided Practice

**Practice 1 (Easiest — suffix parsing):**
Convert `"3.28M"` to a float.

Expected output:
```
3280000.0
```

<details><summary>Solution</summary>

```python
text = "3.28M"
factors = {"k": 1e3, "M": 1e6, "B": 1e9}
print(float(text[:-1]) * factors[text[-1]])
```
</details>

**Practice 2 (A complete converter):**
Write `to_number(value)` that accepts an int, a float, `"500"`, `"12.5k"`, `"3.28M"`, `"1.4B"`.

Expected output:
```
[500.0, 12500.0, 3280000.0, 1400000000.0]
```
for `["500", "12.5k", "3.28M", "1.4B"]`.

<details><summary>Solution</summary>

```python
def to_number(value: str | float) -> float:
    """Convert a number or a string with k/M/B suffix to a float."""
    if isinstance(value, (int, float)):
        return float(value)
    factors = {"k": 1e3, "M": 1e6, "B": 1e9}
    text = str(value).strip()
    if text and text[-1] in factors:
        return float(text[:-1]) * factors[text[-1]]
    return float(text)
```
</details>

**Practice 3 (Restrict to a range of years):**
Given `years = [1799, 1800, 2050, 2051]` and `values = [1, 2, 3, 4]`, keep only 1800–2050.

Expected output:
```
([1800, 2050], [2, 3])
```

<details><summary>Solution</summary>

```python
years = [1799, 1800, 2050, 2051]
values = [1, 2, 3, 4]
pairs = [(y, v) for y, v in zip(years, values) if 1800 <= y <= 2050]
print(([p[0] for p in pairs], [p[1] for p in pairs]))
```
</details>

**Practice 4 (Two curves with legend):**
Plot `[1, 2, 3]` labelled `"A"` and `[3, 2, 1]` labelled `"B"`, with title and axis labels.

Expected output: a window with two lines and a legend showing A and B.

<details><summary>Solution</summary>

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [1, 2, 3], label="A")
plt.plot([1, 2, 3], [3, 2, 1], label="B")
plt.title("Demo")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()
```
</details>

**Practice 5 (Hardest — the full, rule-compliant `aff_pop.py`):**

Expected output when running `python aff_pop.py`: a window titled `Population Projections`, x-axis `Year` (1800–2050), y-axis `Population` with `M` ticks, two labelled curves and a legend.

<details><summary>Solution</summary>

```python
"""Compare the population of two countries between 1800 and 2050."""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter
from load_csv import load


def to_number(value: str | float) -> float:
    """Convert a number or a string with a k/M/B suffix to a float."""
    if isinstance(value, (int, float)):
        return float(value)
    factors = {"k": 1e3, "M": 1e6, "B": 1e9}
    text = str(value).strip()
    if text and text[-1] in factors:
        return float(text[:-1]) * factors[text[-1]]
    return float(text)


def get_population(
    data: pd.DataFrame, country: str
) -> tuple[list[int], list[float]]:
    """Return the years (1800-2050) and populations of a country.

    Raises:
        ValueError: If the country is not in the dataset.
    """
    rows = data[data["country"] == country]
    if rows.empty:
        raise ValueError(f"Country '{country}' not found.")
    series = rows.iloc[0].drop("country")
    years = []
    values = []
    for year, cell in series.items():
        if 1800 <= int(year) <= 2050:
            years.append(int(year))
            values.append(to_number(cell))
    return years, values


def millions(value: float, _: int) -> str:
    """Format a tick value as a number of millions (e.g. 20M)."""
    return f"{int(value / 1e6)}M"


def main() -> None:
    """Load the population file and compare two countries."""
    try:
        first = "France"    # replace with your campus's country
        second = "Belgium"  # any other country of your choice
        data = load("population_total.csv")
        if data is None:
            return
        for name in (second, first):
            years, values = get_population(data, name)
            plt.plot(years, values, label=name)
        plt.title("Population Projections")
        plt.xlabel("Year")
        plt.ylabel("Population")
        plt.gca().yaxis.set_major_formatter(FuncFormatter(millions))
        plt.legend(loc="lower right")
        plt.show()
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
```
</details>

---

## 8. Exercise-Specific Knowledge

- **Two countries required:** yours and one of your choice. Pick one whose population scale is visible next to yours (the subject uses Belgium).
- **Years 1800 to 2050 only.** The file contains projections up to 2100; cut them.
- **Legend for each graph:** every `plt.plot` needs a `label`, and `plt.legend()` must be called.
- **The `M`-tick formatting is optional but matches the subject picture.** If your data are plain numbers, the same formatter still works.
- **Check your own file.** Data versions differ. If cells are already floats, `to_number` simply returns them; the converter is harmless either way.
- **Global variable rule:** keep the conversion factors inside the function (a local dict), never at module level.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `ValueError: could not convert string to float: '3.28M'` | Suffixed text | Write and use `to_number` |
| Plot runs to 2100 | Range not restricted | Filter `1800 <= year <= 2050` |
| Legend empty | No `label=` or `legend()` called too early | Label each `plot`, call `legend()` last |
| One curve dwarfs the other and looks flat | Real scale difference | Normal; do not "fix" by changing data |
| Y ticks like `1e7` | No formatter | Use `FuncFormatter` or label the axis "Population" clearly |
| Global `FACTORS` dict | Constant habit | Put it inside `to_number` |

---

## 10. Debugging Guide

- **`TypeError` when plotting:** values are still strings; print `type(values[0])`.
- **`KeyError: '2050'` or similar:** the file's columns might stop earlier/later; print `data.columns[-3:]`.
- **Both curves identical:** you reused the same variable; check that the country name changes in each loop iteration.
- **Legend covers the curves:** move it with `loc="upper left"` or `"lower right"`.
- **`ValueError: Country ... not found.`:** print `data["country"].tolist()` to see valid names.

---

## 11. Cheat Sheet

```python
def to_number(value):
    if isinstance(value, (int, float)):
        return float(value)
    f = {"k": 1e3, "M": 1e6, "B": 1e9}
    return float(value[:-1]) * f[value[-1]] if value[-1] in f else float(value)

row = data[data["country"] == name].iloc[0].drop("country")
pairs = [(int(y), to_number(v)) for y, v in row.items() if int(y) <= 2050]
plt.plot([p[0] for p in pairs], [p[1] for p in pairs], label=name)
plt.legend()
```

---

## 12. Knowledge Checklist

- [ ] I load `population_total.csv` through my own `load` function.
- [ ] Population cells with `k`/`M`/`B` suffixes are converted correctly.
- [ ] The graph shows my country and another one, from 1800 to 2050.
- [ ] Title, x label, y label and a legend entry for each curve are present.
- [ ] Unknown country / missing file is handled without a traceback.
- [ ] No globals, `main()` present, docstrings everywhere, `flake8` clean.
