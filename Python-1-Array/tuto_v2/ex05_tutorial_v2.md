# Study Tutorial — Exercise 05: pimp_image.py

## 1. Exercise Overview

**What it asks:**
Create a module named `pimp_image.py` in directory `ex05/` containing 5 color filter functions that operate on an image array while **keeping the image shape the same**:
1. `def ft_invert(array) -> array:`
   - Inverts the colors of the image.
   - Allowed operators: `=`, `+`, `-`, `*`
2. `def ft_red(array) -> array:`
   - Isolates the red channel (zeroes green and blue).
   - Allowed operators: `=`, `*`
3. `def ft_green(array) -> array:`
   - Isolates the green channel (zeroes red and blue).
   - Allowed operators: `=`, `-`
4. `def ft_blue(array) -> array:`
   - Isolates the blue channel (zeroes red and green).
   - Allowed operators: `=`
5. `def ft_grey(array) -> array:`
   - Converts the image into grayscale while keeping shape `(H, W, 3)`.
   - Allowed operators: `=`, `/`

**Rules and Constraints:**
- **Strict Operator Restrictions:** You can **only** use the operators explicitly listed for each function. You do not have to use all of them, but you cannot use any unlisted operators!
- **Preserve Image Shape:** Each function must return an array with the exact same shape as the input `(height, width, 3)`.
- **Do Not Mutate in Place:** Always operate on `array.copy()` so that subsequent filter calls in `tester.py` receive the original unmodified image data.
- **Display Transformed Images:** Each filter must display the transformed image (e.g. using `matplotlib.pyplot`).
- **Docstrings Required:** Every function must have documentation (`__doc__`). The subject tester explicitly tests `print(ft_invert.__doc__)`.
- Follow all 42 Python Norm rules: PEP 8 / `flake8` compliance, type annotations, and a `main()` function.

**Main concepts you'll learn:**
- Color spaces and RGB color channel separation.
- Array operations with strict arithmetic constraints.
- In-place mutation vs. non-destructive copying (`.copy()`).
- Grayscale luminance computation without shape reduction.
- Visualizing multi-channel filters with Matplotlib.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **3D NumPy Arrays (Module 1 ex02, ex03):** Indexing slices along the channel axis `[:, :, channel]`.
- **Image Visualization (Module 1 ex03, ex04):** Displaying arrays using `matplotlib.pyplot.imshow()`.
- **Docstrings & Introspection (Module 0 ex02, ex05):** Adding PEP 257 docstrings accessible via `.__doc__`.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `array.copy()` | Creates a deep copy of the NumPy array | Crucial: prevents mutating input image |
| `array[:, :, c]` | Selects the $c$-th color channel (0=Red, 1=Green, 2=Blue) | Slices across all rows and columns |
| `plt.imshow(array)` | Displays RGB image array | Renders 3-channel color correctly |
| `plt.show()` | Opens the graphical window | Visualizes each filter |
| Operator restrictions | Restricts which arithmetic symbols are allowed in code | Verified during evaluation |

**Common pitfalls:**
- **Mutating the Original Array:** In Python, arrays are passed by reference. If `ft_invert` changes `array` in place, then `ft_red` will receive an inverted image instead of the original `landscape.jpg`! Always do `result = array.copy()`.
- **Using Forbidden Operators:** Writing `result[:, :, 1] = 0` inside `ft_green` violates green's restriction (`=, -`), because `0` assignment does not use `-`. Instead, subtract the channel from itself: `result[:, :, 1] = result[:, :, 1] - result[:, :, 1]`.
- **Changing Shape in `ft_grey`:** A common mistake is reducing `(H, W, 3)` to `(H, W)`. The subject explicitly mandates: *"while keeping the image shape the same"*. `ft_grey` must replicate the grayscale value across all 3 channels to retain shape `(H, W, 3)`.
- **Missing or Empty Docstrings:** Evaluators run `print(ft_invert.__doc__)`. If it is missing or empty, you lose points.

---

## 4. Concepts You Need to Learn

