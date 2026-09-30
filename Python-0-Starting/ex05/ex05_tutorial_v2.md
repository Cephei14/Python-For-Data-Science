# Study Tutorial — Exercise 05: building.py

## 1. Exercise Overview

**What it asks:**
Build your first fully structured standalone program named `building.py`. The program takes a single string and counts its character composition:
- Total number of characters
- Uppercase letters (`isupper()`)
- Lowercase letters (`islower()`)
- Punctuation marks (`string.punctuation`)
- Spaces (`isspace()`, including newlines/carriage returns)
- Digits (`isdigit()`)

**Input conditions:**
1. If **no argument** (or `None` / empty) is provided on the command line, prompt the user in the terminal:
   `What is the text to count?`
2. If **more than one argument** is provided, print an `AssertionError: more than one argument is provided`.

**CRITICAL MILESTONE — The Additional Rules:**
From Exercise 05 onwards, the subject introduces strict architectural requirements that apply to **all remaining exercises**:
1. **No code in global scope:** All logic must live inside functions.
2. **Mandatory `main()` entry point:**
   ```python
   def main():
       # logic and error handling
   if __name__ == "__main__":
       main()
   ```
3. **No uncaught exceptions:** Any exception that crashes without being caught will give you a 0 on the exercise!
4. **All functions must have docstrings (`__doc__`).**
5. **Code must be at the norm:** Pass `flake8` with zero warnings.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **`sys.argv` (ex04):** You know how command-line arguments are stored in `sys.argv`.
- **`try ... except` & `AssertionError` (ex04):** Catching errors and asserting preconditions.
- **Lists and Strings (ex00):** You know that strings are sequences of characters that can be measured with `len()` and looped over.
- **Functions (ex02):** Defining functions with `def`.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `import sys` | Access system arguments and streams | `sys.argv`, `sys.stdin` |
| `import string` | Built-in module containing character sets | `string.punctuation` contains all standard punctuation characters |
| `char.isupper()` | Returns `True` if `char` is an uppercase letter | Built-in string method |
| `char.islower()` | Returns `True` if `char` is a lowercase letter | Built-in string method |
| `char.isdigit()` | Returns `True` if `char` is a digit `0`–`9` | Built-in string method |
| `char.isspace()` | Returns `True` if `char` is whitespace (spaces, `\t`, `\n`, `\r`) | Treats Enter (carriage return) as space! |
| `char in string.punctuation` | Checks if `char` belongs to standard punctuation | `!"#$%&'()*+,-./:;<=>?@[\]^_`{\|}~` |
| `sys.stdin.readline()` | Reads input from terminal preserving the newline `\n` | Matches the subject's exact character count! |
| `flake8` | Python code style checker ("norminette" for Python) | Enforces PEP 8 rules |

Common pitfalls:
- Using `input()` instead of `sys.stdin.readline()`: Standard `input()` strips the trailing newline `\n`. But the subject explicitly notes: *"the carriage return counts as a space, if you don't want to return one use ctrl + D"*. Using `sys.stdin.readline()` correctly keeps the newline, giving 13 characters (with 2 spaces) for `"Hello World!\n"`, exactly matching the subject!
- Missing docstrings: Forgetting `"""Documentation."""` on any function violates the subject's mandatory rule.
- Code in global scope: Writing any computation outside a function (except the `if __name__ == "__main__":` check) violates the subject's rules.

---

## 4. Concepts You Need to Learn

### 4.1 The 5 New Mandatory Rules Explained

#### Rule 1 & 2: No Global Code & The `main()` Guard
In earlier exercises, scripts could run top-level statements. From now on, your file must only contain:
1. Imports at the top.
2. Function definitions.
3. The guard at the very bottom:
```python
def count_characters(text: str) -> None:
    """Count and display character categories for a given string."""
    # logic here


def main():
    """Handle arguments and orchestrate program flow."""
    # call your functions here


if __name__ == "__main__":
    main()
```

#### Rule 3: Any Exception Not Caught Invalidates the Exercise
If your program crashes with an unhandled traceback during evaluation, you fail.
Always catch potential exceptions (such as `AssertionError` or `EOFError`) inside `main()`:
```python
def main():
    """Main program entry."""
    try:
        # validate and run
        ...
    except AssertionError as error:
        print(f"AssertionError: {error}")
```

#### Rule 4: Documentation (`__doc__`)
Every function you write must begin with a docstring inside triple quotes (`"""..."""`):
```python
def my_function(text: str) -> None:
    """This docstring explains what the function does."""
    print(text)

