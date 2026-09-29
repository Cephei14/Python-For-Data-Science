# Study Tutorial — Module 1, Exercise 05: pimp_image.py

## 1. Exercise Overview

**What it asks:** Write five functions that apply color filters to an image array, each restricted to using only certain operators: `ft_invert` (invert colors: `=, +, -, *`), `ft_red` (isolate red: `=, *`), `ft_green` (isolate green: `=, -`), `ft_blue` (isolate blue: `=`), and `ft_grey` (grayscale: `=, /`). All must preserve the image's original shape.

**Main concepts you'll learn:**
- How color inversion, channel isolation, and grayscale conversion work mathematically
- Applying arithmetic operations across an entire array at once (vectorization)
- Working within an artificial operator constraint — a good exercise in translating "what I want to do" into "the only tools I'm allowed to use"

**Why this matters:** This exercise is a compact tour of the most common image-processing operations, all done via simple array math — no special image-processing functions needed. It reinforces that "manipulating an image" often just means "doing arithmetic on an array," a mental model that generalizes to all kinds of numeric data transformations, not just images.

**Skills after completing it:**
- Invert values within a fixed range (e.g., 0–255) using arithmetic
- Zero out specific channels to isolate a single color
- Convert RGB to grayscale using averaging
- Work creatively within a restricted operator set

---

## 2. Prerequisites

- Exercise 02's image loading (`ft_load`), producing an `(H, W, 3)` array
- Basic understanding of RGB channels (index 0=Red, 1=Green, 2=Blue)
- Elementwise array arithmetic (NumPy applies `+`, `-`, `*`, `/` to every element of an array at once)

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| NumPy elementwise arithmetic (`arr + 5`, `255 - arr`, `arr * 0`, `arr / 3`) | Applies the operation to every value in the array simultaneously | This *is* vectorization — no loops needed |
| `arr.copy()` | Creates an independent copy of an array | Important so you don't accidentally modify the original image when building each filtered version |
| Slicing to select a channel: `arr[:, :, 0]` | Selects just one channel (e.g., Red) across the whole image | Combine with assignment to zero out other channels |

Common pitfalls:
- Modifying the original array in place instead of working on a copy — since NumPy arrays are mutable, `arr[:, :, 1] = 0` changes the array itself, which can silently corrupt later operations if you don't copy first.
- For `ft_invert`, forgetting standard 8-bit images range 0–255, so "inverting" a value means `255 - value`, not just negating it.
- For `ft_grey`, forgetting grayscale conversion needs **all three channels averaged**, not just one channel picked — using only `/`, this is `(R + G + B) / 3`, but wait: the allowed operators for grey are only `=` and `/` — meaning you cannot use `+` to sum the channels! This requires a different approach (see below).

---

## 4. Concepts You Need to Learn

### 4.1 Vectorized arithmetic on arrays
```python
import numpy as np
arr = np.array([10, 20, 30])
print(arr * 2)     # [20 40 60]
print(255 - arr)    # [245 235 225]
```
Every operation applies to *every element* simultaneously — no explicit loop required. This is the core reason NumPy exists: expressing "do this to every pixel" as a single line.

### 4.2 Color inversion
Standard 8-bit color images store each channel value in the range 0–255. Inverting a color means flipping it around the midpoint: `inverted = 255 - original`. Allowed operators (`=, +, -, *`) comfortably support this: `255 - arr` uses subtraction.

### 4.3 Isolating a single channel
To make an image "look red," you keep the Red channel as-is and zero out Green and Blue:
```python
red_only = arr.copy()
red_only[:, :, 1] = 0   # zero out Green
red_only[:, :, 2] = 0   # zero out Blue
```
Zeroing with `= 0` is assignment (`=`), and if you need to *scale* a channel instead of zeroing it, that's where `*` (e.g., `* 0`) comes in — matching the "red: `=, *`" and "blue: `=`" operator restrictions.

