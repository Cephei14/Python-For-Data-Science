# Study Tutorial — Exercise 01: aff_life.py

## 1. Exercise Overview

**What it asks:**
Create a program `aff_life.py` (along with `load_csv.py`) in directory `ex01/` that:
1. Calls the `load` function from ex00.
2. Loads `life_expectancy_years.csv`.
3. Extracts the row of **your campus's country**.
4. Plots life expectancy against the years (1800 to 2100).
5. The graph must have a **title** and a **label on each axis**.

The subject's example is France: title `France Life expectancy Projections`, x-axis `Year`, y-axis `Life expectancy`, a single blue line rising from about 30 in 1800 to about 92 in 2100, with dips around the World Wars.

**Rules and Constraints:**
- Files to turn in: `load_csv.py`, `aff_life.py`.
- Allowed: `matplotlib`, `seaborn` or any data-visualization library, plus your ex00 library.
- No code in the global scope, no global variables, a `main()` with error handling.
- Uncaught exceptions invalidate the exercise (e.g. a country that doesn't exist).
- Docstrings on every function, `flake8` clean, explicit imports, Python 3.10+.

**Main concepts you'll learn:**
- Selecting a row from a DataFrame by condition (boolean filtering).
- Turning a DataFrame row into two lists: x values (years) and y values.
- Drawing a labelled line chart with `matplotlib`.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **`load()` from ex00 (Module 2):** returns a DataFrame or `None`.
- **DataFrame shape and columns (ex00):** one row per country, columns `country`, `1800`...`2100`.
- **Lists and type conversion (Module 0):** `int("1800")`, `float(x)`, list comprehensions.
- **Plotting basics (Data Science 1 ex03):** `plt.imshow`, `plt.show`; here we use `plt.plot`.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `from load_csv import load` | Loads the dataset | Copy of ex00 file |
| `import matplotlib.pyplot as plt` | Plotting | Explicit import |
| `data[data["country"] == name]` | Filters rows | Boolean mask |
| `.iloc[0]` | First row of the filtered result | Returns a Series |
| `plt.plot(x, y)` | Draws a line | x and y same length |
| `plt.title`, `plt.xlabel`, `plt.ylabel` | Text decorations | All three required |
| `plt.show()` | Opens the window | Blocks until closed |

**Common pitfalls:**
- **Column names are strings:** after `read_csv`, the columns are `"1800"`, not `1800`. Plotting them directly gives a categorical axis with every label crammed together. Convert years to `int`.
- **Country not found:** filtering returns an empty result; `.iloc[0]` then raises `IndexError`. Check first and raise a clear error.
- **Forgetting to drop the `country` column** from the row: you would try to plot the country name as a value.
- **Missing axis labels or title:** the subject requires them; evaluators look for them.
- **Hard-coding a wrong country:** use the country of **your own campus**, spelled exactly as in the CSV (`"France"`, not `"france"`).

---

## 4. Concepts You Need to Learn

### 4.1 Boolean filtering
```python
mask = data["country"] == "France"     # Series of True/False, one per row
rows = data[mask]                      # DataFrame with only matching rows
```
`rows.empty` is `True` when nothing matched.

### 4.2 From a row to (x, y)
The filtered row contains `country` followed by one value per year:
```python
series = rows.iloc[0].drop("country")  # index: "1800".."2100", values: floats
years = [int(year) for year in series.index]
values = [float(v) for v in series.values]
```

### 4.3 Anatomy of a matplotlib line chart
```python
plt.plot(years, values)
plt.title("France Life expectancy Projections")
plt.xlabel("Year")
plt.ylabel("Life expectancy")
plt.show()
```
`plt.plot` with no format string draws a solid blue line, the default colour cycle's first colour, as in the subject.

### 4.4 Why "projections"?
The dataset extends to 2100: values after today's date are forecasts. That's why the title says "Projections".

---

## 5. Syntax and Examples

### Step-by-step snippet
```python
import matplotlib.pyplot as plt
from load_csv import load

data = load("life_expectancy_years.csv")
row = data[data["country"] == "France"].iloc[0].drop("country")

plt.plot([int(y) for y in row.index], [float(v) for v in row.values])
plt.title("France Life expectancy Projections")
plt.xlabel("Year")
plt.ylabel("Life expectancy")
plt.show()
```

---

## 6. How to Think About the Exercise

1. **Step 1: Load.** Call `load("life_expectancy_years.csv")`. If it returns `None`, stop cleanly.
2. **Step 2: Select the country.** Filter the DataFrame; raise a `ValueError` if nothing matches.
3. **Step 3: Build x and y.** Drop the `country` cell, convert the index to `int` years and values to `float`.
4. **Step 4: Plot.** `plt.plot`, then title, xlabel, ylabel.
5. **Step 5: Show.** `plt.show()`.
6. **Step 6: Wrap everything in `main()`** with `try`/`except`, and keep the global scope empty.

---

## 7. Guided Practice

**Practice 1 (Easiest — plot a hard-coded line):**
Plot `x = [1, 2, 3]`, `y = [2, 4, 8]` with a title and both axis labels.

Expected output: a window showing a rising blue curve with title and labels.

<details><summary>Solution</summary>

```python
import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [2, 4, 8])
plt.title("Demo")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
```
</details>

**Practice 2 (Filter a row):**
Given `df = pd.DataFrame({"country": ["A", "B"], "2000": [1.0, 2.0], "2001": [3.0, 4.0]})`, extract the values for `"B"` as a list of floats.

Expected output:
```
[2.0, 4.0]
```

<details><summary>Solution</summary>

```python
import pandas as pd

df = pd.DataFrame(
    {"country": ["A", "B"], "2000": [1.0, 2.0], "2001": [3.0, 4.0]}
)
row = df[df["country"] == "B"].iloc[0].drop("country")
print([float(v) for v in row.values])
```
</details>

**Practice 3 (Years as integers):**
From the same row, produce the years as integers.

Expected output:
```
[2000, 2001]
```

<details><summary>Solution</summary>

```python
print([int(y) for y in row.index])
```
</details>

**Practice 4 (Handle an unknown country):**
Write `get_series(data, country)` returning `(years, values)` and raising `ValueError("Country 'X' not found.")` when absent.

Expected output for `get_series(df, "Z")`:
```
ValueError: Country 'Z' not found.
```

<details><summary>Solution</summary>

```python
import pandas as pd


def get_series(
    data: pd.DataFrame, country: str
) -> tuple[list[int], list[float]]:
    """Return the years and values of one country."""
    rows = data[data["country"] == country]
    if rows.empty:
        raise ValueError(f"Country '{country}' not found.")
    series = rows.iloc[0].drop("country")
    years = [int(year) for year in series.index]
    values = [float(value) for value in series.values]
    return years, values
```
</details>

**Practice 5 (Hardest — the full, rule-compliant `aff_life.py`):**

Expected output when running `python aff_life.py`: a window titled `<Country> Life expectancy Projections`, x-axis `Year`, y-axis `Life expectancy`.

<details><summary>Solution</summary>

```python
"""Display the life expectancy projections of one country."""

import matplotlib.pyplot as plt
import pandas as pd
from load_csv import load


def get_series(
    data: pd.DataFrame, country: str
) -> tuple[list[int], list[float]]:
    """Extract the years and life expectancies of one country.

    Args:
        data: DataFrame with a 'country' column and one column per year.
        country: Name of the country, as written in the file.

    Returns:
        A tuple (years, values).

    Raises:
        ValueError: If the country is not in the dataset.
    """
    rows = data[data["country"] == country]
    if rows.empty:
        raise ValueError(f"Country '{country}' not found.")
    series = rows.iloc[0].drop("country")
    years = [int(year) for year in series.index]
    values = [float(value) for value in series.values]
    return years, values


def main() -> None:
    """Load the dataset and plot the life expectancy of a country."""
    try:
        country = "France"  # replace with your campus's country
        data = load("life_expectancy_years.csv")
        if data is None:
            return
        years, values = get_series(data, country)
        plt.plot(years, values)
        plt.title(f"{country} Life expectancy Projections")
        plt.xlabel("Year")
        plt.ylabel("Life expectancy")
        plt.show()
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
```
</details>

---

## 8. Exercise-Specific Knowledge

- **Your campus's country is the point.** The subject uses France as an example; use your own and spell it exactly as in the CSV.
- **Two files to turn in:** `load_csv.py` (same as ex00) and `aff_life.py`. The plotting script must use `load`, not its own `read_csv`.
- **Labels required:** title + x label + y label. No legend is required in this exercise (only one curve), unlike ex02 and ex03.
- **The x-axis should read 1800 ... 2080 in steps of 40** (as in the subject picture), which happens automatically when years are integers.
- **Cleanliness of the local variable:** a local `country = "France"` inside `main()` is fine; a module-level constant is a *global variable* and is not allowed.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| X-axis crowded with 301 overlapping labels | Years left as strings | `int(year)` for each column name |
| `IndexError` for an unknown country | `.iloc[0]` on empty result | Check `rows.empty` and raise `ValueError` |
| Plot fails with a `ValueError` on the string `France` | `country` cell not dropped | `.drop("country")` |
| No title / labels | Forgot decorations | Add `plt.title`, `plt.xlabel`, `plt.ylabel` |
| Module-level `COUNTRY = "France"` | Constant habit | Put it inside `main()` or pass as a parameter |
| Reading the CSV directly with pandas | Skipping `load` | Import and call `load` from `load_csv` |

---

## 10. Debugging Guide

- **Empty chart / flat line:** check that `years` and `values` have the same length (`len(years) == len(values)`).
- **`KeyError: 'country'`:** the dataset loaded wrongly, or you already dropped the column. Print `data.columns[:3]`.
- **`ValueError: Country 'france' not found.`:** case matters. Print `data["country"].tolist()` to see the exact spelling.
- **Window does not appear (remote/WSL):** a GUI backend is needed; check `MPLBACKEND` or use a machine with a display.
- **Curve looks jagged:** that is real data (wars, epidemics), not a bug.

---

## 11. Cheat Sheet

```python
data = load("life_expectancy_years.csv")
row = data[data["country"] == country].iloc[0].drop("country")
years = [int(y) for y in row.index]
values = [float(v) for v in row.values]

plt.plot(years, values)
plt.title(f"{country} Life expectancy Projections")
plt.xlabel("Year")
plt.ylabel("Life expectancy")
plt.show()
```

---

## 12. Knowledge Checklist

- [ ] My program uses `load` from my own `load_csv.py`.
- [ ] The plot shows my campus's country with a title, an x label and a y label.
- [ ] Years are integers, so the x-axis ticks are readable.
- [ ] An unknown country or missing file prints a clear message instead of crashing.
- [ ] No global variables or global-scope code; `main()` present; docstrings everywhere; `flake8` clean.
