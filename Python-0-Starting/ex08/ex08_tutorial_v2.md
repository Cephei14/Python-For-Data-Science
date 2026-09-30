# Study Tutorial — Exercise 08: Loading.py

## 1. Exercise Overview

**What it asks:**
Create a module named `Loading.py` containing a generator function `ft_tqdm(lst: range) -> None:`.
The function mimics Python's popular `tqdm` progress-bar library using the **`yield` operator**.

When tested with:
```python
from time import sleep
from tqdm import tqdm
from Loading import ft_tqdm

for elem in ft_tqdm(range(333)):
    sleep(0.005)
print()
for elem in tqdm(range(333)):
    sleep(0.005)
print()
```

Expected output for `ft_tqdm`:
```
100%|[===============================================================>]| 333/333
```
(Followed by real `tqdm`'s output for comparison).

**Main concepts you'll learn:**
- The **`yield`** keyword and **Generators** (producing values lazily).
- How `for` loops consume generators.
- Creating live-updating terminal animations using carriage returns (`\r`).
- Dynamically building visual progress bars.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **Loops and `range` (ex00, ex05):** Iterating through numbers with `for elem in range(...)`.
- **String Formatting (ex01):** Formatting numbers and strings into structured text with f-strings.
- **Functions and Docstrings (ex02, ex05):** Defining functions with type hints and adding `"""docstrings"""`.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `yield item` | Emits `item` and pauses execution until the next iteration | Makes the function a **Generator** |
| `print(..., end="\r", flush=True)` | Prints text and moves the cursor to the start of the line | Overwrites the same terminal line |
| `len(lst)` | Gets total number of elements to process | Used to compute percentage |
| `enumerate(lst)` | Yields `(index, item)` pairs during iteration | Helps track current progress |
| `import time` | (Optional) Measures elapsed time | Used for calculating speed (`it/s`) |

Common pitfalls:
- Using `return` instead of `yield`: A generator *must* use `yield`. Using `return` would immediately stop iteration after the first item!
- Forgetting `end="\r"`: Using standard `print()` prints a newline every iteration, spamming 333 separate lines to the terminal instead of updating in place!
- Forgetting `flush=True`: In some terminals, output is buffered and won't appear smoothly unless flushed immediately.

---

## 4. Concepts You Need to Learn

### 4.1 Understanding `yield` and Generators

In Exercise 02, you learned that functions use `return` to send a result back:
```python
def get_numbers():
    return [1, 2, 3]  # Computes everything upfront and exits
```

A **generator** function uses `yield` instead of `return`:
```python
def my_generator():
    yield "first"
    yield "second"
    yield "third"

for item in my_generator():
    print(item)
```

**How `yield` works step-by-step:**
1. When the `for` loop asks for the first item, `my_generator()` runs until it reaches `yield "first"`.
2. It **pauses** right there and gives `"first"` to the loop.
3. When the loop asks for the second item, the function **resumes** exactly where it paused, continuing until `yield "second"`.
4. It repeats this until the function finishes.

This is called **lazy evaluation**—values are generated one at a time, right when they are needed.

### 4.2 Why `yield` is Essential for a Progress Bar

Think about how the tester runs:
```python
for elem in ft_tqdm(range(333)):
    sleep(0.005)  # Caller does some slow work here!
```
Before giving `elem` to the caller, `ft_tqdm`:
1. Calculates the percentage completed so far.
2. Draws the progress bar on the terminal.
3. `yield elem` $\rightarrow$ gives the element to the caller.
4. The caller sleeps for 0.005s.
5. On the next loop cycle, `ft_tqdm` wakes up, updates the progress bar to the next step, and yields again!

### 4.3 Overwriting Lines in the Terminal (`\r`)

In standard printing:
```python
print("Hello")  # Adds a newline '\n' -> moves to next line
```
If you pass `end="\r"`:
```python
print("Hello", end="\r", flush=True)
```
`\r` is the **carriage return** character. It tells the terminal cursor to jump back to the **start of the current line** without advancing to a new line.

If you immediately print something else with `end="\r"`, it overwrites the existing text!

```python
import time

for i in range(1, 6):
    print(f"Counting: {i}", end="\r", flush=True)
    time.sleep(0.5)
print()  # Final print to move to a new line when done!
```

### 4.4 Constructing the Progress Bar String

Look at the subject's target visual:
```
100%|[===============================================================>]| 333/333
```
Let's break down the components:
1. **Percentage:** `f"{percent:3d}%|"` (padded to 3 digits, e.g. ` 50%|`, `100%|`).
2. **Bar bracket start:** `[`
3. **Bar body:** A series of `=` signs, ending with a `>`, padded with spaces.
   - For example, if bar width is 40 characters:
     - `filled_len = int(progress_ratio * bar_width)`
     - `bar = "=" * (filled_len - 1) + ">" + " " * (bar_width - filled_len)`
4. **Bar bracket end:** `]|`
5. **Count:** `f" {current}/{total}"`

---

## 5. Syntax and Examples

### A Simple Generator Progress Bar

```python
def ft_tqdm(lst: range):
    """Decorate an iterable with a visual progress bar."""
    total = len(lst)
    bar_width = 63  # standard bar width matching subject example

    for i, item in enumerate(lst, start=1):
        # Calculate progress
        percent = int((i / total) * 100)
        filled = int((i / total) * bar_width)

        if filled > 0:
            bar = "=" * (filled - 1) + ">" + " " * (bar_width - filled)
        else:
            bar = " " * bar_width

        # Print live-updating line
        output = f"{percent:3d}%|[{bar}]| {i}/{total}"
        print(output, end="\r", flush=True)

        # Hand item over to the caller
        yield item

    # Print newline when iteration is complete
    print(end="")
```

---

## 6. How to Think About the Exercise

1. **Step 1: Get the total count.**
   - Compute `total = len(lst)`.
2. **Step 2: Loop through `lst` using `enumerate(lst, start=1)`.**
   - Track current index `i` from `1` to `total`.
3. **Step 3: Render the progress string.**
   - Calculate percentage: `int((i / total) * 100)`.
   - Build the bar using `=` characters and `>` for the cursor head.
   - Assemble `f"{percent}%|[{bar}]| {i}/{total}"`.
4. **Step 4: Print with `end="\r"` and `flush=True`.**
5. **Step 5: `yield item`.**
   - Let the caller execute their iteration work.

---

## 7. Guided Practice

These five drills go from easiest to hardest, each adding one requirement from the
subject, until Practice 5 reproduces the complete `ft_tqdm`.

**Practice 1 (Easiest — a plain generator):**
Write a generator function `countdown(n)` that yields numbers from `n` down to
`1`, using `yield` instead of `return` (section 4.1).

Expected output:

```python
for num in countdown(3):
    print(num)
# 3
# 2
# 1
```

<details><summary>Solution</summary>

```python
def countdown(n: int):
    """Yield numbers from n down to 1."""
    while n > 0:
        yield n
        n -= 1
```
</details>

**Practice 2 (Overwrite a line instead of printing many):**
Write a loop that prints percentages from `0%` to `100%` in increments of 10, all
on the **same terminal line**, using `end="\r"` and `flush=True` (section 4.3).

Expected behavior: your terminal shows one line that updates in place, ending on
`Progress: 100%`, instead of 11 separate lines.

<details><summary>Solution</summary>

```python
import time

for p in range(0, 101, 10):
    print(f"\rProgress: {p:3d}%", end="", flush=True)
    time.sleep(0.1)
print()
```
</details>

**Practice 3 (Build the bar string, no percentage or `\r` yet):**
Write `render_bar(current, total, width=20)` that returns just the bracketed bar
part (no percentage, no counts) — for example `[=========>          ]`. This
isolates the trickiest piece of arithmetic from section 4.4.

Expected output:

```python
print(render_bar(50, 100))   # [=========>          ]
print(render_bar(100, 100))  # [===================>]
```

<details><summary>Solution</summary>

```python
def render_bar(current: int, total: int, width: int = 20) -> str:
    """Return a bracketed progress bar of specified width."""
    ratio = current / total
    filled = int(ratio * width)
    if filled > 0:
        bar = "=" * (filled - 1) + ">" + " " * (width - filled)
    else:
        bar = " " * width
    return f"[{bar}]"
```
</details>

**Practice 4 (Combine bar + percentage + counts, printed but not yielding yet):**
Merge Practices 2 and 3: for each step from `1` to `total`, print the full line
`f"{percent:3d}%|{bar}| {i}/{total}"` on the same terminal line with `\r`. Still
use a normal loop (no `yield` yet) so you can check the printed text is correct
before turning it into a generator.

Expected final line for a loop over `range(5)` (i.e. `total = 5`):

```
100%|[=================>]| 5/5
```

<details><summary>Solution</summary>

```python
import time


def show_progress(total: int, width: int = 20) -> None:
    """Print a progress bar for `total` steps, one line at a time."""
    for i in range(1, total + 1):
        percent = int((i / total) * 100)
        bar = render_bar(i, total, width)
        print(f"{percent:3d}%|{bar}| {i}/{total}", end="\r", flush=True)
        time.sleep(0.1)
    print()
```
</details>

**Practice 5 (Hardest — turn it into the real `ft_tqdm` generator):**
Turn Practice 4 into a generator: instead of just looping internally, iterate over
`lst`, print the progress line for each item, then `yield` that item so the
caller can do their own work (e.g. `sleep`) between steps — this is what makes it
behave like the real `tqdm`. Use the subject's bar width of 63 characters.

Expected output for `for elem in ft_tqdm(range(333)): sleep(0.005)`, at the final
step:

```
100%|[===============================================================>]| 333/333
```

<details><summary>Solution</summary>

```python
def ft_tqdm(lst: range) -> None:
    """Decorate an iterable with a custom tqdm progress bar."""
    total = len(lst)
    if total == 0:
        return

    bar_len = 63

    for i, elem in enumerate(lst, start=1):
        ratio = i / total
        percent = int(ratio * 100)
        filled = int(ratio * bar_len)

        if filled > 0:
            bar = "=" * (filled - 1) + ">" + " " * (bar_len - filled)
        else:
            bar = " " * bar_len

        print(f"{percent:3d}%|[{bar}]| {i}/{total}", end="\r", flush=True)
        yield elem
```
</details>

If your Practice 5 output matches, save it as `Loading.py` — you're done.

---

## 8. Exercise-Specific Knowledge

- **Subject Target Output:**
  ```
  100%|[===============================================================>]| 333/333
  ```
  Notice:
  - Percentage: `100%|`
  - Opening: `[`
  - Body: 63 `=` signs ending in `>` when complete: `===============================================================>`
  - Closing: `]|`
  - Current/Total: ` 333/333`
- **Prototype:**
  `def ft_tqdm(lst: range) -> None:`
  *(Note: The subject prototype specifies `-> None`. Even though a generator produces items, keep the prototype as requested).*

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Newline printed every step | Default `print()` adds `\n` | Use `end="\r", flush=True` |
| Using `return` inside generator | Habits from regular functions | Use `yield item` |
| Off-by-one in count (`332/333`) | Starting `enumerate` at 0 | Use `enumerate(lst, start=1)` |
| Missing docstring | Subject rule requires `__doc__` | Add `"""Docstring."""` right below `def` |

---

## 10. Debugging Guide

- **Terminal output jumps or scrolls vertically**: Ensure `print()` strictly has `end="\r"` and that no other `print()` statements are called inside the loop.
- **Progress bar gets stuck**: Check `flush=True`. In some shell configurations, unbuffered stdout is required for `\r` updates.

---

## 11. Cheat Sheet

```python
def ft_tqdm(lst: range) -> None:
    """Decorate an iterable with a custom tqdm progress bar."""
    total = len(lst)
    if total == 0:
        return

    bar_len = 63

    for i, elem in enumerate(lst, start=1):
        ratio = i / total
        percent = int(ratio * 100)
        filled = int(ratio * bar_len)

        if filled > 0:
            bar = "=" * (filled - 1) + ">" + " " * (bar_len - filled)
        else:
            bar = " " * bar_len

        print(f"{percent:3d}%|[{bar}]| {i}/{total}", end="\r", flush=True)
        yield elem
```

---

## 12. Knowledge Checklist

- [ ] I understand the difference between `return` (exit) and `yield` (pause & resume).
- [ ] I can explain what a generator is and how a `for` loop consumes it.
- [ ] I can overwrite terminal lines using `print(..., end="\r", flush=True)`.
- [ ] I can dynamically construct a progress bar string matching the subject.
- [ ] My implementation passes `flake8` with zero warnings.
