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

**Practice 1 (Character counts):**
Write a function `count_digits_and_letters(s)` that prints how many digits and letters are in a string.
<details><summary>Solution</summary>

```python
def count_digits_and_letters(s: str) -> None:
    """Print the count of digits and letters."""
    digits = sum(1 for c in s if c.isdigit())
    letters = sum(1 for c in s if c.isalpha())
    print(f"Letters: {letters}, Digits: {digits}")
```
</details>

**Practice 2 (Punctuation check):**
Write a function `count_punct(s)` that uses `string.punctuation` to count punctuation characters.
<details><summary>Solution</summary>

```python
import string

def count_punct(s: str) -> int:
    """Count punctuation characters in a string."""
    count = 0
    for char in s:
        if char in string.punctuation:
            count += 1
    return count
```
</details>

**Practice 3 (Complete compliant structure):**
Implement the program with docstrings and `main()`, catching `AssertionError`.
<details><summary>Solution</summary>

```python
import sys
import string

def count_text(text: str) -> None:
    """Analyze and display counts of various character categories."""
    upper = 0
    lower = 0
    punct = 0
    spaces = 0
    digits = 0

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

    total = len(text)
    print(f"The text contains {total} characters:")
    print(f"{upper} upper letters")
    print(f"{lower} lower letters")
    print(f"{punct} punctuation marks")
    print(f"{spaces} spaces")
    print(f"{digits} digits")

def main():
    """Handle CLI argument or prompt user for text."""
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
</details>

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
