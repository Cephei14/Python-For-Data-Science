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
- Uncaught exceptions invalidate the exercise (including `AttributeError`, `NameError`, `KeyError`...).
- Docstrings on every function, `flake8` clean, explicit imports, Python 3.10+.

**What makes this exercise tricky (real-data problems):**
- Some GDP values are **text** with a suffix, like `"1.2k"` (USA) instead of `1200`.
- Some countries have **missing values** (empty cells, read as `NaN`) for 1900.
- The two files are **different datasets**: they may not list the same countries in the same order.
- `load()` can return `None` if a file is bad, so the code must check for it.

**Main concepts you'll learn:**
- Joining two tables by a shared key (`country`) with `merge`.
- Detecting and removing missing data with `dropna`.
- Converting text like `"1.2k"` into a number (`decode`) and applying it to a whole column with `.map`.
- Filtering rows with a boolean condition (needed for a log axis).
- Scatter plots, logarithmic axes, tick formatting, and legends.
- Safe error handling: checking for `None`, catching `KeyError`, leaving early with `return`.
- Reading a correlation from a chart, and its limits.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **`load()` from ex00:** returns a DataFrame or `None`.
- **Column access (ex00/ex01):** `data["1900"]`; the column names are **strings**, not integers.
- **Basic plot decoration (ex01/ex02):** `plt.title`, `plt.xlabel`, `plt.ylabel`, `plt.show`.
- **Scatter and log scale (your first version):** `plt.scatter(x, y)` and `plt.xscale("log")`.
- **Tick formatting (your first version):** `plt.gca().xaxis.set_major_formatter(EngFormatter(sep=""))`.
- **Dictionaries and `try/except`** basics from earlier modules.

Everything else used below (merge, dropna, map, legend, boolean filter, ...) is explained in section 4.

---

## 3. Tools and Libraries

| Tool / Syntax | What it does | Scope / Notes |
|---|---|---|
| `from load_csv import load` | Loads a CSV safely | Inherited from ex00; returns a DataFrame or `None` |
| `import matplotlib.pyplot as plt` | Plotting library | Explicit import |
| `from matplotlib.ticker import EngFormatter` | Formatter that writes `1000` as `1k` | Explicit import; used on the axis |
| `df is None` | Checks that `load` failed | Use `is None`, **not** `== None`. Check this **before** using `.empty` or any column |
| `df["1900"]` | Selects one column | Returns a `pd.Series`; column name is a string |
| `df[["country", "1900"]]` | Selects several columns | Returns a `pd.DataFrame` (note the double brackets) |
| `df1.merge(df2, on="country")` | Joins two tables on a shared column | **Inner join**: keeps only countries present in both |
| `merge(..., suffixes=("_income", "_life"))` | Renames the clashing columns after a merge | Both tables have a `1900` column, so they become `1900_income` and `1900_life` |
| `df.dropna()` | Removes rows containing `NaN` | A missing value can't be plotted |
| `df.dropna(subset=["x", "y"])` | Removes rows with `NaN` only in the listed columns | More precise than a bare `dropna()` |
| `float("nan")` | Creates a "not a number" value | Used by `decode` for invalid text |
| `isinstance(v, (int, float))` | Checks the type of a value | `True` if `v` is already a number |
| `text.strip()` | Removes spaces at both ends of a string | `" 1.2k "` becomes `"1.2k"` |
| `text[-1]` / `text[:-1]` | Last character / everything except the last | `"1.2k"[-1]` is `"k"`, `"1.2k"[:-1]` is `"1.2"` |
| `series.map(func)` | Applies a function to **each** value of a Series | Returns a new Series (here, floats) |
| `df["x"] = ...` | Creates (or overwrites) a column | Here: stores the converted numbers |
| `df["x"] > 0` | Creates a boolean mask | Series of `True`/`False` |
| `df[df["x"] > 0]` | Filters rows by a mask | Keeps rows where the mask is `True`; a log axis can't show `0` or negatives |
| `df.empty` | Checks if a DataFrame has 0 rows | `True` if nothing is left to plot |
| `except KeyError as e` | Catches a missing column / key | `e` holds the missing name |
| `return` (inside `main`) | Leaves the function immediately | Stops the program cleanly after an error message |
| `plt.scatter(x, y, label="...")` | Draws one dot per `(x, y)` pair | Not `plt.plot`; `label` is the text shown in the legend |
| `plt.xscale("log")` | Makes the x-axis logarithmic | Equal distances mean equal **ratios** |
| `plt.gca()` | "Get current axes": returns the axes object of the plot | Gives access to axis-level settings |
| `.xaxis.set_major_formatter(...)` | Chooses how the x tick labels are written | Used with `EngFormatter(sep="")` |
| `plt.legend()` | Draws the legend box | Only shows entries that have a `label=` |
| `plt.title("1900")` | Sets the title of the plot | Required by subject |
| `plt.xlabel("Gross domestic product")` | Labels the horizontal x-axis | Required by subject |
| `plt.ylabel("Life expectancy")` | Labels the vertical y-axis | Required by subject |
| `plt.show()` | Renders the visualization window | Blocks until the window is closed |

