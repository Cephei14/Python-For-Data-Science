# Study Tutorial — Exercise 00: Hello.py

## 1. Exercise Overview

**What it asks:** You're given four variables — a list, a tuple, a set, and a dictionary — each containing `"Hello"` paired with a placeholder word (`"tata!"`, `"toto!"`, etc.). Your job is to change the *second* element/value of each one so the pair reads `"Hello", "World!"` (or your country/city/campus name), without deleting and recreating the variables from scratch.

**Main concepts you'll learn:**
- The four core built-in Python collection types: `list`, `tuple`, `set`, `dict`
- Which of these are **mutable** (can be changed in place) and which are **immutable** (cannot)
- How to modify each type using its own correct method

**Why this matters in real data science work:** Every pandas DataFrame, every NumPy array, every JSON API response you'll ever load is built out of these four structures underneath. Before you can manipulate a spreadsheet of data, you need rock-solid instincts for "can I change this in place, or do I need to build a new one?" — that instinct is exactly what this exercise drills.

**Skills after completing it:**
- Confidently distinguish mutable vs immutable types
- Modify a list by index
- Rebuild a tuple (since you can't modify it directly)
- Add/remove elements from a set correctly
- Update a dictionary value by key

---

## 2. Prerequisites

You need to know:
- How to run a Python script from the terminal: `python Hello.py`
- What a variable and an assignment (`=`) are
- What `print()` does

That's it — this is exercise 00 for a reason. Everything else is taught below.

---

## 3. Tools and Libraries

No external libraries needed. Everything here is built into core Python:

| Tool | What it does | When to use it |
|---|---|---|
| `list[index] = value` | Replaces the item at `index` in a list | Lists are mutable — this always works |
| Tuple repacking (`t = (t[0], new_value)`) | Tuples don't support item assignment, so you build a new tuple | Whenever you need to "change" a tuple |
| `set.add(value)` / `set.remove(value)` | Adds/removes an item from a set | Sets are unordered — you add the new item and remove the old one |
| `dict[key] = value` | Replaces (or adds) the value for a given key | Dictionaries are mutable by key |

---

## 4. Concepts You Need to Learn

### 4.1 Lists — ordered, mutable, allow duplicates

A list is written with square brackets: `["Hello", "tata!"]`. "Mutable" means you can change its contents after creation without making a new list object.

### 4.2 Tuples — ordered, **immutable**

A tuple looks like a list but uses parentheses: `("Hello", "toto!")`. Immutable means: once created, you cannot change, add, or remove an item. If you try `my_tuple[1] = "x"`, Python raises `TypeError: 'tuple' object does not support item assignment`.

So how do you "change" a tuple? You don't — you build a new tuple keeping the first item and providing the new second item, and rebind the variable name `ft_tuple` to it. The old tuple object in memory is discarded; the variable now points to the new one.

### 4.3 Sets — unordered, mutable, **no duplicates**, no indexing

A set is written with curly braces: `{"Hello", "tutu!"}`. Because sets are unordered hash tables, there is no indexing (`my_set[0]` raises `TypeError`). You modify a set by adding what you want (`.add()`) and removing what you don't (`.remove()`).

> [!NOTE]
> **Why is my set order different from the subject?**
> When you run your code, you might see `{'Tokyo!', 'Hello'}` instead of `{'Hello', 'Tokyo!'}`. **This is completely normal!** In Python, sets are unordered, and Python randomizes hash seeds per run for security (`PYTHONHASHSEED`). Evaluators and tests check that the set contains the correct elements, not their printed order.

### 4.4 Dictionaries — key/value pairs, mutable

A dictionary maps keys to values: `{"Hello": "titi!"}`. Here `"Hello"` is the key and `"titi!"` is the value. You change a value by referring to its key, not its position: `ft_dict["Hello"] = "42Paris!"`.

---

## 5. Syntax and Examples

### Lists
```python
fruits = ["apple", "banana"]
fruits[1] = "cherry"
print(fruits)  # ['apple', 'cherry']
```
`fruits[1]` refers to the item at index 1 (indexes start at 0). Assigning to it replaces that item in place — the same list object, just with different contents.

Applied to the exercise:
```python
ft_list[1] = "World!"
```

### Tuples
```python
point = (1, 2)
point = (point[0], 3)
print(point)  # (1, 3)
```
You can't touch `point[1]` directly. Instead you build a new tuple `(point[0], 3)` — keeping the first element, replacing the second — and reassign it to `point`.

Applied to the exercise:
```python
ft_tuple = (ft_tuple[0], "Japan!")
```

### Sets
```python
colors = {"red", "green"}
colors.remove("green")
colors.add("blue")
print(colors)  # {'red', 'blue'} (order not guaranteed)
```
`.remove(x)` deletes `x` from the set (raises `KeyError` if `x` isn't present — see Common Mistakes). `.add(x)` inserts `x`.

Applied to the exercise:
```python
ft_set.remove("tutu!")
ft_set.add("Tokyo!")
```

### Dictionaries
```python
person = {"name": "Alex"}
person["name"] = "Sam"
print(person)  # {'name': 'Sam'}
```
`person["name"]` looks up the value for key `"name"` and reassigns it. If the key already exists, its value is overwritten; if it doesn't, a new key/value pair is added.

Applied to the exercise:
```python
ft_dict["Hello"] = "42Tokyo!"
```

---

## 6. How to Think About the Exercise

1. Look at each variable's **type** first — that tells you which technique applies.
2. Ask: "Is this mutable?" Lists, sets, dicts → yes. Tuples → no.
3. For mutable types, find the *correct* way to change them (index for list, key for dict, add/remove for set) — don't just guess `[1] = ...` for everything.
4. For the tuple, accept that you must rebuild it rather than fight the immutability.
5. Print each one at the end and compare against the expected output character-for-character, including the exact greeting wording.

---

## 7. Guided Practice

**Practice 1 (Easy):** Given `nums = [10, 20, 30]`, change the last element to `99` without rewriting the whole list.
<details><summary>Hint</summary>What's the index of the last element in a 3-item list?</details>
<details><summary>Solution</summary>

```python
nums[2] = 99
```
Index 2 is the third (last) position since indexing starts at 0.
</details>

**Practice 2 (Easy-Medium):** Given `coord = (5, 5)`, produce a new tuple where the second value is `10`, keeping the first value unchanged.
<details><summary>Hint</summary>You cannot assign into a tuple. Build a new one using the old value.</details>
<details><summary>Solution</summary>

```python
coord = (coord[0], 10)
```
</details>

**Practice 3 (Medium):** Given `tags = {"python", "java"}`, replace `"java"` with `"rust"`.
<details><summary>Hint</summary>Two separate set operations are needed.</details>
<details><summary>Solution</summary>

```python
tags.remove("java")
tags.add("rust")
```
</details>

**Practice 4 (Medium):** Given `ages = {"Alex": 30}`, change Alex's age to `31`.
<details><summary>Hint</summary>Use the key, not a position.</details>
<details><summary>Solution</summary>

```python
ages["Alex"] = 31
```
</details>

---

## 8. Exercise-Specific Knowledge

- The exercise expects **four** print statements, one per variable, in the given order.
- The greetings must exactly match: `"Hello World!"`, `"Hello <country>!"`, `"Hello <city>!"`, `"Hello <campus>!"` split across the two elements each collection already has (`"Hello"` stays as-is; only the second word changes).
- The grader pipes output through `cat -e`, which shows a `$` at the end of each line — this just confirms there's no trailing whitespace or missing newline; you don't need to do anything special for it, `print()` already ends lines correctly.
- No imports, no functions required — this is a flat, top-level script (global-scope code is explicitly fine *only* in this early exercise, before the "no global scope" rule kicks in from Exercise 05 onward).

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| `ft_tuple[1] = "World!"` | Forgetting tuples are immutable | Rebuild the tuple: `ft_tuple = (ft_tuple[0], "World!")` |
| `ft_set[1] = "World!"` | Treating a set like a list | Sets have no index — use `.add()`/`.remove()` |
| `ft_set.remove("Tokyo!")` before it's added, or removing something not present | Wrong order of operations, or typo in the value | Always remove the *old* value, then add the *new* one; double-check spelling/case |
| Forgetting the dictionary key stays the same, only the value changes | Confusing key and value | `ft_dict["Hello"] = "42Tokyo!"` — the key `"Hello"` never changes |
| Small typos like `"Word!"` instead of `"World!"` | Typing quickly | Automated graders test exact string equality — double-check character-for-character |
| Panicking because the set prints in a different order than the subject | Not knowing sets are unordered in Python | Set order is not fixed and varies across runs; evaluators check elements, not order |
| Using tabs instead of 4 spaces | Habit from 42 C norminette | In Python, PEP 8 / `flake8` forbids tabs (`W191`). Always use 4 spaces |

---

## 10. Debugging Guide

- **`TypeError: 'tuple' object does not support item assignment`** → You tried to assign into a tuple by index. Rebuild it instead.
- **`KeyError: 'x'`** on `set.remove('x')` → The value `'x'` isn't in the set (check spelling/case exactly, including the `!`).
- **Set prints `{'Tokyo!', 'Hello'}` instead of `{'Hello', 'Tokyo!'}`** → This is expected behavior for sets; you do not need to fix it.
- **Nothing prints / wrong order** → Make sure your four `print()` calls are actually placed *after* your modifications, and in the same order as the original script.
- **Flake8 warning `W191 indentation contains tabs`** → Replace all tab characters with 4 spaces.
- Useful inspection: `print(type(ft_list))` to double check you're reasoning about the right collection type when debugging.

---

## 11. Cheat Sheet

```python
# List — mutate by index
my_list[i] = new_value

# Tuple — cannot mutate; rebuild
my_tuple = (my_tuple[0], new_value)

# Set — no index; add/remove by value
my_set.remove(old_value)
my_set.add(new_value)

# Dict — mutate by key
my_dict[key] = new_value
```

---

## 12. Knowledge Checklist

- [ ] I can explain the difference between mutable and immutable types.
- [ ] I know why tuples require rebuilding instead of item assignment.
- [ ] I can modify a list by index.
- [ ] I can add and remove items from a set correctly.
- [ ] I can update a dictionary value using its key.
- [ ] I understand that this same mutable/immutable distinction will matter later when working with NumPy arrays and pandas objects.