# Python exposes this string as:
print(my_function.__doc__)
```

#### Rule 5: The Norm (`flake8`)
42 uses `flake8` to enforce Python's PEP 8 style guide:
- **Indent with 4 spaces** (never use tabs: `W191`).
- **Maximum line length is 79 characters** (`E501`).
- **Two blank lines** between top-level functions (`E302`).
- **One newline at end of file** (`W292`).
- No trailing whitespace at end of lines (`W291`).

### 4.2 Classifying Characters One by One

Strings in Python can be looped over directly:
```python
text = "Hi 42!"

for char in text:
    print(char)
```
Each `char` is a single-character string with built-in helper methods:
- `"A".isupper()` $\rightarrow$ `True`
- `"a".islower()` $\rightarrow$ `True`
- `"4".isdigit()` $\rightarrow$ `True`
- `" ".isspace()` $\rightarrow$ `True`
- `"\n".isspace()` $\rightarrow$ `True` (newline counts as whitespace!)

For punctuation, Python does not have `.ispunctuation()`. Instead, `import string` provides `string.punctuation`:
```python
import string

print(string.punctuation)  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
print("!".strip() in string.punctuation)  # True
```

### 4.3 Handling Prompt Input and Carriage Return

When `python building.py` is run with no arguments:
The program must prompt:
```
What is the text to count?
```
Look at the subject's test:
```
What is the text to count?
Hello World!
The text contains 13 characters:
2 upper letters
8 lower letters
1 punctuation marks
2 spaces
0 digits
```
Let's count:
- `"Hello"` = 5 letters (1 upper, 4 lower)
- `" "` = 1 space
- `"World!"` = 6 characters (1 upper, 4 lower, 1 punctuation)
- **Total so far:** 5 + 1 + 6 = 12 characters (1 space).
- **Why does the output say 13 characters and 2 spaces?**
  Because the user pressed **Enter** to submit the line! The Enter key sends a newline `\n`.
  In Python, `"\n".isspace()` is `True`!
  If you use `sys.stdin.readline()`, it includes the `\n`, producing exactly **13 characters and 2 spaces**.
  If the user ended input with `Ctrl + D` (EOF), no newline is sent.

---

## 5. Syntax and Examples

### Inspecting Each Character

```python
import string

text = "Hello 42!\n"
upper = 0
lower = 0
digits = 0
spaces = 0
punct = 0

for char in text:
    if char.isupper():
        upper += 1
    elif char.islower():
        lower += 1
    elif char.isdigit():
        digits += 1
    elif char.isspace():
        spaces += 1
    elif char in string.punctuation:
        punct += 1

print(f"Total: {len(text)}")
print(f"Upper: {upper}, Lower: {lower}, Digits: {digits}, Spaces: {spaces}, Punct: {punct}")
```

### Reading from Argument or Standard Input

```python
import sys

if len(sys.argv) > 2:
    raise AssertionError("more than one argument is provided")
elif len(sys.argv) == 2:
    text = sys.argv[1]
else:
    # Prompt the user if no argument provided
    print("What is the text to count?")
    text = sys.stdin.readline()
```

---

## 6. How to Think About the Exercise

1. **Step 1: Check arguments.**
   - If `len(sys.argv) > 2`: raise `AssertionError("more than one argument is provided")`.
   - If `len(sys.argv) == 2`: use `sys.argv[1]`.
   - If `len(sys.argv) == 1` or input is empty/None: print `"What is the text to count?"` and read from `sys.stdin.readline()`.
2. **Step 2: Count characters.**
   - Initialize counters for upper, lower, punctuation, spaces, and digits.
   - Loop through `text`, check each condition with `elif` to ensure each character is counted in exactly one category.
3. **Step 3: Print results.**
   - Match the exact subject output labels:
     - `The text contains {total} characters:`
     - `{upper} upper letters`
     - `{lower} lower letters`
     - `{punct} punctuation marks`
     - `{spaces} spaces`
     - `{digits} digits`
4. **Step 4: Wrap everything in `main()` with `try ... except`.**

---

## 7. Guided Practice

These five drills go from easiest to hardest. Each one adds exactly one more piece
of the subject's requirements on top of the last, so that Practice 5 is the
complete, rule-compliant `building.py`. Try each one yourself and check it against
the **Expected output** before opening the solution.

**Practice 1 (Easiest — classify a single character):**
Write a function `classify_char(char)` that returns the string `"upper"`,
`"lower"`, `"digit"`, `"space"`, `"punct"`, or `"other"` depending on what kind of
character it is. This only uses the character methods from section 4.2 — no
loops, no CLI, no `main()` yet.

Expected output:

| Call | Result |
|---|---|
| `classify_char("A")` | `"upper"` |
| `classify_char("a")` | `"lower"` |
| `classify_char("4")` | `"digit"` |
| `classify_char(" ")` | `"space"` |
| `classify_char("!")` | `"punct"` |

<details><summary>Solution</summary>

```python
import string


