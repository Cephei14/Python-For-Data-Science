# Study Tutorial — Exercise 03: projection_life.py

## 1. Exercise Overview

**What it asks:**
Create a program `projection_life.py` (along with `load_csv.py`) in directory `ex03/` that:
1. Calls the `load` function from ex00.
2. Loads **two** files: `income_per_person_gdppercapita_ppp_inflation_adjusted.csv` and `life_expectancy_years.csv`.
3. Displays, for the **year 1900**, the life expectancy as a function of the gross domestic product (GDP per person) **for each country**: one point per country (a **scatter plot**).
4. The graph must have a **title**, a **label on each axis** and a **legend for each graph**.
5. You must display the year **1900**.

The subject's example: title `1900`, x-axis `Gross domestic product` on a **logarithmic scale** (ticks `300`, `1k`, `10k`), y-axis `Life Expectancy` (about 20 to 55), a cloud of blue dots rising from left to right.

**The question from the subject:**
> Do you see a correlation between life span and gross domestic product?

**Rules and Constraints:**
- Files to turn in: `load_csv.py`, `projection_life.py`.
- Allowed: `matplotlib`, `seaborn` or any data-visualization library, and your ex00 library.
- No code in the global scope, no global variables, `main()` with error handling.
- Uncaught exceptions invalidate the exercise.
- Docstrings, `flake8`, explicit imports, Python 3.10+.

**Main concepts you'll learn:**
- Combining two datasets by a shared key (`country`).
- Extracting one column (one year) from a table.
- Scatter plots and logarithmic axes.
- Reading a correlation from a chart, and its limits.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **`load()` from ex00:** returns a DataFrame or `None`.
- **Column access (ex00/ex01):** `data["1900"]`; columns are strings.
- **Suffix parsing (ex02):** `"1.2k"` to `1200.0`. GDP values may also carry a `k` suffix depending on your file version.
- **Plot decoration and legend (ex01/ex02):** title, labels, `label=`, `plt.legend()`.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `from load_csv import load` | Loads both datasets | Called twice |
| `DataFrame.merge(other, on="country")` | Joins two tables by country | Keeps only countries present in both (inner join) |
| `DataFrame.dropna()` | Removes rows with missing values | A missing point can't be plotted |
| `plt.scatter(x, y, label=...)` | Draws one dot per pair | Not `plt.plot` |
| `plt.xscale("log")` | Logarithmic x-axis | Matches the subject picture |
| `plt.legend()` | Legend | "Legend for each graph" |

**Common pitfalls:**
- **Assuming both files list the same countries in the same order.** Rows may differ in count or order; aligning by position gives wrong pairs. **Merge on `country`.**
- **Missing values (NaN):** some countries have no 1900 data. Drop them before plotting.
- **Strings like `"1.2k"`:** check `data["1900"].dtype`; if it is `object`, convert with a `to_number` helper (see ex02).
- **Linear x-axis:** GDP spans orders of magnitude; on a linear axis all dots clump on the left. Use `plt.xscale("log")`.
- **Wrong year:** columns are `"1900"` (string), not `1900` (int).
- **Plotting with `plt.plot`:** it connects the dots with a line. A scatter of independent countries needs `plt.scatter`.

---

## 4. Concepts You Need to Learn

### 4.1 Joining two tables
```python
merged = gdp[["country", "1900"]].merge(
    life[["country", "1900"]],
    on="country",
    suffixes=("_gdp", "_life"),
)
```
Both tables have a column named `1900`, so `suffixes` renames them `1900_gdp` and `1900_life`. The merge keeps each country once, with its two values side by side.

### 4.2 Missing data
```python
merged = merged.dropna()
```
Removes any country missing either value.

### 4.3 Scatter plot
```python
plt.scatter(x_values, y_values, label="1900")
```
One dot per country: x is the GDP, y is the life expectancy.

### 4.4 Logarithmic axis
On a log axis, equal distances mean equal **ratios** (300 → 1k → 10k, roughly evenly spaced). This spreads out the poorer countries and makes a relationship visible. To label ticks like `300`, `1k`, `10k`:
```python
from matplotlib.ticker import FuncFormatter

def short(value: float, _: int) -> str:
    return f"{value / 1000:g}k" if value >= 1000 else f"{value:g}"

axes = plt.gca()
axes.set_xticks([300, 1000, 10000])
axes.xaxis.set_major_formatter(FuncFormatter(short))
```

### 4.5 Correlation, not causation
In the picture, countries with a higher GDP tend to have a higher life expectancy: a **positive correlation**. But the cloud is wide (at a given GDP, life expectancy varies by 10+ years), and correlation does not prove that wealth *causes* longer life (public health, geography, data quality and other factors matter too).

