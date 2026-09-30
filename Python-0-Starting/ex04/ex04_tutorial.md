# Study Tutorial — Exercise 04: whatis.py

## 1. Exercise Overview

**What it asks:**
Write a script named `whatis.py` that takes one number as a command-line argument
and prints whether it is **Even** or **Odd**.

- If **no argument** is given, the script prints nothing and just exits.
- If **more than one argument** is given, print `AssertionError: more than one argument is provided`.
- If the argument **is not an integer**, print `AssertionError: argument is not an integer`.

**A note on structure:** unlike ex02 and ex03, this exercise does **not** ask you to
write a function with a prototype. The subject only requires you to wrap your code
in functions and a `main()` starting from Exercise 05 onward. So for `whatis.py`,
it's fine — and expected — to write it as a simple, direct script.

**Why this matters:**
In data science you will often run scripts from a terminal with arguments (a file
path, a batch size, a threshold...). Checking that the input is valid *before* using
it is what stops a bad argument from silently corrupting your results later on.

---

## 2. What You Already Know (and What's New)

You've completed ex00–ex03, so you already know:

- **Lists and indexing (ex00):** a list stores ordered items, and you read one item
  with `my_list[0]`, `my_list[1]`, etc.
- **`len()` (ex00/ex01 style tools):** counts how many items are in something.
- **Functions and `return` (ex02):** you can write `def f(x): ... return value`.
- **Conditionals (ex02, ex03):** `if`, `elif`, `else` to branch your code.

This exercise adds exactly **four** new ideas on top of that: `sys.argv`, `int()`,
`try ... except`, and `assert`. Nothing else. Let's take them one at a time.

---

## 3. New Concept #1: `sys.argv` — Arguments Are Just a List

When you run a script from the terminal:

```bash
python whatis.py 14
```

Python collects everything you typed into a **list of strings** called `sys.argv`.
You already know how to work with lists (ex00), so this isn't a new data structure —
just a new *source* for one.

```python
import sys

# When running: python whatis.py 14
print(sys.argv)        # ['whatis.py', '14']
```

Two things to remember:
1. `sys.argv[0]` is always the script's own name — not something the user typed.
2. Everything in `sys.argv` is a **string**, even `'14'`, not the number `14`.

Since you already know how to slice a list, you can grab just the user's arguments
(everything *except* the script name) like this:

```python
args = sys.argv[1:]   # drop index 0 (the script name)
print(len(args))      # how many arguments the user actually gave
```

- `len(args) == 0` → no argument was given.
- `len(args) == 1` → exactly one argument, `args[0]`.
- `len(args) > 1` → too many arguments.

This is exactly the kind of `if / elif / else` branching you already used in ex02/ex03
— just applied to `len(args)` instead of a type.

---

## 4. New Concept #2: `int()` and Why It Can Fail

`sys.argv` only ever gives you strings. To check if a number is even or odd, you
need an actual integer, so you convert it:

```python
number = int("14")   # number is now the integer 14
number = int("-5")    # works too, -5 is a valid integer
```

But what if the user types something that isn't a number, like `Hi!`?

```python
int("Hi!")   # Python raises: ValueError
```

This is called an **exception** — Python's way of saying "I can't do what you asked,
and if nobody handles it, the program will crash."

---

## 5. New Concept #3: `try ... except` — Catching the Failure

To stop that crash and handle it yourself, wrap the risky code in `try ... except`:

```python
text = "Hi!"

try:
    number = int(text)
    print("It worked:", number)
except ValueError:
    print("That wasn't a valid integer.")
```

- Python runs the `try` block first.
- If `int()` raises `ValueError`, Python jumps straight to the matching `except` block
  instead of crashing.
- If no error happens, the `except` block is simply skipped.

This is the tool that lets you check "is this argument a real integer?" safely.

**Common trap:** you might think you can check `"-5".isdigit()` instead. Don't — it
returns `False`, because the minus sign isn't a digit. `try / except` with `int()`
is the correct and simplest way to handle negative numbers too.

---

## 6. New Concept #4: `assert` and `AssertionError`