### 4.1 RGB Channels and Color Filters
A color image in NumPy has shape `(Height, Width, 3)`:
- Channel `0`: **Red**
- Channel `1`: **Green**
- Channel `2`: **Blue**

To create color filters:
- **Invert:** Each pixel value $v$ is replaced by $255 - v$.
- **Red filter:** Keep Red channel ($c=0$), set Green ($c=1$) and Blue ($c=2$) to $0$.
- **Green filter:** Keep Green channel ($c=1$), set Red ($c=0$) and Blue ($c=2$) to $0$.
- **Blue filter:** Keep Blue channel ($c=2$), set Red ($c=0$) and Green ($c=1$) to $0$.
- **Grey filter:** Set all three channels $R, G, B$ to the average value $\frac{R + G + B}{3}$.

### 4.2 Solving the Operator Restrictions

#### 1. Invert (`=`, `+`, `-`, `*`)
$$\text{inverted} = 255 - \text{array}$$
Uses only `=` and `-`. Completely valid.

#### 2. Red (`=`, `*`)
To set Green and Blue to 0 using `*`:
```python
result = array.copy()
result[:, :, 1] = result[:, :, 1] * 0
result[:, :, 2] = result[:, :, 2] * 0
```
Or vector multiplication: `result = array * [1, 0, 0]`. Both use only `=` and `*`.

#### 3. Green (`=`, `-`)
To set Red and Blue to 0 using `-`:
```python
result = array.copy()
result[:, :, 0] = result[:, :, 0] - result[:, :, 0]
result[:, :, 2] = result[:, :, 2] - result[:, :, 2]
```
Subtracting a channel from itself gives 0! This uses only `=` and `-`.

#### 4. Blue (`=`)
Only assignment `=` is allowed:
```python
result = array.copy()
result[:, :, 0] = 0
result[:, :, 1] = 0
```
This uses only `=`.

#### 5. Grey (`=`, `/`)
Only `=` and `/` are allowed:
To compute the grayscale average across channels without using `+`, we can use NumPy's `.sum(axis=2)` method (which is a method, not an operator) divided by 3:
```python
result = array.copy()
grey_channel = array.sum(axis=2) / 3
result[:, :, 0] = grey_channel
result[:, :, 1] = grey_channel
result[:, :, 2] = grey_channel
```
The only arithmetic operator in this code is `/`, and assignment is `=`.
Alternatively, if single channel luminance is used:
```python
result = array.copy()
result[:, :, 0] = array[:, :, 1] / 1
result[:, :, 1] = array[:, :, 1] / 1
result[:, :, 2] = array[:, :, 1] / 1
```
Both strictly follow the restriction!

---

## 5. Syntax and Examples

### Preserving Array Types and Values
```python
import numpy as np

# Ensure results are uint8 or standard integer array
result = (255 - array).astype(np.uint8)
```

### Visualizing with Matplotlib
```python
import matplotlib.pyplot as plt


def show_image(img: np.ndarray, title: str) -> None:
    """Display an image with a title."""
    plt.imshow(img)
    plt.title(title)
    plt.axis("on")
    plt.show()
```

---

## 6. How to Think About the Exercise

1. **Step 1: Check operator rules.** For each function, review its specific allowed operators.
2. **Step 2: Never mutate input.** Start every function with `result = array.copy()`.
3. **Step 3: Implement `ft_invert`.** Compute `255 - result`.
4. **Step 4: Implement `ft_red`.** Multiply Green and Blue channels by `0`.
5. **Step 5: Implement `ft_green`.** Subtract Red and Blue channels from themselves.
6. **Step 6: Implement `ft_blue`.** Assign `0` directly to Red and Green channels.
7. **Step 7: Implement `ft_grey`.** Compute channel average with `.sum(axis=2) / 3` and assign to all three channels.
8. **Step 8: Display and verify.** Display each transformed image and verify docstrings.

---

## 7. Guided Practice

