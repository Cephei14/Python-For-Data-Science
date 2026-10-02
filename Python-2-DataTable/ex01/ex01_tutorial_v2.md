# Study Tutorial — Exercise 01: aff_life.py

## 1. Exercise Overview

**What it asks:**
Create a program `aff_life.py` (along with `load_csv.py`) in directory `ex01/` that:
1. Calls the `load` function from ex00.
2. Loads `life_expectancy_years.csv`.
3. Extracts the row of **your campus's country** (e.g., France, Japan, Germany, etc.).
4. Plots life expectancy against the years (1800 to 2100).
5. The graph must have a **title** and a **label on each axis** (`Year` on the x-axis, `Life expectancy` on the y-axis).

The subject's example is France: title `France Life expectancy Projections`, x-axis `Year`, y-axis `Life expectancy`, displaying a single blue line rising from ~30 in 1800 to ~92 in 2100, with noticeable drops during historical events such as the World Wars.

**Visualizing the Data Challenge:**
The dataset has dimensions `(195, 302)`:
- 195 rows (each representing a country).
- 302 columns (the first column is `"country"`, followed by 301 year columns `"1800"` through `"2100"`).

To plot the graph, you cannot pass a 2D DataFrame directly to Matplotlib. You must:
1. **Filter rows:** isolate the single row corresponding to your campus's country.
2. **Filter columns:** separate or exclude the non-numeric `"country"` label, keeping only the year columns.
3. **Transform data:** convert column headers (`"1800"`, `"1801"`...) into integer years for the x-axis, and the row values into floats for the y-axis.

**Rules and Constraints:**
- Files to turn in: `load_csv.py`, `aff_life.py`.
- Allowed libraries: `matplotlib`, `seaborn` or any data-visualization library, plus your `load_csv` module from ex00.
- No code in the global scope, no global variables. Everything must live inside functions (`main()`, helper functions).
- The file must contain a `main()` and the `if __name__ == "__main__":` guard.
- Any uncaught exception invalidates the exercise (e.g. invalid country name, missing file, corrupt CSV).
- Every function must have a docstring (`__doc__`).
- Code must adhere strictly to flake8 / PEP 8 norms.
- Use explicit imports (e.g. `import pandas as pd`, `import matplotlib.pyplot as plt`). Wildcard imports (`from pandas import *`) result in a score of 0.
- Python 3.10+.

**Main concepts you'll learn:**
- Indexing and selecting columns from a DataFrame (by name, slice, or condition).
- Filtering rows using boolean indexing (masks, conditions, `.loc`, and `.iloc`).
- Combined row and column filtering to extract clean 1D Series.
- Defensive handling when queries return empty results.
- Transforming DataFrame rows into plotting coordinates `(x, y)`.
- Creating and styling 2D line charts with `matplotlib.pyplot`.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **`load()` from ex00:** loads a CSV file into a `pd.DataFrame` and returns `None` on error.
- **DataFrame dimensions & structure:** shape `(rows, columns)` where rows represent observations and columns represent variables.
- **Python data structures:** iterating through dictionary-like objects, extracting `.index` and `.values`.
- **List comprehensions & type casting:** `[int(x) for x in list]` and `[float(y) for y in list]`.
- **Functions and defensive error handling:** `try` / `except`, catching exceptions and raising informative errors.

---

## 3. Tools and Libraries