The subject asks you to **print** an `AssertionError` message in two specific cases.
`assert` is Python's built-in way to raise that exact kind of error:

```python
assert condition, "your message here"
```

If `condition` is `False`, Python raises `AssertionError("your message here")`.

You can also raise one directly, without a condition, when you already know
something is wrong:

```python
raise AssertionError("argument is not an integer")
```

Since an unhandled `AssertionError` would print an ugly multi-line traceback, and the
subject wants a single clean line, you catch it yourself — the same `try/except`
tool from section 5, just for a different exception type:

```python
try:
    ...  # your checks go here
except AssertionError as error:
    print(f"AssertionError: {error}")
```

---

## 7. The Modulo Operator (`%`) for Even and Odd

This part uses nothing new — just arithmetic and the `if/else` you already know:

- `14 % 2` is `0` → 14 is **Even**.
- `0 % 2` is `0` → 0 is **Even**.
- `-5 % 2` is `1` → -5 is **Odd**.

```python
if number % 2 == 0:
    print("I'm Even.")
else:
    print("I'm Odd.")
```

---

## 8. Putting It All Together

Since `whatis.py` doesn't require a `main()` yet (see section 1), a direct script
like this satisfies the subject:

```python
import sys

args = sys.argv[1:]

try:
    # Step 1: check argument count
    if len(args) == 0:
        sys.exit()  # no argument: exit silently, print nothing
    if len(args) > 1:
        raise AssertionError("more than one argument is provided")

    # Step 2: check it's really an integer
    try:
        number = int(args[0])
    except ValueError:
        raise AssertionError("argument is not an integer")

    # Step 3: even or odd
    if number % 2 == 0:
        print("I'm Even.")
    else:
        print("I'm Odd.")

except AssertionError as error:
    print(f"AssertionError: {error}")
```

Walk through it the same way you'd walk through an ex02/ex03 function: read top to
bottom, one `if` at a time.

1. **Zero arguments** → `sys.exit()` stops the script immediately, nothing is printed.
2. **More than one argument** → raise the first `AssertionError`, caught at the bottom
   and printed cleanly.
3. **One argument** → try to convert it with `int()`. If that fails, raise the second
   `AssertionError`.
4. **Valid integer** → use `%` to decide Even or Odd.

---

## 9. Guided Practice

These five drills are ordered from easiest to hardest. Each one adds exactly one
new requirement from the subject on top of the last, so that Practice 5 ends up
being the complete `whatis.py`. Try to write the code yourself and check it against
the **Expected output** table before opening the solution.

**Practice 1 (Easiest — just read and count the arguments):**
Write a script that prints how many arguments the user gave (not counting the
script name itself).

Expected output:

| Command | Output |
|---|---|
| `python practice.py` | `0` |
| `python practice.py 14` | `1` |
| `python practice.py 13 5` | `2` |

<details><summary>Solution</summary>

```python
import sys

args = sys.argv[1:]
print(len(args))
```
</details>

**Practice 2 (Branch on the count):**
Extend Practice 1: if there are zero arguments, exit without printing anything.
If there is more than one, print `AssertionError: more than one argument is
provided`. Otherwise, just print the single argument you received.

Expected output:

| Command | Output |
|---|---|
| `python practice.py` | *(nothing)* |
| `python practice.py 13 5` | `AssertionError: more than one argument is provided` |
| `python practice.py 14` | `14` |

<details><summary>Solution</summary>

```python
import sys

args = sys.argv[1:]

if len(args) == 0:
    sys.exit()
elif len(args) > 1:
    print("AssertionError: more than one argument is provided")
else:
    print(args[0])
```
</details>

**Practice 3 (Safely convert to an integer):**
Write a function `safe_convert(text)` that returns the integer value of `text`,
or `None` if `text` isn't a valid number. This reuses what you already know about
functions and `return` from ex02 — the only new part is the `try/except`.

Expected output:

| Call | Result |
|---|---|
| `safe_convert("14")` | `14` |
| `safe_convert("-5")` | `-5` |
| `safe_convert("Hi!")` | `None` |

<details><summary>Solution</summary>