**Practice 1 (Easiest — Inverting an RGB array):**
Given an RGB pixel `[19, 42, 83]`, compute its inverted RGB values using `255 - val`.

Expected output:
```python
[236, 213, 172]
```

<details><summary>Solution</summary>

```python
import numpy as np

pixel = np.array([19, 42, 83])
inverted = 255 - pixel
print(inverted)
```
</details>

**Practice 2 (Red filter with multiplication):**
Take a `(2, 2, 3)` dummy array and set the Green and Blue channels to zero using only `*` and `=`.

Expected output:
Channel 0 retains original values; channels 1 and 2 are all zeros.

<details><summary>Solution</summary>

```python
import numpy as np

arr = np.array([[[10, 20, 30], [40, 50, 60]]])
res = arr.copy()
res[:, :, 1] = res[:, :, 1] * 0
res[:, :, 2] = res[:, :, 2] * 0
print(res)
```
</details>

**Practice 3 (Green filter with subtraction & Blue filter with assignment):**
Implement `ft_green` using only `=` and `-`, and `ft_blue` using only `=`.

Expected output:
Green filter keeps only channel 1; Blue filter keeps only channel 2.

<details><summary>Solution</summary>

```python
import numpy as np


def ft_green(array: np.ndarray) -> np.ndarray:
    """Filter green channel using = and -."""
    res = array.copy()
    res[:, :, 0] = res[:, :, 0] - res[:, :, 0]
    res[:, :, 2] = res[:, :, 2] - res[:, :, 2]
    return res


def ft_blue(array: np.ndarray) -> np.ndarray:
    """Filter blue channel using =."""
    res = array.copy()
    res[:, :, 0] = 0
    res[:, :, 1] = 0
    return res
```
</details>

**Practice 4 (Grayscale filter with `/` and `=`):**
Implement `ft_grey` using only `=` and `/` that keeps shape `(H, W, 3)`.

Expected output:
All three channels contain identical grayscale values.

<details><summary>Solution</summary>

```python
import numpy as np


def ft_grey(array: np.ndarray) -> np.ndarray:
    """Convert to grayscale using = and / while keeping 3 channels."""
    res = array.copy()
    grey = array.sum(axis=2) / 3
    res[:, :, 0] = grey
    res[:, :, 1] = grey
    res[:, :, 2] = grey
    return res
```
</details>

**Practice 5 (Hardest — the full, rule-compliant `pimp_image.py`):**
Write the complete `pimp_image.py` containing all 5 filter functions with full docstrings, strict operator compliance, image visualization, and `main()` function.

Expected output when running `tester.py`:
```
$> python tester.py
The shape of image is: (257, 450, 3)
[[[19 42 83]
  [23 42 84]
  [28 43 84]
  ...
  [ 0  0  0]
  [ 1  1  1]
  [ 1  1  1]]]
...
Inverts the color of the image received.
```

<details><summary>Solution</summary>

```python
"""Module providing various artistic color filters for RGB images."""

import matplotlib.pyplot as plt
import numpy as np


def ft_invert(array: np.ndarray) -> np.ndarray:
    """Invert the color of the image received.

    Operators allowed: =, +, -, *
    """
    result = 255 - array
    plt.imshow(result)
    plt.title("Figure VIII.2: Invert")
    plt.show()
    return result


def ft_red(array: np.ndarray) -> np.ndarray:
    """Isolate the red channel of the image received.

    Operators allowed: =, *
    """
    result = array.copy()
    result[:, :, 1] = result[:, :, 1] * 0
    result[:, :, 2] = result[:, :, 2] * 0
    plt.imshow(result)
    plt.title("Figure VIII.3: Red")
    plt.show()
    return result


def ft_green(array: np.ndarray) -> np.ndarray:
    """Isolate the green channel of the image received.

    Operators allowed: =, -
    """
    result = array.copy()
    result[:, :, 0] = result[:, :, 0] - result[:, :, 0]
    result[:, :, 2] = result[:, :, 2] - result[:, :, 2]
    plt.imshow(result)
    plt.title("Figure VIII.4: Green")
    plt.show()
    return result


def ft_blue(array: np.ndarray) -> np.ndarray:
    """Isolate the blue channel of the image received.

    Operators allowed: =
    """
    result = array.copy()
    result[:, :, 0] = 0
    result[:, :, 1] = 0
    plt.imshow(result)
    plt.title("Figure VIII.5: Blue")
    plt.show()
    return result


def ft_grey(array: np.ndarray) -> np.ndarray:
    """Convert the image received to greyscale.

    Operators allowed: =, /
    """
    result = array.copy()
    grey = array.sum(axis=2) / 3
    result[:, :, 0] = grey
    result[:, :, 1] = grey
    result[:, :, 2] = grey
    plt.imshow(result)
    plt.title("Figure VIII.6: Grey")
    plt.show()
    return result


def main():
    """Execute tester sequence."""
    try:
        from load_image import ft_load
        array = ft_load("landscape.jpg")
        if array is not None:
            ft_invert(array)
            ft_red(array)
            ft_green(array)
            ft_blue(array)
            ft_grey(array)
            print(ft_invert.__doc__)
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
```
</details>