**Common pitfalls:**
- **Using `.values` on two separate tables.** `income["1900"].values` and `life["1900"].values` assume both files list the same countries in the same order. If they don't, the dots pair the wrong countries. **Merge on `country` instead.**
- **Never calling the converter.** Writing a `decode` function does nothing until you apply it (`.map(decode)`).
- **Missing values (NaN):** some countries have no 1900 data. Drop them explicitly.
- **Strings like `"1.2k"`:** check `data["1900"].dtype`; if it is `object`, some cells are text and need converting.
- **Linear x-axis:** GDP spans orders of magnitude; on a linear axis all dots clump on the left. Use `plt.xscale("log")`.
- **Zero or negative values on a log axis:** the log of `0` is undefined, so filter them out.
- **Wrong year:** columns are `"1900"` (string), not `1900` (int).
- **Using `plt.plot`:** it connects the dots with a line. Independent countries need `plt.scatter`.
- **Catching the wrong exception.** `income.empty` on `None` raises `AttributeError`, not `AssertionError`.
- **Continuing after an error.** If you only `print` the error, the code keeps running and crashes later with a `NameError`. Use `return`.

---

## 4. Concepts You Need to Learn

### 4.1 Why `.values` on two tables is risky
```python
i_data = income["1900"].values
l_data = life["1900"].values
plt.scatter(i_data, l_data)
```
This only works if row 0 of `income` is the same country as row 0 of `life`, row 1 the same as row 1, and so on. The two files come from different datasets: they can contain different countries or a different order. Matplotlib wouldn't complain, you'd simply get a **wrong plot**. The fix is to let pandas match the rows by country name (next section).

### 4.2 Joining two tables with `merge`
```python
data = income[["country", "1900"]].merge(
    life[["country", "1900"]],
    on="country",
    suffixes=("_income", "_life"),
)
```
Step by step:
- `income[["country", "1900"]]` keeps only the two columns we need (double brackets = list of columns = a DataFrame).
- `.merge(other, on="country")` matches rows that have the **same country name** in both tables.
- By default it is an **inner join**: a country that exists in only one file disappears.
- Both tables contain a column called `1900`. To avoid a clash, `suffixes=("_income", "_life")` renames them `1900_income` (from the left table) and `1900_life` (from the right table).

Result (one country appears once, with both values side by side):

| country | 1900_income | 1900_life |
|---|---|---|
| France | 4.2k | 43.4 |
| USA | 1.2k | 39.4 |

(Illustrative values.) Note that GDP may be text (`"4.2k"`) while life expectancy is a normal number.

### 4.3 Missing data (`NaN`)
An empty cell in a CSV is read by pandas as `NaN` ("not a number"). A point with a missing coordinate can't be drawn, so remove those rows:
```python
data = data.dropna(subset=["x", "y"])
```
`subset=[...]` means "only look for `NaN` in these columns". Without `subset`, `dropna()` checks every column. Remember to do this **after** converting the text to numbers (4.5), because bad text becomes `NaN` during the conversion.