### 4.4 Grayscale conversion within a restricted operator set
A common grayscale formula is the plain average: `grey = (R + G + B) / 3`. But `ft_grey` is only allowed `=` and `/` — no `+`! This means you can't sum the channels directly with `+`. One approach: use NumPy's `.mean(axis=2)`, which computes the average internally without you writing an explicit `+` in your own code — the *addition* happens inside NumPy's own implementation, not in your source code's operator usage. This is a common reading of this kind of operator-restriction exercise: the restriction applies to operators you *write*, while calling a library function that internally performs disallowed operations is generally the intended workaround, since manual summation would otherwise be mathematically necessary and impossible to avoid with the given tools. (If in doubt, this specific interpretation is worth confirming with your evaluator/peers, since the subject's exact intent regarding library-internal operations isn't explicitly spelled out.)
```python
grey = arr.mean(axis=2) / 1   # average across channels, `/` used to satisfy the operator note
```

---

## 5. Syntax and Examples

### `ft_invert`
```python
def ft_invert(array):
    """Invert the colors of the image received."""
    return 255 - array
```
Small example:
```python
import numpy as np
test = np.array([0, 100, 255])
print(255 - test)  # [255 155 0]
```

### `ft_red`
```python
def ft_red(array):
    """Isolate the red channel of the image received."""
    result = array.copy()
    result[:, :, 1] = result[:, :, 1] * 0
    result[:, :, 2] = result[:, :, 2] * 0
    return result
```

### `ft_green`
```python
def ft_green(array):
    """Isolate the green channel of the image received."""
    result = array.copy()
    result[:, :, 0] = result[:, :, 0] - result[:, :, 0]
    result[:, :, 2] = result[:, :, 2] - result[:, :, 2]
    return result
```
Here, subtraction of a channel from itself (`x - x`) is a way to zero it out using only the `-` operator, satisfying green's `=, -` restriction.

### `ft_blue`
```python
def ft_blue(array):
    """Isolate the blue channel of the image received."""
    result = array.copy()
    result[:, :, 0] = 0
    result[:, :, 1] = 0
    return result
```
Blue is restricted to `=` only — plain assignment of `0` satisfies this directly.

### `ft_grey`
```python
def ft_grey(array):
    """Convert the image received to greyscale."""
    grey = array.mean(axis=2)
    return grey
```
`axis=2` tells `.mean()` to average across the channel axis (the third dimension), collapsing `(H, W, 3)` down to `(H, W)` — while preserving the same "content," just represented with one value per pixel instead of three.

---

## 6. How to Think About the Exercise

1. For each filter, first figure out *conceptually* what transformation you need (invert, isolate, average), independent of the operator restriction.
2. Then check: does the allowed operator set for that specific function support your approach directly, or do you need a different, allowed way to express the same idea (like using `-` for zeroing instead of `*`, or `.mean()` for grayscale)?
3. Always copy the array before modifying channels in place (`array.copy()`) — the subject's tester calls all five functions on the *same* loaded array in sequence, so if one function mutates it in place, later functions would operate on already-modified data.
4. Confirm the shape stays the same as required (`ft_invert`, `ft_red`, `ft_green`, `ft_blue` keep `(H, W, 3)`; `ft_grey` is allowed/expected to reduce to `(H, W)`, since the point is grayscale conversion).
5. Write a docstring for each function — the tester explicitly checks `ft_invert.__doc__`.
6. Test by displaying each filtered result with Matplotlib, comparing visually against the subject's example figure (original, invert, red, green, blue, grey).

---

## 7. Guided Practice

**Practice 1 (Easy):** Given `arr = np.array([50, 150, 250])`, compute its color inversion.
<details><summary>Solution</summary>

```python
print(255 - arr)  # [205 105 5]
```
</details>

**Practice 2 (Easy):** Given a `(4, 4, 3)` dummy array, zero out just the first channel using slicing and assignment.
<details><summary>Solution</summary>

```python
import numpy as np
arr = np.random.randint(0, 255, (4, 4, 3))
arr_copy = arr.copy()
arr_copy[:, :, 0] = 0
```
</details>

**Practice 3 (Medium):** Write a function that isolates the Green channel using only `=` and `-` (no `*`, no direct `0` in a way that reads like a shortcut beyond subtraction).
<details><summary>Solution</summary>