| Tool / Syntax | What it does | Scope / Notes |
|---|---|---|
| `from load_csv import load` | Loads the dataset safely | Inherited from ex00 |
| `import matplotlib.pyplot as plt` | Plotting library | Explicit import |
| `df["country"]` | Selects a single column | Returns a `pd.Series` |
| `df[["country", "1800"]]` | Selects multiple columns | Returns a `pd.DataFrame` |
| `df.drop(columns=["country"])` | Drops specified columns from DataFrame | Returns DataFrame without column |
| `series.drop("country")` | Drops an entry from a Series | Used after selecting a single row |
| `df["country"] == "France"` | Creates a boolean mask | Series of `True`/`False` |
| `df[mask]` | Filters rows by boolean mask | Keeps rows where mask is `True` |
| `df.empty` | Checks if DataFrame has 0 rows | `True` if no rows matched filter |
| `df.iloc[0]` | Selects first row by integer position | Returns a `pd.Series` |
| `df.loc[mask, "1800":"2100"]` | Filters rows & columns simultaneously | Label-based selection (inclusive) |
| `df.set_index("country")` | Promotes `"country"` to row index | Enables direct `df.loc["France"]` |
| `series.index` | Labels of a Series (e.g. years) | Index object (iterable strings) |
| `series.values` | Data array of a Series | NumPy array of row values |
| `plt.plot(x, y)` | Draws a line connecting coordinates | `x` and `y` must have equal length |
| `plt.title("...")` | Sets title of the plot | Required by subject |
| `plt.xlabel("Year")` | Labels the horizontal x-axis | Required by subject |
| `plt.ylabel("Life expectancy")` | Labels the vertical y-axis | Required by subject |
| `plt.show()` | Renders the visualization window | Blocks until window is closed |

**Common Pitfalls:**
- **Plotting string years:** column headers after `read_csv` are strings (`"1800"`), not numbers. Plotting strings makes Matplotlib treat each year as an independent category, bunching up 301 overlapping text labels. Always convert years to `int`.
- **Unchecked empty results:** filtering for a misspelled or nonexistent country yields an empty DataFrame (`df.empty == True`). Calling `.iloc[0]` immediately crashes with `IndexError`. Always check `if rows.empty:` first.
- **Swapping axes:** placing Life Expectancy on the x-axis and Year on the y-axis fails the exercise requirement.
- **Not dropping the `"country"` label:** attempting to convert `"France"` to a float raises a `ValueError`.
- **Module-level global constants:** declaring `COUNTRY = "France"` outside functions breaches the "no global variables" rule. Keep variables inside functions.

---

## 4. Concepts You Need to Learn

### 4.1 Anatomy of a Pandas DataFrame
A Pandas DataFrame is a 2D tabular structure containing three core components:
1. **Values:** The 2D grid of data.
2. **Index (Rows):** The labels along the vertical axis (by default, integers `0, 1, 2, ...`).
3. **Columns:** The labels along the horizontal axis (e.g., `'country'`, `'1800'`, `'1801'`, ...).

```
                      Columns (df.columns)
            'country'    '1800'    '1801'  ...   '2100'
Index (row) +----------+---------+---------+-----+--------+
     0      | France   |  33.9   |  33.9   | ... |  92.5  |
     1      | Japan    |  36.4   |  36.4   | ... |  93.1  |
    ...     | ...      |  ...    |  ...    | ... |  ...   |
```

- When you select a **single row** or a **single column**, Pandas returns a **`Series`** (a 1D labelled array).
- When you select **multiple rows and columns**, Pandas returns a **`DataFrame`**.

---

### 4.2 Selecting and Filtering Columns

Throughout Module 2, you will need to select single years, subsets of years, or exclude metadata columns like `"country"`. Here are the essential techniques:

#### 1. Selecting a single column
- Bracket notation with a single string returns a `pd.Series`:
  ```python
  countries = data["country"]       # pd.Series of country names
  year_1900 = data["1900"]          # pd.Series of values for 1900 (used in ex03)
  ```
- Bracket notation with a list of strings returns a `pd.DataFrame`:
  ```python
  country_df = data[["country"]]     # pd.DataFrame with 1 column
  ```

#### 2. Selecting multiple columns
Pass a list of column names:
```python
sub_table = data[["country", "1800", "1900", "2000"]]
```