---

## 5. Syntax and Examples

### Step-by-step snippet
```python
import matplotlib.pyplot as plt
from load_csv import load

gdp = load("income_per_person_gdppercapita_ppp_inflation_adjusted.csv")
life = load("life_expectancy_years.csv")

merged = gdp[["country", "1900"]].merge(
    life[["country", "1900"]], on="country", suffixes=("_gdp", "_life")
).dropna()

plt.scatter(merged["1900_gdp"], merged["1900_life"], label="1900")
plt.xscale("log")
plt.title("1900")
plt.xlabel("Gross domestic product")
plt.ylabel("Life Expectancy")
plt.legend()
plt.show()
```
(If the GDP column holds text such as `"1.2k"`, convert it first; see the full solution.)

---

## 6. How to Think About the Exercise

1. **Step 1: Load both files** with `load`. If either is `None`, stop cleanly.
2. **Step 2: Keep only `country` and `1900`** in each table (check the column exists).
3. **Step 3: Merge on `country`** and drop rows with missing values.
4. **Step 4: Convert values to floats** (handle `k`/`M` suffixes if present).
5. **Step 5: Plot** a scatter with log x-axis, title `1900`, both axis labels and a legend.
6. **Step 6: Wrap in `main()`**, catch errors, `plt.show()`, then answer the correlation question for yourself (be ready to discuss it in the defence).

---

## 7. Guided Practice

**Practice 1 (Easiest — a scatter plot):**
Scatter `x = [1, 2, 3, 4]` against `y = [2, 4, 5, 8]` with a title and axis labels.

Expected output: four dots rising from left to right.

<details><summary>Solution</summary>

```python
import matplotlib.pyplot as plt

plt.scatter([1, 2, 3, 4], [2, 4, 5, 8], label="demo")
plt.title("Demo")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.show()
```
</details>

**Practice 2 (Merge two tables):**
Merge `a = {"country": ["X", "Y", "Z"], "1900": [100, 200, 300]}` and `b = {"country": ["Y", "Z", "W"], "1900": [40, 50, 60]}` on `country`.

Expected output:
```
  country  1900_gdp  1900_life
0       Y       200         40
1       Z       300         50
```

<details><summary>Solution</summary>

```python
import pandas as pd

a = pd.DataFrame({"country": ["X", "Y", "Z"], "1900": [100, 200, 300]})
b = pd.DataFrame({"country": ["Y", "Z", "W"], "1900": [40, 50, 60]})
print(a.merge(b, on="country", suffixes=("_gdp", "_life")))
```
</details>

**Practice 3 (Drop missing values):**
Drop rows with `NaN` from a merged table containing one missing life-expectancy value.

Expected output: the row with `NaN` is gone.

<details><summary>Solution</summary>

```python
import numpy as np
import pandas as pd

df = pd.DataFrame(
    {"country": ["A", "B"], "1900_gdp": [1.0, 2.0], "1900_life": [30.0, np.nan]}
)
print(df.dropna())
```
</details>

**Practice 4 (Log axis):**
Scatter `x = [300, 1000, 10000]`, `y = [25, 35, 50]` with `plt.xscale("log")`. The three dots should be roughly evenly spaced horizontally.

Expected output: three dots on a rising line with a log x-axis.

<details><summary>Solution</summary>

```python
import matplotlib.pyplot as plt

plt.scatter([300, 1000, 10000], [25, 35, 50], label="demo")
plt.xscale("log")
plt.xlabel("GDP")
plt.ylabel("Life Expectancy")
plt.legend()
plt.show()
```
</details>

**Practice 5 (Hardest — the full, rule-compliant `projection_life.py`):**

Expected output when running `python projection_life.py`: a window titled `1900` with x-axis `Gross domestic product` (log scale), y-axis `Life Expectancy`, a legend, and one dot per country.

<details><summary>Solution</summary>