### 4.4 Converting `"1.2k"` into `1200.0` (the `decode` function)
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
- `formats` is a dictionary mapping a suffix to its multiplier. `1e3` is `1000.0`, `1e6` is a million, `1e9` is a billion.
- `isinstance(text, (int, float))`: if the value is **already a number** (this includes `NaN`, which is a float), just return it as a float. Nothing to decode.
- `text.strip()` removes accidental spaces.
- `text and text[-1] in formats`: `text` alone is `False` for an empty string, which avoids an `IndexError` on `text[-1]`. If the last character is `k`, `M` or `B`:
  - `text[:-1]` is the number part (`"1.2"`), converted by `float(...)`,
  - `formats[text[-1]]` is the multiplier, so `"1.2k"` gives `1.2 * 1000 = 1200.0`.
- Otherwise it's plain text like `"850"`, so `float(text)` is enough.
- If the text is garbage (`"abc"`), `float` raises `ValueError`; we catch it and return `float("nan")`, which `dropna` will remove later. The program doesn't crash on bad data.

### 4.5 Applying a function to a whole column (`.map`)
```python
data["x"] = data["1900_income"].map(decode)
data["y"] = data["1900_life"].map(decode)
```
`series.map(decode)` calls `decode` on **every value** of the column and returns a new Series with the results. Assigning to `data["x"]` creates a **new column** `x`. Now `x` and `y` are guaranteed to be floats, whether the original cell was `1200`, `"1.2k"` or garbage.

### 4.6 Filtering rows with a boolean mask
```python
data = data[data["x"] > 0]
```
- `data["x"] > 0` gives a Series of `True`/`False`, one per row (a **mask**).
- `data[mask]` keeps only the rows where the mask is `True`.

Why here? On a logarithmic axis, `0` and negative numbers have no position (log of 0 is undefined). One bad GDP value could cause warnings or a missing dot, so we remove them first.

After all cleaning, check whether anything survived:
```python
if data.empty:
    print("Error: no valid data for 1900")
    return
```

### 4.7 Scatter plot with a label
```python
plt.scatter(data["x"], data["y"], label="Countries")
```
One dot per country: x is the GDP, y is the life expectancy. `plt.scatter` does not connect the dots (unlike `plt.plot`), which is right because countries are independent observations with no order. `label="Countries"` is the text that will appear in the legend.

### 4.8 Logarithmic axis and readable ticks
```python
plt.xscale("log")
plt.gca().xaxis.set_major_formatter(EngFormatter(sep=""))
```
- On a log axis, equal distances mean equal **ratios**: 300 to 1k to 10k are spaced roughly evenly. This spreads out the poorer countries and makes the relationship visible.
- `plt.gca()` returns the "current axes" (the drawing area). Through it you can change axis-level details.
- `xaxis.set_major_formatter(EngFormatter(sep=""))` tells matplotlib to write big ticks the engineering way: `1000` becomes `1k`, `10000` becomes `10k`. `sep=""` removes the space between the number and the suffix (`1k`, not `1 k`).

### 4.9 Legend
```python
plt.legend()
```
The subject asks for "a legend for each graph". `plt.legend()` draws a box listing every plotted series **that has a `label=`**. If you forget `label=` in `scatter`, matplotlib prints a warning and shows no legend entry. Call `plt.legend()` **after** the plotting calls.

### 4.10 Safe error handling (where the first version broke)
Three separate problems in the original structure:

1. **`load` returns `None` on failure.** Then `income.empty` raises `AttributeError`, which `except AssertionError` does not catch, so the program crashes. Check `is None` **first**:
   ```python
   if income is None or life is None:
       print("Error: could not load the data")
       return
   ```
2. **Printing an error is not stopping.** After `print(f"Error: {e}")` the old code kept going and hit `NameError` on `i_data`. Add `return` after every error message so `main` ends cleanly.
3. **Catch only what can really fail.** A missing `"1900"` column raises `KeyError`, so wrap just the column selection:
   ```python
   try:
       data = income[["country", "1900"]].merge(...)
   except KeyError as e:
       print(f"Error: missing column {e}")
       return
   ```

