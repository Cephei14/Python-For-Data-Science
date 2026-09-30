# Study Tutorial — Exercise 01: format_ft_time.py

## 1. Exercise Overview

**What it asks:** Write a script that prints the current time twice, in two different formats:
1. Seconds since January 1, 1970 (the "Unix epoch"), formatted with thousands separators, plus the same number in scientific notation.
2. The current date formatted like `Oct 21 2022`.

**Main concepts you'll learn:**
- What "Unix time" / "epoch time" is and why computers use it
- Getting the current time in Python (`time` and `datetime` modules)
- Formatting numbers (commas as thousands separators, scientific notation)
- Formatting dates into custom human-readable strings

**Why this matters:** Timestamps are everywhere in data science — log files, sensor readings, stock prices, database rows. You constantly need to convert between "a number of seconds" (great for computers, for sorting and math) and "a human-readable date" (great for reports and plots). This exercise is your first hands-on contact with that conversion.

**Skills after completing it:**
- Fetch the current time as a raw float
- Format floats with custom separators and notations using Python's f-string mini-language
- Format a `datetime` object into an arbitrary string pattern

---

## 2. Prerequisites

- Basic Python: variables, `print()`, importing modules (`import time`)
- f-strings: `f"{value}"` syntax for inserting a variable into a string

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `time.time()` | Returns the current time as a float — seconds since Jan 1, 1970 UTC | This *is* "seconds since epoch" |
| `datetime.datetime.now()` | Returns a `datetime` object representing right now | Richer than `time.time()`; has year/month/day/etc. as attributes |
| `datetime.strftime(pattern)` | Converts a `datetime` object into a formatted string | You supply a pattern using format codes like `%b`, `%d`, `%Y` |
| f-string format specs (`f"{x:,.4f}"`, `f"{x:.2e}"`) | Control how a number is displayed | `,` = thousands separator, `.Nf` = N decimal places, `e` = scientific notation |

Common pitfalls:
- Confusing `time.time()` (a plain float) with `datetime.now()` (a rich object) — you need **both** kinds of formatting in this exercise, so you'll likely use both.
- Forgetting that `strftime` codes are case-sensitive: `%m` is month-as-number, `%M` is minutes.

---

## 4. Concepts You Need to Learn

### 4.1 Epoch time
Computers often store time as a single number: the number of seconds elapsed since a fixed reference point, `1970-01-01 00:00:00 UTC`. This is called "Unix time" or "epoch time." It's easy to store, compare, and do math with (subtracting two epoch times gives you a duration in seconds).

### 4.2 f-string format specifiers
An f-string lets you embed a formatting instruction right inside `{}`:
```python
value = 1234567.891
print(f"{value:,.2f}")
```
The part after the colon is the **format spec**:
- `,` → insert commas every three digits
- `.2f` → show exactly 2 digits after the decimal point, as a fixed-point number
- `.2e` → show in scientific notation with 2 digits after the decimal

### 4.3 `strftime` — "string format time"
`strftime` takes a `datetime` object and a pattern string, and produces a formatted string. Common codes:

| Code | Meaning | Example |
|---|---|---|
| `%b` | Abbreviated month name | `Oct` |
| `%d` | Zero-padded day of month | `21` |
| `%Y` | 4-digit year | `2022` |

---

## 5. Syntax and Examples

### Getting epoch time
```python
import time
now = time.time()
print(now)  # e.g. 1666355857.3622341
```
`time.time()` takes no arguments and returns a `float`.

### Getting both epoch time and formatted date cleanly
A `datetime` object can give you **both** the epoch seconds and the formatted date from a single call, ensuring they stay perfectly synchronized:
```python
from datetime import datetime

now = datetime.now()
epoch = now.timestamp()                  # float: seconds since Jan 1, 1970
formatted_date = now.strftime("%b %d %Y") # str: e.g. "Oct 21 2022"
```

### Formatting with commas and decimals
```python
value = 1666355857.3622341
print(f"{value:,.4f}")  # 1,666,355,857.3622
```
The `,` groups digits into thousands; `.4f` formats as float with exactly 4 decimal places.

### Scientific notation
```python
value = 1666355857.3622341
print(f"{value:.2e}")  # 1.67e+09
```
`.2e` formats as exponential (scientific) notation with 2 decimal places.

### Splitting long f-strings cleanly (PEP 8 / flake8)
The required first sentence is over 80 characters long. To respect PEP 8's 79-character line limit without adding extra newlines, use implicit string concatenation inside parentheses:
```python
print(f"Seconds since January 1, 1970: {epoch:,.4f} or "
      f"{epoch:.2e} in scientific notation")
```
Python automatically joins adjacent string literals inside parentheses into one single string.

---

## 6. How to Think About the Exercise