```python
def isolate_green(arr):
    result = arr.copy()
    result[:, :, 0] = result[:, :, 0] - result[:, :, 0]
    result[:, :, 2] = result[:, :, 2] - result[:, :, 2]
    return result
```
</details>

**Practice 4 (Close to the real exercise):** Convert a `(H, W, 3)` array to grayscale using `.mean(axis=2)`, and confirm the resulting shape.
<details><summary>Solution</summary>

```python
def to_grey(arr):
    return arr.mean(axis=2)

test = np.random.randint(0, 255, (10, 10, 3))
grey = to_grey(test)
print(grey.shape)  # (10, 10)
```
</details>

---

## 8. Exercise-Specific Knowledge

- Function names and prototypes: `ft_invert`, `ft_red`, `ft_green`, `ft_blue`, `ft_grey` — all take and return an `array`.
- Operator restrictions per function (you don't have to use every allowed operator, just stay within the allowed set):
  - `ft_invert`: `=, +, -, *`
  - `ft_red`: `=, *`
  - `ft_green`: `=, -`
  - `ft_blue`: `=`
  - `ft_grey`: `=, /`
- All filtered images must keep the *same shape* as the original (except grayscale, which conceptually collapses the channel dimension — check the subject's exact expectation here if graded strictly on shape-preservation for `ft_grey` specifically, since "keeping the image shape the same" is stated as a general goal but grayscale inherently changes channel count).
- Docstrings are checked directly via `__doc__` in the tester.
- Must reuse `load_image.py`; turn in both `load_image.py` and `pimp_image.py`.
- Must display all five transformed images, matching the general spirit of the subject's example figure.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Modifying the original array in place across multiple filter calls | Forgetting `.copy()` | Always copy before mutating channels |
| Using a disallowed operator for a specific filter (e.g., `+` in `ft_blue`) | Reaching for the most obvious approach without checking the restriction | Re-read each function's allowed operator list before implementing it |
| `ft_grey` producing wrong-looking results (too light/dark) | Forgetting to average, e.g. just picking one channel and calling it "grey" | Use `.mean(axis=2)` (or a manually restricted equivalent) to properly average all channels |
| Inversion producing negative numbers or overflow artifacts | Not accounting for the image's dtype (`uint8` wraps around instead of going negative) | If needed, cast to a signed/float type before subtracting, then cast back if you need `uint8` output |

---

## 10. Debugging Guide

- **Inverted image looks wrong (very dark instead of very light, or vice versa)** → check whether your array's dtype is `uint8`; subtracting from `255` should behave correctly, but double-check for unexpected wraparound if you used a different operation order.
- **All five filters appear identical** → you likely forgot `.copy()` somewhere, causing later filters to operate on an already-modified array from a previous call.
- **`ft_grey` result won't display properly** → grayscale 2D arrays need `cmap="gray"` in `plt.imshow()`; without it, Matplotlib may apply a default colormap that looks like false color.
- Useful inspection: `print(array.dtype)` to confirm you're working with the expected numeric type (`uint8` is standard for 0–255 image data) before doing arithmetic that could overflow or produce unexpected results.

---

## 11. Cheat Sheet

```python
def ft_invert(array):
    return 255 - array

def ft_red(array):
    result = array.copy()
    result[:, :, 1] *= 0
    result[:, :, 2] *= 0
    return result

def ft_green(array):
    result = array.copy()
    result[:, :, 0] -= result[:, :, 0]
    result[:, :, 2] -= result[:, :, 2]
    return result

def ft_blue(array):
    result = array.copy()
    result[:, :, 0] = 0
    result[:, :, 1] = 0
    return result

def ft_grey(array):
    return array.mean(axis=2)
```

---

## 12. Knowledge Checklist

- [ ] I understand vectorized arithmetic applies an operation to every array element at once.
- [ ] I can invert an image's colors using `255 - array`.
- [ ] I can isolate a single color channel by zeroing out the others.
- [ ] I can convert an RGB image to grayscale by averaging channels.
- [ ] I remember to `.copy()` an array before modifying it in place, to avoid corrupting shared data across function calls.