#### 3. Slicing columns by label range (`.loc`)
In ex02 you need years from 1800 to 2050. Rather than listing 251 column names manually, slice with `.loc`:
```python
# .loc[:, "start_col":"end_col"]
# Note: Label slicing in pandas INCLUDES the stop column!
years_up_to_2050 = data.loc[:, "1800":"2050"]
```

#### 4. Slicing columns by position (`.iloc`)
If you want all year columns and simply want to discard the first column (`"country"` at index `0`):
```python
# .iloc[:, 1:] means: all rows, columns from index 1 to the end
only_years = data.iloc[:, 1:]
```

#### 5. Dropping columns
To remove specific columns by name:
- On a DataFrame:
  ```python
  only_years = data.drop(columns=["country"])
  ```
- On a Series (a single extracted row):
  ```python
  clean_series = row.drop("country")
  ```

#### 6. Dynamic column filtering (List Comprehensions)
When you want columns matching a condition:
```python
# All columns that are pure digits
year_cols = [col for col in data.columns if col.isdigit()]

# All columns for years between 1800 and 2050 (for ex02)
range_cols = [col for col in data.columns if col.isdigit() and 1800 <= int(col) <= 2050]
```

---

### 4.3 Filtering Rows

Row filtering is how you isolate one or more countries from the 195 rows in the CSV.

#### 1. Boolean Indexing (Masks) Step-by-Step
Boolean indexing works in three stages:
1. **Define a condition:** `data["country"] == "France"`
2. **Generate a boolean mask:** Pandas compares each row's `"country"` value to `"France"`. This produces a `pd.Series` of `True` and `False` values of the same length as the DataFrame:
   ```python
   mask = data["country"] == "France"
   # 0     True
   # 1    False
   # ...
   ```
3. **Filter the DataFrame:** Passing the mask into `data[...]` preserves only the rows where the mask is `True`:
   ```python
   france_df = data[mask]
   ```

#### 2. Safe Checking for Missing Rows
If the user requests a country not in the CSV (e.g. `"Atlantis"`), the boolean mask contains only `False`, and `data[mask]` returns an **empty DataFrame**:
```python
rows = data[data["country"] == "Atlantis"]
print(rows.empty)   # True
print(len(rows))     # 0
```
**Never immediately call `.iloc[0]` on a filtered result.** Check `rows.empty` first:
```python
if rows.empty:
    raise ValueError(f"Country '{country}' not found in dataset.")
row_series = rows.iloc[0]
```

#### 3. Filtering by Multiple Row Conditions (AND, OR, NOT)
In ex02, you will need to filter two countries (e.g. France AND Belgium) at once.
- **AND (`&`):** Both conditions must be True.
- **OR (`|`):** At least one condition must be True.
- **NOT (`~`):** Inverts the boolean mask.

> [!IMPORTANT]
> In Python, bitwise operators (`&`, `|`, `~`) have higher operator precedence than comparison operators (`==`, `>`, `<`). You **must** wrap each condition in parentheses `(...)`, or Python will raise a `TypeError`!

```python
# Correct (parentheses around each comparison):
two_countries = data[(data["country"] == "France") | (data["country"] == "Belgium")]

# WRONG (will raise TypeError or give unexpected results):
# two_countries = data[data["country"] == "France" | data["country"] == "Belgium"]
```

#### 4. The `.isin()` Method
When checking if a column value matches any item in a collection:
```python
selected = data[data["country"].isin(["France", "Belgium", "Japan"])]
```

#### 5. Numeric Row Filtering
For exercises where you filter rows by data thresholds (e.g. ex03):
```python
# Countries with life expectancy in 1900 greater than 40
high_life = data[data["1900"] > 40]

# Countries where 1900 data is not missing (not NaN)
valid_1900 = data[data["1900"].notna()]
```

---

### 4.4 Advanced & Combined Filtering: `.loc`, `.iloc`, and Setting Indexes