### 4.11 Correlation, not causation
In the picture, countries with a higher GDP tend to have a higher life expectancy: a **positive correlation**. But the cloud is wide (at a given GDP, life expectancy varies by 10+ years), and correlation does not prove that wealth *causes* longer life (public health, geography, data quality and other factors matter too). The log scale is also why the trend looks roughly linear.

---

## 5. Syntax and Examples

### Step-by-step snippet
```python
import matplotlib.pyplot as plt
import pandas as pd

income = pd.DataFrame(
    {"country": ["France", "USA", "Chad"], "1900": ["4.2k", "1.2k", None]}
)
life = pd.DataFrame(
    {"country": ["USA", "France", "Chad"], "1900": [39.4, 43.4, 31.0]}
)

# same countries, different order: merge handles it
data = income.merge(life, on="country", suffixes=("_income", "_life"))
print(data)
```
Output:
```
  country 1900_income  1900_life
0  France        4.2k       43.4
1     USA        1.2k       39.4
2    Chad        None       31.0
```
Notice that the rows were matched by name even though the order differed. Chad has a missing GDP and will be removed by `dropna` after conversion.

---

## 6. How to Think About the Exercise

1. **Step 1: Load both files** with `load`. If either is `None`, print a message and `return`.
2. **Step 2: Select `country` and `"1900"`** from each table and **merge on `country`**, with `suffixes`. Wrap in `try/except KeyError`.
3. **Step 3: Convert** both merged columns to floats with `.map(decode)` into new columns `x` and `y`.
4. **Step 4: Clean**: `dropna(subset=["x", "y"])`, then keep only `x > 0`.
5. **Step 5: Check** `data.empty`; if so, print a message and `return`.
6. **Step 6: Plot**: `scatter` with a `label`, `xscale("log")`, labels, title `1900`, `EngFormatter`, `legend`, `show`.
7. **Step 7: Answer the correlation question** for yourself (be ready to discuss it in the defence).

---

## 7. Guided Practice

**Practice 1 (Easiest, a scatter plot with a legend):**
Scatter `x = [1, 2, 3, 4]` against `y = [2, 4, 5, 8]` with a title, axis labels and a legend.

Expected output: four dots rising from left to right, with a legend entry `demo`.

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

**Practice 2 (Decode text numbers):**
Write `decode` and test it on `"1.2k"`, `"3M"`, `"2B"`, `"850"`, `5`, `"abc"`.

Expected output:
```
1200.0
3000000.0
2000000000.0
850.0
5.0
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
    for value in ["1.2k", "3M", "2B", "850", 5, "abc"]:
        print(decode(value))


if __name__ == "__main__":
    main()
```
</details>

**Practice 3 (Apply a function to a column with `.map`):**
Convert the Series `["1k", "2.5k", "300"]` with `decode`.

Expected output:
```
0    1000.0
1    2500.0
2     300.0
dtype: float64
```

<details><summary>Solution</summary>

```python
import pandas as pd


def decode(text: str | float) -> float:
    """Convert values like '1.2k' to float. Invalid -> nan."""
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
    """Map decode over a Series."""
    series = pd.Series(["1k", "2.5k", "300"])
    print(series.map(decode))


if __name__ == "__main__":
    main()
```
</details>

**Practice 4 (Merge two tables, different order):**
Merge `a = {"country": ["X", "Y", "Z"], "1900": [100, 200, 300]}` and `b = {"country": ["Z", "Y", "W"], "1900": [50, 40, 60]}` on `country` with suffixes `_income` and `_life`.

Expected output (only the countries present in both, matched by name):
```
  country  1900_income  1900_life
0       Y          200         40
1       Z          300         50
```

<details><summary>Solution</summary>

```python
import pandas as pd


def main() -> None:
    """Merge two tables by country."""
    a = pd.DataFrame({"country": ["X", "Y", "Z"], "1900": [100, 200, 300]})
    b = pd.DataFrame({"country": ["Z", "Y", "W"], "1900": [50, 40, 60]})
    print(a.merge(b, on="country", suffixes=("_income", "_life")))


if __name__ == "__main__":
    main()
```
</details>

**Practice 5 (Clean: `dropna` and boolean filter):**
Given a table with columns `x` and `y` where one row has `y = NaN` and another has `x = 0`, keep only valid rows.