def classify_char(char: str) -> str:
    """Return the category name of a single character."""
    if char.isupper():
        return "upper"
    elif char.islower():
        return "lower"
    elif char.isdigit():
        return "digit"
    elif char.isspace():
        return "space"
    elif char in string.punctuation:
        return "punct"
    return "other"
```
</details>

**Practice 2 (Tally a whole string):**
Reuse `classify_char` from Practice 1 inside a loop to count every category across
an entire string, and print the totals using the subject's exact labels.

Expected output for `count_text("Hi 42!")`:

```
The text contains 6 characters:
1 upper letters
1 lower letters
1 punctuation marks
1 spaces
2 digits
```

<details><summary>Solution</summary>

```python
def count_text(text: str) -> None:
    """Analyze and display counts of various character categories."""
    upper = lower = digits = spaces = punct = 0

    for char in text:
        category = classify_char(char)
        if category == "upper":
            upper += 1
        elif category == "lower":
            lower += 1
        elif category == "digit":
            digits += 1
        elif category == "space":
            spaces += 1
        elif category == "punct":
            punct += 1

    print(f"The text contains {len(text)} characters:")
    print(f"{upper} upper letters")
    print(f"{lower} lower letters")
    print(f"{punct} punctuation marks")
    print(f"{spaces} spaces")
    print(f"{digits} digits")
```
</details>

**Practice 3 (Read the text: argument or prompt, no error handling yet):**
Write a function that returns the text to analyze: if a CLI argument was given, use
it; otherwise print `What is the text to count?` and read a line with
`sys.stdin.readline()`. Don't worry about the "too many arguments" case yet.

Expected behavior:

| Command | What happens |
|---|---|
| `python practice.py 14` | returns `"14"` directly, no prompt |
| `python practice.py` then typing `Hi!` + Enter | prints the prompt, then returns `"Hi!\n"` |

<details><summary>Solution</summary>

```python
import sys


def read_text() -> str:
    """Return the CLI argument, or prompt the user if none was given."""
    if len(sys.argv) >= 2:
        return sys.argv[1]
    print("What is the text to count?")
    return sys.stdin.readline()
```
</details>

**Practice 4 (Add the argument-count guard):**
Extend Practice 3: if more than one argument is given, raise
`AssertionError("more than one argument is provided")` instead of silently using
the first one.

Expected output:

| Command | Output |
|---|---|
| `python practice.py 13 5` | `AssertionError: more than one argument is provided` |
| `python practice.py 14` | *(returns `"14"`, no error)* |

<details><summary>Solution</summary>

```python
import sys


def read_text() -> str:
    """Return validated input text from CLI argument or prompt."""
    if len(sys.argv) > 2:
        raise AssertionError("more than one argument is provided")
    elif len(sys.argv) == 2:
        return sys.argv[1]
    print("What is the text to count?")
    return sys.stdin.readline()
```

(Test the error case by wrapping the call in a `try/except AssertionError as e:
print(f"AssertionError: {e}")` the way you did in ex04.)
</details>

**Practice 5 (Hardest — assemble the full, rule-compliant program):**
Combine Practices 1, 2 and 4 into the final `building.py`: docstrings on every
function, all logic inside `main()`, and `AssertionError` caught cleanly (the
mandatory rules from section 4.1).

Expected output — check both against your solution:

```
$ python practice.py "Hello World!"
The text contains 12 characters:
2 upper letters
8 lower letters
1 punctuation marks
1 spaces
0 digits
```

```
$ python practice.py 13 5
AssertionError: more than one argument is provided
```

<details><summary>Solution</summary>

```python
import sys
import string


def classify_char(char: str) -> str:
    """Return the category name of a single character."""
    if char.isupper():
        return "upper"
    elif char.islower():
        return "lower"
    elif char.isdigit():
        return "digit"
    elif char.isspace():
        return "space"
    elif char in string.punctuation:
        return "punct"
    return "other"