Rather than filtering rows first and then filtering columns in separate lines, Pandas offers powerful unified tools.

#### 1. `.loc[row_selector, col_selector]` (Label-based)
`.loc` accepts `[row_condition, column_selection]` in a single bracket pair:
```python
# Filter row where country is France, and select year columns 1800 to 2100:
france_years = data.loc[data["country"] == "France", "1800":"2100"]
```
This directly returns a DataFrame with 1 row and 301 columns, completely omitting the `"country"` column without needing `.drop()`!

To turn that single row into a Series:
```python
series = data.loc[data["country"] == "France", "1800":"2100"].iloc[0]
```

#### 2. `.iloc[row_idx, col_idx]` (Position-based)
If you know the exact integer row index (e.g. first row `0`):
```python
# Row 0, columns 1 to the end:
first_country_series = data.iloc[0, 1:]
```

#### 3. Setting the Index (`.set_index`)
By default, DataFrame rows are indexed by numbers `0, 1, ...`. If you make `"country"` the index:
```python
indexed_data = data.set_index("country")
```
Now the country names ARE the row labels! You can query any country directly with `.loc`:
```python
france_series = indexed_data.loc["France"]               # Series of all years
france_series_2050 = indexed_data.loc["France", "1800":"2050"]  # Series 1800-2050
```

#### Summary of Row & Column Filtering Approaches

| Goal | Approach A (Step-by-step) | Approach B (`.loc` simultaneous) | Approach C (`.set_index`) |
|---|---|---|---|
| Filter 1 country & all years | `row = data[data["country"] == "France"].iloc[0].drop("country")` | `series = data.loc[data["country"] == "France", "1800":"2100"].iloc[0]` | `series = data.set_index("country").loc["France"]` |
| Filter 2 countries & 1800-2050 | `sub = data[data["country"].isin(["FR", "BE"])][["country"] + years]` | `sub = data.loc[data["country"].isin(["FR", "BE"]), "1800":"2050"]` | `sub = data.set_index("country").loc[["FR", "BE"], "1800":"2050"]` |

For `aff_life.py`, **Approach A** and **Approach B** are the most direct and widely understood.

---

### 4.5 Transforming Extracted Data for Matplotlib

Once you have isolated a row as a `pd.Series`, inspecting it reveals:
```python
print(series.index)   # Index(['1800', '1801', ..., '2100'], dtype='object')
print(series.values)  # array([33.9, 33.9, ..., 92.5], dtype=object or float64)
```

To plot this on a chart:
1. **X-axis values (Years):** Must be numbers.
   ```python
   years = [int(year) for year in series.index]
   ```
   *Why this matters:* If `years` were left as strings (`"1800"`, `"1801"`...), Matplotlib treats them as distinct categorical labels. It would attempt to write all 301 string labels across the bottom, creating an unreadable solid black bar of overlapping text. When converted to `int`, Matplotlib recognizes them as numeric coordinates and automatically chooses clean, readable ticks (e.g. `1800, 1840, 1880, 1920, 1960, 2000, 2040, 2080`).

2. **Y-axis values (Life Expectancy):** Must be floats.
   ```python
   values = [float(val) for val in series.values]
   ```

---

### 4.6 Anatomy of a Matplotlib Line Chart

Matplotlib follows a simple state-machine model:
```python
plt.plot(years, values)                    # 1. Plot the line (x, y)
plt.title("France Life expectancy Projections") # 2. Add title
plt.xlabel("Year")                         # 3. Add horizontal axis label
plt.ylabel("Life expectancy")              # 4. Add vertical axis label
plt.show()                                 # 5. Display the figure window
```

> [!WARNING]
> Be careful not to swap the labels!
> - The horizontal axis represents **time**, so `plt.xlabel("Year")`.
> - The vertical axis represents **life expectancy**, so `plt.ylabel("Life expectancy")`.

---