```python
def safe_convert(text):
    """Convert text to an int, or return None if it fails."""
    try:
        return int(text)
    except ValueError:
        return None
```
</details>

**Practice 4 (Combine counting + conversion, still without AssertionError):**
Merge Practices 2 and 3: if there's exactly one argument, try to convert it. If
conversion fails, print a plain message instead of crashing. Don't check Even/Odd
yet — just prove the conversion step works inside the full branching logic.

Expected output:

| Command | Output |
|---|---|
| `python practice.py Hi!` | `Not a valid integer` |
| `python practice.py 14` | `Converted: 14` |
| `python practice.py -5` | `Converted: -5` |

<details><summary>Solution</summary>

```python
import sys

args = sys.argv[1:]

if len(args) == 0:
    sys.exit()
elif len(args) > 1:
    print("AssertionError: more than one argument is provided")
else:
    try:
        number = int(args[0])
        print("Converted:", number)
    except ValueError:
        print("Not a valid integer")
```
</details>

**Practice 5 (Hardest — the full exercise, with real `AssertionError`s):**
Now finish it properly: replace the plain `print` error messages from Practice 4
with real `raise AssertionError(...)` calls (see section 6), catch them once at
the bottom, and add the Even/Odd check with `%`. This is the complete `whatis.py`.

Expected output — check all six against your solution, they must match exactly:

| Command | Output |
|---|---|
| `python practice.py 14` | `I'm Even.` |
| `python practice.py -5` | `I'm Odd.` |
| `python practice.py` | *(nothing)* |
| `python practice.py 0` | `I'm Even.` |
| `python practice.py Hi!` | `AssertionError: argument is not an integer` |
| `python practice.py 13 5` | `AssertionError: more than one argument is provided` |

<details><summary>Solution</summary>

```python
import sys

args = sys.argv[1:]

try:
    if len(args) == 0:
        sys.exit()
    if len(args) > 1:
        raise AssertionError("more than one argument is provided")

    try:
        number = int(args[0])
    except ValueError:
        raise AssertionError("argument is not an integer")

    if number % 2 == 0:
        print("I'm Even.")
    else:
        print("I'm Odd.")

except AssertionError as error:
    print(f"AssertionError: {error}")
```
</details>

If all six outputs in Practice 5 match, rename your file to `whatis.py` — you're done.

---

## 10. Exact Expected Outputs (from the subject)

- `python whatis.py 14` → `I'm Even.`
- `python whatis.py -5` → `I'm Odd.`
- `python whatis.py 0` → `I'm Even.`
- `python whatis.py` → *(nothing printed)*
- `python whatis.py Hi!` → `AssertionError: argument is not an integer`
- `python whatis.py 13 5` → `AssertionError: more than one argument is provided`

Note that `0` counts as Even (`0 % 2 == 0`), and negative numbers work fine with `%`
(`-5 % 2 == 1`, so it's Odd).

---

## 11. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Using `"-5".isdigit()` | Returns `False` because `-` isn't a digit | Use `try: int(s) except ValueError:` |
| Printing something when 0 arguments are given | Assuming every run must output something | Check `if len(args) == 0` first and exit silently |
| `IndexError: list index out of range` | Reading `args[0]` before checking `len(args)` | Always check the length first |
| Forgetting `sys.argv[0]` is the script name | Confusing it with the first real argument | Use `args = sys.argv[1:]` |
| Letting `AssertionError` crash with a traceback | Not catching it | Wrap your logic in `try / except AssertionError as e` |

---

## 12. Knowledge Checklist

- [ ] I know `sys.argv` is a list of strings, and `sys.argv[0]` is the script name.
- [ ] I can slice it with `sys.argv[1:]` to get just the user's arguments — using
      list skills from ex00.
- [ ] I understand why `int("Hi!")` raises `ValueError`, and how `try/except` catches it.
- [ ] I can use `assert` or `raise AssertionError(...)` to signal bad input.
- [ ] I can catch `AssertionError` at the top level and print it as `AssertionError: <message>`.
- [ ] I know `0` and negative numbers are handled correctly by `%`.
- [ ] I understand `whatis.py` does not need a `main()` yet — that starts at ex05.