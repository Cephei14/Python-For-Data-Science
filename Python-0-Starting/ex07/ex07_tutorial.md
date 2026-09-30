# Study Tutorial — Exercise 07: sos.py

## 1. Exercise Overview

**What it asks:**
Create a program named `sos.py` that takes a single string as a command-line argument and encodes it into **Morse code** using a Python `dict`.
- Supports **alphanumeric characters** (`A`–`Z`, `0`–`9`) and **spaces**.
- Each Morse character consists of dots (`.`) and dashes (`-`).
- Individual Morse characters are separated by a **single space**.
- A space in the input text is represented by a slash (`/`).
- If the argument count is not exactly 1, or if any character is invalid (e.g. `$` or punctuation), print:
  `AssertionError: the arguments are bad`.
- Must follow all Chapter VII rules (`main()`, docstrings, caught exceptions, `flake8`).

**Main concepts you'll learn:**
- Using a `dict` as a translation/lookup table.
- Normalizing string casing using `str.upper()`.
- Joining sequences cleanly with `str.join()`.
- Validating input against a strict allowed character set.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **Dictionaries (ex00):** You learned that a `dict` maps unique keys to values: `mapping[key]`.
- **Loops & Strings (ex05):** Iterating through each character of a string.
- **List Comprehensions (ex06):** Transforming elements of an iterable into a list.
- **CLI Arguments & Error Handling (ex04, ex05):** Checking `sys.argv` and catching `AssertionError` inside `main()`.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `NESTED_MORSE = {...}` | A dictionary mapping characters to Morse strings | Mandatory data structure per the subject |
| `char.upper()` | Converts a character to uppercase | Ensures `'s'` matches dictionary key `'S'` |
| `char.isalnum()` | Returns `True` if `char` is a letter or digit | Helps validate allowed characters |
| `" ".join(elements)` | Glues list elements together separated by a space | Eliminates trailing spaces cleanly! |
| `import sys` | Access CLI arguments via `sys.argv` | Allowed by the subject |

Common pitfalls:
- Forgetting digits `0`–`9`: The subject requires "alphanumeric" support, not just letters. You must include numbers 0 through 9 in your dictionary.
- Leaving a trailing space at the end of output: Look at the expected output `... --- ...$`. There is no space before the end of the line (`$`). Using `" ".join(...)` prevents unwanted trailing spaces.
- Unhandled `KeyError`: Looking up an invalid character like `'$'` directly without checking raises `KeyError`. Catch it or validate beforehand to output `AssertionError: the arguments are bad`.

---

## 4. Concepts You Need to Learn

### 4.1 Dictionaries as Lookup Tables

In Exercise 00, you saw dictionaries store key-value pairs:
```python
MORSE_TABLE = {
    "A": ".-",
    "B": "-...",
    "S": "...",
    "O": "---",
    " ": "/",
}

print(MORSE_TABLE["S"])  # '...'
```
Looking up a value in a dictionary by its key is instant and clean—much better than writing 37 `if/elif` statements!

### 4.2 Handling Case Insensitivity (`.upper()`)

Morse code does not have lowercase letters. Whether the user inputs `'s'` or `'S'`, both should encode to `'...'`:
```python
char = "s"
print(char.upper())  # 'S'
```
By converting every character to uppercase before looking it up in the dictionary, your dictionary only needs uppercase keys.

### 4.3 Joining Strings Cleanly with `" ".join()`

How do we assemble individual Morse codes into a single string separated by spaces without having an ugly space at the end?

Python provides the string method `.join()`:
```python
morse_list = ["...", "---", "..."]

result = " ".join(morse_list)
print(result)  # "... --- ..."
```
The separator `" "` is placed *only between* items—never before the first item, and never after the last item!

### 4.4 Validating Input Characters

The subject allows **only**:
- Alphanumeric characters (`A`–`Z`, `a`–`z`, `0`–`9`)
- Space character (`" "`)

If the user types `'h$llo'`, the character `'$'` is not alphanumeric and not a space. The program must detect this and raise an `AssertionError`.

You can check each character:
```python
for char in text:
    if not (char.isalnum() or char == " "):
        raise AssertionError("the arguments are bad")
```

---

## 5. Syntax and Examples

### The Full Morse Lookup Dictionary

```python
NESTED_MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    " ": "/",
}
```

### Encoding a String

```python
text = "SOS 42"
encoded = [NESTED_MORSE[char.upper()] for char in text]
print(" ".join(encoded))
# ... --- ... / ....- ..---
```

---

## 6. How to Think About the Exercise

1. **Step 1: Check argument count.**
   - Exactly one argument is required: `len(sys.argv) == 2`.
   - Any other count $\rightarrow$ raise `AssertionError("the arguments are bad")`.