### 4.7 Why "Projections"?
The CSV dataset extends from 1800 through 2100. Any data beyond the present year represents demographic forecasts or projections computed by researchers at Gapminder. This explains why the subject specifies the title format `<Country> Life expectancy Projections`.

---

## 5. Syntax and Examples

### Pattern 1: Step-by-Step Row & Column Extraction
```python
# 1. Load data
data = load("life_expectancy_years.csv")
if data is None:
    return

# 2. Filter rows with boolean mask
target_country = "France"
rows = data[data["country"] == target_country]
if rows.empty:
    raise ValueError(f"Country '{target_country}' not found.")

# 3. Extract the first row as a Series and drop 'country'
row_series = rows.iloc[0].drop("country")

# 4. Convert index to integer years and values to floats
years = [int(col) for col in row_series.index]
values = [float(val) for val in row_series.values]
```

### Pattern 2: Unified `.loc` Extraction
```python
# Direct extraction of row condition and column range
filtered = data.loc[data["country"] == "France", "1800":"2100"]
if filtered.empty:
    raise ValueError("Country 'France' not found.")

series = filtered.iloc[0]
years = [int(y) for y in series.index]
values = [float(v) for v in series.values]
```

### Pattern 3: Complete Matplotlib Plotting
```python
plt.plot(years, values)
plt.title("France Life expectancy Projections")
plt.xlabel("Year")
plt.ylabel("Life expectancy")
plt.show()
```

---

## 6. How to Think About the Exercise

1. **Step 1: Load safely.** Use `load("life_expectancy_years.csv")`. If it returns `None`, terminate gracefully without crashing.
2. **Step 2: Choose your campus country.** Pick the country where your campus is located (e.g. `"France"`, `"Japan"`, `"Germany"`, etc.).
3. **Step 3: Filter the row.** Use a boolean mask `data["country"] == country`. If `rows.empty` is `True`, handle it defensively (e.g. raise `ValueError` caught by `main`).
4. **Step 4: Filter the columns.** Isolate the year columns and exclude `"country"` via `.drop("country")` or `.loc`.
5. **Step 5: Convert types.** Build `years` as `list[int]` and `values` as `list[float]`.
6. **Step 6: Render chart.** Call `plt.plot(years, values)`, add `plt.title(...)`, `plt.xlabel("Year")`, `plt.ylabel("Life expectancy")`, and call `plt.show()`.
7. **Step 7: Enforce clean architecture.** Encapsulate logic in functions, wrap execution in `try`/`except` inside `main()`, ensure docstrings and flake8 compliance.

---

## 7. Guided Practice

### Practice 1 (Easiest — Understanding Columns & Row Filtering):
Given a small DataFrame:
```python
import pandas as pd

df = pd.DataFrame({
    "country": ["France", "Japan", "Brazil"],
    "1800": [33.9, 36.4, 32.0],
    "1900": [45.0, 48.0, 38.5]
})
```
1. Print the `"country"` column.
2. Filter the DataFrame to keep only the row where `"country"` equals `"Japan"`.
3. Verify the type of the result (DataFrame) and check `len()` or `.empty`.

Expected output:
```
0    France
1     Japan
2    Brazil
Name: country, dtype: object

  country  1800  1900
1   Japan  36.4  48.0
Filtered row count: 1
```

<details><summary>Solution</summary>

```python
import pandas as pd

df = pd.DataFrame({
    "country": ["France", "Japan", "Brazil"],
    "1800": [33.9, 36.4, 32.0],
    "1900": [45.0, 48.0, 38.5]
})

# 1. Select the country column
print(df["country"])
print()

# 2. Filter rows for Japan
mask = df["country"] == "Japan"
japan_rows = df[mask]
print(japan_rows)

# 3. Check count
print(f"Filtered row count: {len(japan_rows)}")
```
</details>

---