1. You need **one moment in time**, expressed in two different ways. Grab it once with `datetime.now()` (or `time.time()`) and derive both representations from that single snapshot. Calling time functions multiple times can theoretically straddle a second/day boundary and cause subtle desyncs.
2. Note that `datetime` objects have `.timestamp()` (returns seconds since epoch as float) and `.strftime()` (formats date to string).
3. Use a single f-string for line 1, rather than passing multiple arguments separated by commas to `print()`. Comma-separated `print()` can easily introduce unintentional spaces or style errors.
4. Format line 2 using `strftime("%b %d %Y")` — `%b` is the abbreviated month (`Oct`), `%d` is the zero-padded day (`21`), and `%Y` is the 4-digit year (`2022`).

---

## 7. Guided Practice

**Practice 1 (Easy):** Print the number `9876543.21` with comma separators and 2 decimal places.
<details><summary>Solution</summary>

```python
print(f"{9876543.21:,.2f}")  # 9,876,543.21
```
</details>

**Practice 2 (Easy):** Print the number `9876543.21` in scientific notation with 3 digits after the decimal.
<details><summary>Solution</summary>

```python
print(f"{9876543.21:.3e}")  # 9.877e+06
```
</details>

**Practice 3 (Medium):** Print today's date as `Day-Month-Year`, e.g. `21-10-2022`.
<details><summary>Hint</summary>Use `%d`, `%m`, `%Y` joined by hyphens.</details>
<details><summary>Solution</summary>

```python
from datetime import datetime
print(datetime.now().strftime("%d-%m-%Y"))
```
</details>

**Practice 4 (Close to the real exercise):** Get the current epoch time and print it as `"Epoch: X"` with commas and 4 decimals, on one line, then print the current date as `Mon DD YYYY` on the next line.
<details><summary>Solution</summary>

```python
from datetime import datetime
now = datetime.now()
epoch = now.timestamp()
print(f"Epoch: {epoch:,.4f}")
print(now.strftime("%b %d %Y"))
```
</details>

---

## 8. Exercise-Specific Knowledge

- Exact wording expected: `Seconds since January 1, 1970: <comma-formatted> or <scientific> in scientific notation`
- Second line: just the formatted date, no label.
- Your actual numbers will differ from the PDF's example (it's "right now" when you run it) — that's expected and fine; only the *format* is graded, not the exact digits.
- Allowed tools per the subject: `time`, `datetime`, or "any other library that allows you to receive the date" — no restriction beyond that.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Using `%M` instead of `%m`/`%b` for month | Code case confusion | Remember: uppercase `%M` = minutes, `%m` = numeric month, `%b` = month name |
| Printing `time.time()` directly without formatting | Forgetting the exercise wants a *specific* display format | Always run the value through an f-string format spec |
| Mismatched decimal places vs. the example | Copy-pasting without checking exact digit count | Re-read the subject's expected output carefully; match `.4f` / `.2e` etc. precisely |
| Two separate `datetime.now()` calls for the two lines | Not realizing this can (rarely) straddle a second boundary | Call `datetime.now()` once, reuse it for both outputs |
| Passing comma-separated args to `print()` with manual spaces | Leads to irregular spacing and PEP 8 E231/E203 errors | Use a single clean f-string instead |
| Flake8 error `E501 line too long (> 79 characters)` | Printing the long sentence on one line | Split the f-string across lines inside parentheses |

---

## 10. Debugging Guide

- **`AttributeError: module 'time' has no attribute 'strftime'` (when misused)** → `strftime` belongs to `datetime` objects, not the `time` module directly (there's a *different* `time.strftime` that takes a time-tuple, easy to confuse — stick to `datetime.strftime` for this exercise).
- **Output has no comma at all** → check you actually included `,` in the format spec, e.g. `{value:,.4f}` not `{value:.4f}`.
- **Wrong month abbreviation / numbers instead of letters** → double-check `%b` vs `%m`.
- Useful inspection: `print(type(now))` to confirm you have a `datetime` object, not a string, before calling `.strftime()` on it.

---

## 11. Cheat Sheet

```python
from datetime import datetime

now = datetime.now()
epoch = now.timestamp()          # float, seconds since 1970

f"{epoch:,.4f}"                  # 1,666,355,857.3622
f"{epoch:.2e}"                   # 1.67e+09
now.strftime("%b %d %Y")         # Oct 21 2022
```

Common `strftime` codes: `%Y` year, `%m` month(num), `%b` month(name), `%d` day, `%H` hour, `%M` minute, `%S` second.

---

## 12. Knowledge Checklist

- [ ] I can explain what epoch/Unix time is.
- [ ] I can get the current time as a float and as a `datetime` object.
- [ ] I can format a float with comma separators and fixed decimals.
- [ ] I can format a float in scientific notation.
- [ ] I can format a `datetime` into a custom string with `strftime`.
- [ ] I understand this timestamp formatting skill will reappear constantly in data-cleaning tasks later.