```python
"""Display life expectancy versus GDP per person for the year 1900."""

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


def prepare(
    gdp: pd.DataFrame, life: pd.DataFrame, year: str
) -> tuple[list[float], list[float]]:
    """Pair GDP and life expectancy by country for one year.

    Args:
        gdp: GDP-per-person table.
        life: Life-expectancy table.
        year: Column to use, e.g. "1900".

    Returns:
        A tuple (gdp_values, life_values) without missing data.

    Raises:
        KeyError: If the year column is missing from a table.
    """
    merged = gdp[["country", year]].merge(
        life[["country", year]],
        on="country",
        suffixes=("_gdp", "_life"),
    ).dropna()
    x_values = [to_number(v) for v in merged[f"{year}_gdp"]]
    y_values = [to_number(v) for v in merged[f"{year}_life"]]
    return x_values, y_values


def short(value: float, _: int) -> str:
    """Format a tick value as 300, 1k, 10k..."""
    if value >= 1000:
        return f"{value / 1000:g}k"
    return f"{value:g}"


def main() -> None:
    """Load both datasets and plot life expectancy against GDP."""
    try:
        gdp = load("income_per_person_gdppercapita_ppp_inflation_adjusted.csv")
        life = load("life_expectancy_years.csv")
        if gdp is None or life is None:
            return
        x_values, y_values = prepare(gdp, life, "1900")
        plt.scatter(x_values, y_values, label="1900")
        plt.xscale("log")
        axes = plt.gca()
        axes.set_xticks([300, 1000, 10000])
        axes.xaxis.set_major_formatter(FuncFormatter(short))
        plt.title("1900")
        plt.xlabel("Gross domestic product")
        plt.ylabel("Life Expectancy")
        plt.legend()
        plt.show()
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
```
</details>

---

## 8. Exercise-Specific Knowledge

- **The year is 1900**, used as the column name `"1900"` in both files.
- **Scatter, not line:** countries are independent observations; there is no order to connect.
- **One dot per country** that has data in **both** files for 1900.
- **Axis labels from the subject picture:** `Gross domestic product` (x) and `Life Expectancy` (y); title `1900`.
- **Log scale:** the picture's x-axis runs from 300 to 10k on a log scale. Adjust the `set_xticks` values if your data range differs (print `min`/`max` of the x values).
- **The two files are different datasets:** never assume same row order or same number of countries (`load` prints each shape; compare them).
- **Discussion question (expect it in defence):** yes, a positive correlation is visible (richer countries tend to show longer lives), but it is loose and is not proof of causation.
- **Allowed libs:** you may use `seaborn` (`sns.scatterplot`) instead of matplotlib if you prefer, as long as it follows the same rules.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Wrong pairs of points | Zipped two tables by row position | `merge(on="country")` |
| `ValueError: cannot convert float NaN` or a missing-data crash | Countries without 1900 data | `.dropna()` after merge |
| `KeyError: 1900` | Used an int instead of a string | `"1900"` |
| Dots squashed at the left edge | Linear x-axis | `plt.xscale("log")` |
| Line joining all dots | Used `plt.plot` | `plt.scatter` |
| `ValueError` on `"1.2k"` | GDP given as text | Reuse `to_number` |
| No legend | Forgot `label=` / `legend()` | `label="1900"` and `plt.legend()` |
| Suffix columns `1900_x`, `1900_y` | Forgot `suffixes` | Pass `suffixes=("_gdp", "_life")` |

---

## 10. Debugging Guide

- **`KeyError: '1900_gdp'`:** the suffix names differ from what you wrote in `merged[...]`; print `merged.columns`.
- **Empty plot:** `merged` is empty. Check that both files use the same country spelling and that `"1900"` holds data (`print(gdp["1900"].isna().sum())`).
- **Ticks show `10^2`, `10^3`...:** you didn't set the formatter; use `set_xticks` + `FuncFormatter`, or accept the default log ticks.
- **`TypeError` in `scatter`:** values are still strings; print `type(x_values[0])`.
- **Number of dots differs from the subject picture:** data versions differ; that's fine as long as every country with data in both files is plotted.

---

## 11. Cheat Sheet

```python
merged = gdp[["country", "1900"]].merge(
    life[["country", "1900"]], on="country", suffixes=("_gdp", "_life")
).dropna()
x = [to_number(v) for v in merged["1900_gdp"]]
y = [to_number(v) for v in merged["1900_life"]]

plt.scatter(x, y, label="1900")
plt.xscale("log")
plt.title("1900")
plt.xlabel("Gross domestic product")
plt.ylabel("Life Expectancy")
plt.legend()
plt.show()
```

---

## 12. Knowledge Checklist

- [ ] Both datasets are loaded through my own `load` function.
- [ ] Countries are matched by name with a merge, and missing values are dropped.
- [ ] The scatter shows year 1900 with a log x-axis, a title, both axis labels and a legend.
- [ ] Missing files or missing columns print a clear message instead of crashing.
- [ ] I can explain the correlation between GDP and life expectancy, and why it is not proof of causation.
- [ ] No globals, `main()` present, docstrings everywhere, `flake8` clean.