### Practice 2 (Selecting & Dropping Columns):
Using the same `df`:
1. Select only the year columns (`"1800"` and `"1900"`) by dropping `"country"`.
2. Select only the `"1900"` column as a `pd.Series`.
3. Slice the year columns using `.loc[:, "1800":"1900"]`.

Expected output:
```
   1800  1900
0  33.9  45.0
1  36.4  48.0
2  32.0  38.5

0    45.0
1    48.0
2    38.5
Name: 1900, dtype: float64
```

<details><summary>Solution</summary>

```python
import pandas as pd

df = pd.DataFrame({
    "country": ["France", "Japan", "Brazil"],
    "1800": [33.9, 36.4, 32.0],
    "1900": [45.0, 48.0, 38.5]
})

# 1. Drop the country column to keep only years
years_only = df.drop(columns=["country"])
print(years_only)
print()

# 2. Select a single year column as Series
print(df["1900"])
print()

# 3. Slicing with .loc
loc_years = df.loc[:, "1800":"1900"]
```
</details>

---

### Practice 3 (Extracting a Country's Row as a Series):
Extract `"Japan"` from `df` as a 1D `pd.Series` where the index contains only the years (`"1800"`, `"1900"`) and values are floats. Try both the `.iloc[0].drop()` approach and the `.loc` approach.

Expected output:
```
1800    36.4
1900    48.0
Name: 1, dtype: object
```

<details><summary>Solution</summary>

```python
import pandas as pd

df = pd.DataFrame({
    "country": ["France", "Japan", "Brazil"],
    "1800": [33.9, 36.4, 32.0],
    "1900": [45.0, 48.0, 38.5]
})

# Approach A: Boolean filter -> iloc[0] -> drop("country")
row_series_a = df[df["country"] == "Japan"].iloc[0].drop("country")
print(row_series_a)

# Approach B: Combined .loc
row_series_b = df.loc[df["country"] == "Japan", "1800":"1900"].iloc[0]
assert (row_series_a == row_series_b).all()
```
</details>

---

### Practice 4 (Safe Data Extraction Function):
Write a function `get_country_data(data: pd.DataFrame, country: str) -> tuple[list[int], list[float]]` that:
1. Filters the row for `country`.
2. Raises a `ValueError(f"Country '{country}' not found.")` if no row matches.
3. Converts the column headers to `list[int]` (`years`) and values to `list[float]` (`values`).
4. Returns `(years, values)`.
Test it with `"France"` and an invalid country `"Narnia"`.

Expected output:
```
Years: [1800, 1900]
Values: [33.9, 45.0]
Successfully caught error: Country 'Narnia' not found.
```

<details><summary>Solution</summary>

```python
import pandas as pd


def get_country_data(
    data: pd.DataFrame, country: str
) -> tuple[list[int], list[float]]:
    """Extract years and values for a given country."""
    rows = data[data["country"] == country]
    if rows.empty:
        raise ValueError(f"Country '{country}' not found.")
    series = rows.iloc[0].drop("country")
    years = [int(year) for year in series.index]
    values = [float(val) for val in series.values]
    return years, values


df = pd.DataFrame({
    "country": ["France", "Japan"],
    "1800": [33.9, 36.4],
    "1900": [45.0, 48.0]
})

years, values = get_country_data(df, "France")
print(f"Years: {years}")
print(f"Values: {values}")

try:
    get_country_data(df, "Narnia")
except ValueError as error:
    print(f"Successfully caught error: {error}")
```
</details>

---

### Practice 5 (Drawing a Labelled Matplotlib Chart):
Using `years = [1800, 1850, 1900, 1950, 2000]` and `values = [33.9, 38.0, 45.0, 65.0, 80.0]`:
Plot the line chart with:
- Title: `"France Life expectancy Projections"`
- X-axis label: `"Year"`
- Y-axis label: `"Life expectancy"`

<details><summary>Solution</summary>