def count_text(text: str) -> None:
    """Analyze and display counts of various character categories."""
    upper = lower = digits = spaces = punct = 0

    for char in text:
        category = classify_char(char)
        if category == "upper":
            upper += 1
        elif category == "lower":
            lower += 1
        elif category == "digit":
            digits += 1
        elif category == "space":
            spaces += 1
        elif category == "punct":
            punct += 1

    print(f"The text contains {len(text)} characters:")
    print(f"{upper} upper letters")
    print(f"{lower} lower letters")
    print(f"{punct} punctuation marks")
    print(f"{spaces} spaces")
    print(f"{digits} digits")


def read_text() -> str:
    """Return validated input text from CLI argument or prompt."""
    if len(sys.argv) > 2:
        raise AssertionError("more than one argument is provided")
    elif len(sys.argv) == 2:
        return sys.argv[1]
    print("What is the text to count?")
    return sys.stdin.readline()


def main():
    """Handle arguments and orchestrate program flow."""
    try:
        text = read_text()
        count_text(text)
    except AssertionError as error:
        print(f"AssertionError: {error}")


if __name__ == "__main__":
    main()
```
</details>

If both outputs in Practice 5 match, rename your file to `building.py` — you're done.

---

## 8. Exercise-Specific Knowledge

- **Exact Pluralization / Labels:**
  Notice the subject's exact wording:
  - `"X upper letters"`
  - `"X lower letters"`
  - `"X punctuation marks"` (even when count is 1: `1 punctuation marks`)
  - `"X spaces"`
  - `"X digits"`
- **Carriage Return / Enter key:**
  When prompting, pressing Enter appends `\n` to the input. `\n` counts towards total characters and spaces.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Using `input()` and getting 12 instead of 13 characters | `input()` strips `\n` | Use `sys.stdin.readline()` |
| Missing docstrings on functions | Subject rule: all functions need `__doc__` | Add `"""Docstring."""` right under each `def` |
| Code in global scope | Putting logic outside functions | Wrap logic inside helper functions and `main()` |
| Not catching exceptions | Subject rule: uncaught exceptions invalidate project | Wrap `main()` contents in `try ... except AssertionError:` |
| Flake8 warnings (lines > 79 chars, tabs) | C norm habits | Use 4 spaces, keep lines under 79 characters |

---

## 10. Debugging Guide

- **`flake8` reports `E302 expected 2 blank lines`**: Ensure there are exactly two empty lines before every top-level function.
- **`flake8` reports `W291 trailing whitespace`**: Delete any invisible spaces at the end of code lines.
- **Space count is off by 1 during interactive test**: Verify you are counting `\n` as whitespace (which `isspace()` does automatically).

---

## 11. Cheat Sheet

```python
import sys
import string


def count_text(text: str) -> None:
    """Count and print uppercase, lowercase, punctuation, spaces, and digits."""
    upper = sum(1 for c in text if c.isupper())
    lower = sum(1 for c in text if c.islower())
    digits = sum(1 for c in text if c.isdigit())
    spaces = sum(1 for c in text if c.isspace())
    punct = sum(1 for c in text if c in string.punctuation)
    total = len(text)

    print(f"The text contains {total} characters:")
    print(f"{upper} upper letters")
    print(f"{lower} lower letters")
    print(f"{punct} punctuation marks")
    print(f"{spaces} spaces")
    print(f"{digits} digits")


def main():
    """Main program entry handling input and assertion errors."""
    try:
        if len(sys.argv) > 2:
            raise AssertionError("more than one argument is provided")
        elif len(sys.argv) == 2:
            text = sys.argv[1]
        else:
            print("What is the text to count?")
            text = sys.stdin.readline()
        count_text(text)
    except AssertionError as error:
        print(f"AssertionError: {error}")


if __name__ == "__main__":
    main()
```

---

## 12. Knowledge Checklist

- [ ] I know the 5 mandatory rules (no global scope, `main()` guard, docstrings, caught exceptions, `flake8`).
- [ ] I can check character types with `.isupper()`, `.islower()`, `.isdigit()`, and `.isspace()`.
- [ ] I can check for punctuation marks using `string.punctuation`.
- [ ] I know why `sys.stdin.readline()` preserves `\n` to match the subject's count.
- [ ] I have verified that my file passes `flake8` with zero errors.