2. **Step 2: Validate each character.**
   - For every character in `sys.argv[1]`:
     - If it is not in `NESTED_MORSE` (after `.upper()`):
       $\rightarrow$ raise `AssertionError("the arguments are bad")`.
3. **Step 3: Encode and join.**
   - Translate each character to its Morse equivalent.
   - Join the list using `" ".join(...)`.
4. **Step 4: Print and wrap in `main()`.**
   - Catch `AssertionError` to print `AssertionError: <error>` cleanly.

---

## 7. Guided Practice

**Practice 1 (Dictionary lookup):**
Write a function `translate_word(word, table)` that returns a list of translated symbols for each letter in `word`.
<details><summary>Solution</summary>

```python
def translate_word(word: str, table: dict) -> list:
    """Translate each character of word using table."""
    return [table[c.upper()] for c in word if c.upper() in table]
```
</details>

**Practice 2 (Character validation):**
Write a function `is_clean(text)` that returns `True` if all characters are alphanumeric or spaces, and `False` otherwise.
<details><summary>Solution</summary>

```python
def is_clean(text: str) -> bool:
    """Return True if text contains only alphanumeric characters or spaces."""
    for c in text:
        if not (c.isalnum() or c == " "):
            return False
    return True
```
</details>

**Practice 3 (Complete encoding flow):**
Build the complete script structure complying with docstring and exception rules.
<details><summary>Solution</summary>

```python
import sys

NESTED_MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    " ": "/",
}

def encode_morse(text: str) -> str:
    """Encode a valid string into Morse code."""
    for char in text:
        if char.upper() not in NESTED_MORSE:
            raise AssertionError("the arguments are bad")
    return " ".join(NESTED_MORSE[char.upper()] for char in text)

def main():
    """Validate CLI input and display Morse output."""
    try:
        if len(sys.argv) != 2:
            raise AssertionError("the arguments are bad")
        print(encode_morse(sys.argv[1]))
    except AssertionError as error:
        print(f"AssertionError: {error}")

if __name__ == "__main__":
    main()
```
</details>

---

## 8. Exercise-Specific Knowledge

- **Exact Subject Examples:**
  - `python sos.py "sos" | cat -e` $\rightarrow$ `... --- ...$`
  - `python sos.py 'h$llo'` $\rightarrow$ `AssertionError: the arguments are bad`
  - `python sos.py` $\rightarrow$ `AssertionError: the arguments are bad`
- **Spaces:** A space is represented by `/`. Between letters and slashes, single spaces separate them: `"s s"` becomes `... / ...`.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Forgetting numbers (0–9) | Only entering letters A–Z | Add entries for `'0'` through `'9'` |
| Trailing space at end of output | Concatenating with `+= code + " "` | Use `" ".join(...)` |
| `KeyError` on lowercase | Keys in dict are uppercase | Use `char.upper()` |
| Not catching exceptions | Unhandled crash fails norm | Wrap in `try ... except AssertionError:` in `main()` |

---

## 10. Debugging Guide

- **`cat -e` shows a space before `$` (e.g. `... --- ... $`)**: You have a trailing space. Replace string concatenation with `" ".join(...)`.
- **`AssertionError` not raised on `$hello`**: Ensure your validation runs on *every* character before printing.

---

## 11. Cheat Sheet

```python
import sys

NESTED_MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".",
    "F": "..-.", "G": "--.", "H": "....", "I": "..", "J": ".---",
    "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---",
    "P": ".--.", "Q": "--.-", "R": ".-.", "S": "...", "T": "-",
    "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--",
    "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
    " ": "/",
}


def encode_morse(text: str) -> str:
    """Encode an alphanumeric string into Morse code."""
    for char in text:
        if char.upper() not in NESTED_MORSE:
            raise AssertionError("the arguments are bad")
    return " ".join(NESTED_MORSE[char.upper()] for char in text)


def main():
    """Read CLI input, validate, and print encoded Morse code."""
    try:
        if len(sys.argv) != 2:
            raise AssertionError("the arguments are bad")
        print(encode_morse(sys.argv[1]))
    except AssertionError as error:
        print(f"AssertionError: {error}")


if __name__ == "__main__":
    main()
```

---

## 12. Knowledge Checklist

- [ ] I can define and use a lookup dictionary.
- [ ] I know how to convert characters to uppercase with `.upper()`.
- [ ] I can check if characters are valid alphanumeric symbols.
- [ ] I can join strings cleanly without trailing spaces using `" ".join()`.
- [ ] My code passes `flake8` and catches all exceptions cleanly inside `main()`.