If all five filters render correctly and docstrings print as expected, you're done!

---

## 8. Exercise-Specific Knowledge

- **Exact Tester from Subject:**
  ```python
  from load_image import ft_load
  from pimp_image import ft_invert, ft_red, ft_green, ft_blue, ft_grey

  array = ft_load("landscape.jpg")
  ft_invert(array)
  ft_red(array)
  ft_green(array)
  ft_blue(array)
  ft_grey(array)
  print(ft_invert.__doc__)
  ```
- **Operator Verification:** Peers will grep for operators in each function. Make sure:
  - `ft_invert` contains only `=`, `+`, `-`, `*`
  - `ft_red` contains only `=`, `*`
  - `ft_green` contains only `=`, `-`
  - `ft_blue` contains only `=`
  - `ft_grey` contains only `=`, `/`
- **Output Figures:** The subject shows 6 figures: Original, Invert, Red, Green, Blue, Grey. Using `plt.imshow(...)` and `plt.show()` satisfies the requirement to display each image.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| In-place mutation | Modifying `array` without `.copy()` | Use `result = array.copy()` |
| Using `=` in `ft_green` with literal 0 | Writing `arr[:, :, 0] = 0` (uses only `=`) | Use subtraction: `arr - arr` |
| Changing shape in `ft_grey` to `(H, W)` | Using `array.mean(axis=2)` directly | Assign grayscale values back to all 3 channels |
| Forgetting docstrings | Tester prints `ft_invert.__doc__` | Include meaningful docstrings |

---

## 10. Debugging Guide

- **Red filter image appears cyan**: You kept channels 1 and 2 instead of zeroing them. Keep channel 0 and zero channels 1 and 2.
- **Grayscale image looks dark**: Dividing integer arrays by integer `3` may cause truncation if not handled carefully; ensure division `/` produces float or proper casting.

---

## 11. Cheat Sheet

```python
# Invert (=, -):
res = 255 - array

# Red (=, *):
res[:, :, 1] = res[:, :, 1] * 0
res[:, :, 2] = res[:, :, 2] * 0

# Green (=, -):
res[:, :, 0] = res[:, :, 0] - res[:, :, 0]
res[:, :, 2] = res[:, :, 2] - res[:, :, 2]

# Blue (=):
res[:, :, 0] = 0
res[:, :, 1] = 0

# Grey (=, /):
g = array.sum(axis=2) / 3
res[:, :, 0] = g; res[:, :, 1] = g; res[:, :, 2] = g
```

---

## 12. Knowledge Checklist

- [ ] I implemented all 5 filter functions while strictly respecting allowed operators.
- [ ] I kept the shape `(H, W, 3)` unchanged across all functions.
- [ ] I used `array.copy()` to avoid corrupting data between function calls.
- [ ] I included detailed docstrings for all functions.
- [ ] My code conforms to PEP 8 and passes `flake8` without warnings.