```python
import matplotlib.pyplot as plt

years = [1800, 1850, 1900, 1950, 2000]
values = [33.9, 38.0, 45.0, 65.0, 80.0]

plt.plot(years, values)
plt.title("France Life expectancy Projections")
plt.xlabel("Year")
plt.ylabel("Life expectancy")
plt.show()
```
</details>

---

### Practice 6 (Hardest — The Complete, Rule-Compliant `aff_life.py`):
Create the full, norm-compliant `aff_life.py` script:
- Imports `load` from `load_csv.py`.
- Loads `life_expectancy_years.csv`.
- Filters your campus country (e.g. `"France"`).
- Handles errors cleanly with `try` / `except` inside `main()`.
- Flake8 clean, docstrings on every function, no global variables.

<details><summary>Solution</summary>

```python
"""Display the life expectancy projections of a campus country."""

import matplotlib.pyplot as plt
import pandas as pd
from load_csv import load


def get_country_data(
    data: pd.DataFrame, country: str
) -> tuple[list[int], list[float]]:
    """Extract the years and life expectancy values of one country.

    Args:
        data: DataFrame containing 'country' and year columns.
        country: The country name to search for.

    Returns:
        A tuple of (years, values).

    Raises:
        ValueError: If the country is not present in the dataset.
    """
    rows = data[data["country"] == country]
    if rows.empty:
        raise ValueError(f"Country '{country}' not found.")
    series = rows.iloc[0].drop("country")
    years = [int(year) for year in series.index]
    values = [float(val) for val in series.values]
    return years, values


def main() -> None:
    """Load dataset, filter campus country, and render projection plot."""
    try:
        country = "France"  # Set to your campus country (e.g. France, Japan)
        data = load("life_expectancy_years.csv")
        if data is None:
            return
        years, values = get_country_data(data, country)
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

## 8. Exercise-Specific Knowledge & Scope of Module 2

- **Campus Country Requirement:** The subject specifically asks for "the country information of your campus". For example:
  - 42 Paris / 42 Nice / 42 Angoulême -> `"France"`
  - 42 Tokyo -> `"Japan"`
  - 42 Heilbronn / 42 Berlin / 42 Wolfsburg -> `"Germany"`
  - 42 Seoul -> `"South Korea"`
  Check `data["country"].tolist()` if you are unsure of the exact spelling in the CSV.
- **Connection to Exercise 02 (`aff_pop.py`):**
  In ex02, you will need to filter **two** countries (`data["country"].isin([c1, c2])`) and restrict the columns to years **between 1800 and 2050** (`data.loc[:, "1800":"2050"]` or list comprehension).
- **Connection to Exercise 03 (`projection_life.py`):**
  In ex03, you will select a single year column (`"1900"`) from two separate tables, filter out missing entries (`.notna()`), and join/merge the tables on the `"country"` column.
- **No Global Scope:** In Python scripts, writing variables at the root indentation level (e.g. `country = "France"` or `data = load(...)`) places them in global scope. Evaluators check for this: all execution must be enclosed within `main()` or other functions.

---

## 9. Common Mistakes

| Mistake | Why it happens | How to Fix |
|---|---|---|
| `IndexError: single positional indexer is out-of-bounds` | Calling `.iloc[0]` when country was not found | Check `if rows.empty:` before calling `.iloc[0]` and raise a `ValueError` |
| `TypeError: cannot compare a dtyped [object] array...` | Combining conditions without parentheses: `data[data["a"] == 1 & data["b"] == 2]` | Wrap each condition in parentheses: `((data["a"] == 1) & (data["b"] == 2))` |
| Using `and` / `or` instead of `&` / `\|` | Python boolean keywords evaluate the truth value of the entire Series | Use bitwise `&` and `\|` for element-wise boolean operations on Series |
| X-axis is an illegible solid black blur | Years plotted as strings (`"1800"`), forcing categorical ticks | Convert years to integers: `[int(y) for y in series.index]` |
| Swapped axis labels | Confusion between x and y coordinates | Verify `plt.xlabel("Year")` (horizontal) and `plt.ylabel("Life expectancy")` (vertical) |
| `ValueError: could not convert string to float: 'France'` | Forgot to drop `"country"` column before converting values to float | Drop the column: `series = row.drop("country")` |
| `KeyError: 'country'` | Typo in column name or column already dropped | Check column spelling with `data.columns[:5]` |
| Hardcoded global variable | Defining `COUNTRY = "France"` at module level | Move `country = "France"` inside `main()` |

---

## 10. Debugging Guide

When your filtering or plotting does not behave as expected, test with these diagnostic steps:

1. **Inspect loaded DataFrame dimensions:**
   ```python
   print(data.shape)        # Should be (195, 302)
   print(data.columns[:5])  # Should start with ['country', '1800', '1801'...]
   ```
2. **Debug your boolean mask:**
   ```python
   mask = data["country"] == "France"
   print("Matches found:", mask.sum())  # Should be 1
   ```
3. **Inspect the extracted row:**
   ```python
   row = data[mask]
   print("Row shape:", row.shape)       # Should be (1, 302)
   ```
4. **Verify coordinates before plotting:**
   ```python
   print("Years count:", len(years), "First 3:", years[:3], "Type:", type(years[0]))
   print("Values count:", len(values), "First 3:", values[:3], "Type:", type(values[0]))
   assert len(years) == len(values), "Mismatched coordinate lengths!"
   ```
5. **No GUI window on remote servers / WSL:**
   If running on a remote headless server without an X display, `plt.show()` may raise an error or hang. In local evaluation (42 campus cluster), standard desktop displays work directly.

---

## 11. Cheat Sheet

### Filtering Anything in Module 2

```python
# --- ROW FILTERING ---
# Single exact match
df[df["country"] == "France"]