Expected output: only the rows with a real `y` and `x > 0` remain.

<details><summary>Solution</summary>

```python
import pandas as pd


def main() -> None:
    """Remove NaN rows and non-positive x values."""
    data = pd.DataFrame(
        {
            "country": ["A", "B", "C", "D"],
            "x": [100.0, 200.0, 0.0, 400.0],
            "y": [30.0, float("nan"), 35.0, 40.0],
        }
    )
    data = data.dropna(subset=["x", "y"])
    data = data[data["x"] > 0]
    print(data)


if __name__ == "__main__":
    main()
```

Output: rows `A` and `D` (B has `NaN`, C has `x = 0`).
</details>

**Practice 6 (Log axis with readable ticks):**
Scatter `x = [300, 1000, 10000]`, `y = [25, 35, 50]` with a log x-axis, `EngFormatter` ticks, labels and a legend. The three dots should be roughly evenly spaced horizontally.

Expected output: three dots on a rising line, x ticks written like `1k` and `10k`.

<details><summary>Solution</summary>

```python
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter


def main() -> None:
    """Scatter with a logarithmic x-axis."""
    plt.scatter([300, 1000, 10000], [25, 35, 50], label="demo")
    plt.xscale("log")
    plt.xlabel("GDP")
    plt.ylabel("Life expectancy")
    plt.legend()
    plt.gca().xaxis.set_major_formatter(EngFormatter(sep=""))
    plt.show()


if __name__ == "__main__":
    main()
```
</details>

**Practice 7 (Hardest, the full rule-compliant `projection_life.py`):**

Expected output when running `python projection_life.py`: a window titled `1900` with x-axis `Gross domestic product` (log scale), y-axis `Life expectancy`, a legend `Countries`, and one dot per country present in both files with valid data.

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
    """Plot life expectancy against GDP per person for the year 1900."""
    income = load("income_per_person_gdppercapita_ppp_inflation_adjusted.csv")
    life = load("life_expectancy_years.csv")
    if income is None or life is None:
        print("Error: could not load the data")
        return

    try:
        data = income[["country", "1900"]].merge(
            life[["country", "1900"]],
            on="country",
            suffixes=("_income", "_life"),
        )
    except KeyError as e:
        print(f"Error: missing column {e}")
        return

    data["x"] = data["1900_income"].map(decode)
    data["y"] = data["1900_life"].map(decode)
    data = data.dropna(subset=["x", "y"])
    data = data[data["x"] > 0]  # log scale can't show 0 or negatives
    if data.empty:
        print("Error: no valid data for 1900")
        return

    plt.scatter(data["x"], data["y"], label="Countries")
    plt.xscale("log")
    plt.xlabel("Gross domestic product")
    plt.ylabel("Life expectancy")
    plt.title("1900")
    plt.legend()
    plt.gca().xaxis.set_major_formatter(EngFormatter(sep=""))
    plt.show()


if __name__ == "__main__":
    main()