# Multiple countries (OR)
df[(df["country"] == "France") | (df["country"] == "Belgium")]

# Using .isin()
df[df["country"].isin(["France", "Belgium"])]

# Numeric condition
df[df["1900"] > 40]

# Non-null values
df[df["1900"].notna()]

# --- COLUMN FILTERING ---
# Single column as Series
df["country"]

# Multiple columns
df[["country", "1800", "1900"]]

# Drop column from DataFrame
df.drop(columns=["country"])

# Drop label from Series
series.drop("country")

# Slicing column range by label (inclusive!)
df.loc[:, "1800":"2050"]

# Slicing columns by position (skip first column)
df.iloc[:, 1:]

# --- COMBINED ROW & COLUMN FILTERING ---
# Simultaneous row mask and column range
df.loc[df["country"] == "France", "1800":"2100"].iloc[0]

# --- CONVERTING TO PLOT LISTS ---
years = [int(y) for y in series.index]
values = [float(v) for v in series.values]

# --- PLOTTING ---
plt.plot(years, values)
plt.title("<Country> Life expectancy Projections")
plt.xlabel("Year")
plt.ylabel("Life expectancy")
plt.show()
```

---

## 12. Knowledge Checklist

- [ ] I understand how boolean indexing works (generating a mask of `True`/`False` and applying it to a DataFrame).
- [ ] I know how to select single columns, multiple columns, slice columns with `.loc`, and drop unwanted columns.
- [ ] I always wrap multiple boolean conditions in parentheses `(cond1) & (cond2)`.
- [ ] I defensively verify that a filtered result is not empty (`if rows.empty:`) before accessing `.iloc[0]`.
- [ ] I understand why year column labels must be converted to `int` so Matplotlib creates clean numeric ticks rather than overlapping text categories.
- [ ] My graph has the correct title, with `Year` on the x-axis and `Life expectancy` on the y-axis.
- [ ] The code is wrapped cleanly in `main()`, functions contain docstrings, imports are explicit, and there are no global variables.