```
</details>

---

## 8. Exercise-Specific Knowledge

- **The year is 1900**, used as the column name `"1900"` in both files.
- **Scatter, not line:** countries are independent observations; there is no order to connect.
- **One dot per country** that has valid data in **both** files for 1900.
- **Axis labels and title from the subject picture:** `Gross domestic product` (x), `Life expectancy` (y), title `1900`.
- **Log scale:** the picture's x-axis runs from 300 to 10k. `EngFormatter` produces `1k`/`10k` style labels automatically.
- **The two files are different datasets:** never assume the same row order or the same number of countries (`load` prints each shape; compare them).
- **`load` can return `None`:** always test `is None` before touching the DataFrame.
- **Discussion question (expect it in defence):** yes, a positive correlation is visible (richer countries tend to show longer lives), but it is loose and is not proof of causation.
- **Allowed libs:** you may use `seaborn` (`sns.scatterplot`) instead of matplotlib if you prefer, as long as it follows the same rules.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Wrong pairs of points | Used `.values` on two tables, assuming the same order | `merge(on="country")` |
| `decode` defined but nothing changes | Function never called | `data["x"] = data["1900_income"].map(decode)` |
| `ValueError` on `"1.2k"` | GDP given as text and passed to `float` directly | Use `decode` |
| `B` suffix not handled | Dictionary only had `k` and `M` | Add `"B": 1e9` |
| Crash on a bad string | No `try/except` around `float` | Return `float("nan")` on `ValueError` |
| `AttributeError: 'NoneType'...` | `load` returned `None` and code used `.empty` | Check `is None` first |
| `NameError` after an error message | Error printed but code kept running | `return` after each error |
| `KeyError: 1900` | Used an int instead of a string | `"1900"` |
| `KeyError: '1900_income'` | Suffix names differ from what was used later | Print `data.columns` and match them |
| Suffix columns `1900_x`, `1900_y` | Forgot `suffixes` | Pass `suffixes=("_income", "_life")` |
| Warnings or missing dots on log axis | `0` or negative values | `data = data[data["x"] > 0]` |
| Dots squashed at the left edge | Linear x-axis | `plt.xscale("log")` |
| Line joining all dots | Used `plt.plot` | `plt.scatter` |
| Empty legend / warning | Forgot `label=` or `plt.legend()` | `label="Countries"` and `plt.legend()` |
| Legend missing even with label | `plt.legend()` called before the plot | Call it after `scatter` |

---

## 10. Debugging Guide

- **`KeyError: '1900_income'`:** the suffix names differ from what you wrote; print `data.columns`.
- **Empty plot or "no valid data" message:** `data` is empty after cleaning. Print `len(data)` after the merge, after `dropna` and after the `x > 0` filter to see where rows disappear. Also check that both files spell country names the same way.
- **`TypeError` in `scatter` or `.map`:** values are still strings or `None`; print `data.dtypes` and `type(data["x"].iloc[0])`.
- **Ticks show `10^2`, `10^3`...:** the formatter was not applied; check that `plt.gca().xaxis.set_major_formatter(EngFormatter(sep=""))` runs (and that you used `xaxis`, not `yaxis`).
- **Everything on one side of the plot:** you forgot `plt.xscale("log")`, or the data isn't converted (still text).
- **Number of dots differs from the subject picture:** data versions differ; that's fine as long as every country with valid data in both files is plotted.
- **Quick data inspection:**
  ```python
  print(data.head())
  print(data.dtypes)
  print(data[["x", "y"]].describe())
  ```

---

## 11. Cheat Sheet

```python
income = load("income_per_person_gdppercapita_ppp_inflation_adjusted.csv")
life = load("life_expectancy_years.csv")
if income is None or life is None:
    return

data = income[["country", "1900"]].merge(
    life[["country", "1900"]], on="country", suffixes=("_income", "_life")
)
data["x"] = data["1900_income"].map(decode)    # "1.2k" -> 1200.0
data["y"] = data["1900_life"].map(decode)
data = data.dropna(subset=["x", "y"])          # remove missing data
data = data[data["x"] > 0]                     # log axis needs x > 0

plt.scatter(data["x"], data["y"], label="Countries")
plt.xscale("log")
plt.xlabel("Gross domestic product")
plt.ylabel("Life expectancy")
plt.title("1900")
plt.legend()
plt.gca().xaxis.set_major_formatter(EngFormatter(sep=""))
plt.show()
```

---

## 12. Knowledge Checklist

- [ ] Both datasets are loaded through my own `load` function, and I check `is None` before using them.
- [ ] Countries are matched by name with `merge` (never by row position) and I used `suffixes`.
- [ ] `decode` is actually applied with `.map` and handles `k`, `M`, `B` and invalid text.
- [ ] Missing values are removed with `dropna`, and non-positive GDP values are filtered out.
- [ ] The scatter shows year 1900 with a log x-axis, a title, both axis labels, `label=` and `plt.legend()`.
- [ ] Missing files, missing columns and empty results print a clear message and `return` instead of crashing.
- [ ] I can explain what `merge`, `dropna`, `.map`, `plt.gca()` and `EngFormatter` do.
- [ ] I can explain the correlation between GDP and life expectancy, and why it is not proof of causation.
- [ ] No globals, `main()` present, docstrings everywhere, `flake8` clean.
