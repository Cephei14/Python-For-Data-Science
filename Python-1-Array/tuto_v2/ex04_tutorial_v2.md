# Study Tutorial — Exercise 04: rotate.py

## 1. Exercise Overview

**What it asks:**
Create a program named `rotate.py` (along with `load_image.py`) in directory `ex04/` that:
1. Loads `"animal.jpeg"` using `ft_load` from `load_image.py`.
2. Cuts a square 400×400 single-channel part from the image (similar to ex03).
3. Prints the sliced image shape and pixel values:
   `The shape of image is: (400, 400, 1)` (or `(400, 400)`)
   Followed by the pixel array data.
4. **Transposes** the 2D matrix **manually** — converting rows into columns.
5. Prints the new transposed shape and data:
   `New shape after Transpose: (400, 400)`
   Followed by the transposed 2D pixel array.
6. Displays the transposed image using `matplotlib.pyplot.imshow()` with grayscale colormap and coordinate scale axes.
7. Handles any error with a clear error message without crashing.

**Strict Subject Rule:**
> **"You have to do the transpose yourself, no library is allowed for the transpose"**
> You CANNOT use `np.transpose()`, `array.T`, `np.swapaxes()`, `cv2.rotate`, or any built-in transpose library! Using any of these will result in an immediate score of 0 for this exercise during evaluation.

**Rules and Constraints:**
- Must follow all 42 Python Norm rules: PEP 8 / `flake8` clean, docstrings on every function and module, type annotations, and a `main()` function catching exceptions.

**Main concepts you'll learn:**
- Matrix transposition fundamentals ($T[j][i] = M[i][j]$).
- Algorithmic implementation of 2D matrix transformation using nested loops and list comprehensions.
- Converting pure Python matrix structures into NumPy arrays.
- Image rotation via transposition.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **2D Arrays & Dimensions (Module 1 ex01):** Rows vs. columns in rectangular matrices.
- **Image Slicing (Module 1 ex03):** Cropping spatial regions and isolating channels from image tensors.
- **List Comprehensions (Module 0 ex06):** Writing nested list comprehensions to build 2D grids.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `from load_image import ft_load` | Loads the image file | From `load_image.py` |
| `import matplotlib.pyplot as plt` | Displays image with axes | For final rendering |
| `import numpy as np` | Array container | Allowed for creating arrays, NOT for transposition! |
| Nested Loops / List Comprehensions | Iterates through rows and columns | Mandatory for manual transpose |
| `plt.imshow(arr, cmap="gray")` | Displays 2D grayscale image | Shows rotated result |

**Common pitfalls:**
- **USING `.T` OR `np.transpose()`:** The subject explicitly states: *"You have to do the transpose yourself, no library is allowed for the transpose"*. Evaluators check this first!
- **Transposing 3D Tensor vs 2D Matrix:** A 3D tensor of shape `(400, 400, 1)` has 3 dimensions. You should squeeze or index the 2D matrix `(400, 400)` first before transposing: `arr[:, :, 0]`.
- **Row/Column Swapping Logic:** In transposition:
  $$\text{Transposed}[c][r] = \text{Original}[r][c]$$
  If you iterate $r$ on the outer loop and $c$ on the inner loop, you're just copying the original! The outer loop must iterate over columns $c$, and the inner loop over rows $r$.
- **Displaying with Scales:** As in ex03, the image display must show the x and y axes with scale ticks.

---

## 4. Concepts You Need to Learn

### 4.1 What is Matrix Transposition?
The transpose of a matrix $M$, denoted $M^T$, is formed by turning all the rows of $M$ into columns and all the columns into rows:
$$\begin{bmatrix} a & b & c \\ d & e & f \end{bmatrix}^T = \begin{bmatrix} a & d \\ b & e \\ c & f \end{bmatrix}$$
If $M$ has dimensions $(R, C)$, $M^T$ has dimensions $(C, R)$.
For our square 400×400 crop, both $R = 400$ and $C = 400$, so the shape remains `(400, 400)`, but pixel positions are reflected across the main diagonal.

### 4.2 Implementing Transposition Manually

#### Method A: Nested For-Loops
```python
def manual_transpose(matrix: list[list[int]]) -> list[list[int]]:
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = []
    for c in range(cols):
        new_row = []
        for r in range(rows):
            new_row.append(matrix[r][c])
        transposed.append(new_row)
    return transposed
```

#### Method B: Nested List Comprehension
```python
transposed = [[matrix[r][c] for r in range(rows)] for c in range(cols)]
```
Notice: The outer comprehension iterates over `c in range(cols)` (building each new row of the transposed matrix), and the inner comprehension iterates over `r in range(rows)` (gathering elements from that column across all original rows).

### 4.3 Why Transposition Rotates and Flips
Transposition reflects an image across the main diagonal ($x = y$). Visually, this is equivalent to rotating the image by 90 degrees counter-clockwise followed by a horizontal flip (or a 90-degree clockwise rotation followed by a vertical flip). This matches the subject illustration of the rotated animal.

---

## 5. Syntax and Examples

### Step-by-Step Transpose Snippet
```python
import numpy as np

# 1. 2D slice from 3D array:
mono_2d = image[100:500, 450:850, 0]  # shape (400, 400)

# 2. Extract dimensions:
rows, cols = mono_2d.shape

# 3. Manual transpose without any library transpose:
transposed_list = [
    [mono_2d[r][c] for r in range(rows)]
    for c in range(cols)
]

# 4. Convert to NumPy array for display and shape checking:
transposed_arr = np.array(transposed_list)
print(f"New shape after Transpose: {transposed_arr.shape}")
```

---

## 6. How to Think About the Exercise

1. **Step 1: Load image and crop.** Load `"animal.jpeg"`, crop 400×400 slice, extract 1 channel.
2. **Step 2: Print sliced shape and content.** Print `The shape of image is: ...` and pixel array.
3. **Step 3: Manually transpose.** Write an explicit double-loop or comprehension swapping $r$ and $c$. Do NOT call `.T` or `np.transpose()`.
4. **Step 4: Convert and report.** Convert to `np.array`, print `New shape after Transpose: (400, 400)` and print the transposed array.
5. **Step 5: Display.** Render using `plt.imshow(transposed_arr, cmap="gray")` and `plt.show()`.
6. **Step 6: Handle errors cleanly.** Ensure no crash occurs on invalid inputs or missing files.

---

## 7. Guided Practice

**Practice 1 (Easiest — Manual transpose of a 3×3 matrix):**
Given a small matrix:
```python
mat = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
```
Write a manual transposition function using a nested list comprehension.

Expected output:
```python
[
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9]
]
```

<details><summary>Solution</summary>

```python
mat = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
transposed = [[mat[r][c] for r in range(len(mat))] for c in range(len(mat[0]))]
print(transposed)
```
</details>

**Practice 2 (Transposing a non-square 2×3 matrix):**
Verify that your transposition correctly changes shape from $(2, 3)$ to $(3, 2)$ on `[[1, 2, 3], [4, 5, 6]]`.

Expected output:
```python
[[1, 4], [2, 5], [3, 6]]
```

<details><summary>Solution</summary>

```python
mat = [[1, 2, 3], [4, 5, 6]]
rows, cols = len(mat), len(mat[0])
transposed = [[mat[r][c] for r in range(rows)] for c in range(cols)]
print(transposed)
```
</details>

**Practice 3 (Manual transpose on a 2D NumPy array):**
Take a 2D slice from an image array and manually transpose it into a new NumPy array without calling `.T` or `np.transpose()`.

Expected output:
```
New shape after Transpose: (400, 400)
```

<details><summary>Solution</summary>

```python
import numpy as np


def manual_transpose_array(arr_2d: np.ndarray) -> np.ndarray:
    """Manually transpose a 2D array without library transpose functions."""
    rows, cols = arr_2d.shape
    transposed = [
        [arr_2d[r, c] for r in range(rows)]
        for c in range(cols)
    ]
    return np.array(transposed)
```
</details>

**Practice 4 (Plotting transposed image with axes):**
Render `transposed_arr` with `plt.imshow` using `cmap="gray"`. Ensure axes are displayed.

Expected output:
A window displays the rotated/reflected raccoon with pixel coordinate axes.

<details><summary>Solution</summary>

```python
import matplotlib.pyplot as plt

plt.imshow(transposed_arr, cmap="gray")
plt.title("Transposed Image")
plt.show()
```
</details>

**Practice 5 (Hardest — the full, rule-compliant `rotate.py`):**
Write the complete `rotate.py` file with documentation, PEP 8 formatting, and `main()` function with error handling.

Expected output when running `python rotate.py`:
```
$> python rotate.py
The shape of image is: (400, 400, 1) or (400, 400)
[[[167]
  [180]
  [194]
  ...
  [102]
  [104]
  [103]]]
New shape after Transpose: (400, 400)
[[167 180 194 ...  64  50  72]
 ...
 [115 116 119 ... 102 104 103]]
```

<details><summary>Solution</summary>

```python
"""Program to crop and manually transpose a square part of an image."""

import matplotlib.pyplot as plt
import numpy as np
from load_image import ft_load


def manual_transpose(matrix: np.ndarray) -> np.ndarray:
    """Manually transpose a 2D matrix without library transpose functions.

    Args:
        matrix: 2D array of shape (rows, cols).

    Returns:
        New NumPy array of shape (cols, rows) containing transposed data.
    """
    rows, cols = matrix.shape
    transposed = [
        [matrix[r, c] for r in range(rows)]
        for c in range(cols)
    ]
    return np.array(transposed)


def main():
    """Load image, slice square part, transpose manually, and display."""
    try:
        image = ft_load("animal.jpeg")
        if image is None:
            raise FileNotFoundError("Could not load image 'animal.jpeg'.")

        # Slice 400x400 single-channel region
        zoomed_3d = image[100:500, 450:850, 0:1]
        print(f"The shape of image is: {zoomed_3d.shape}")
        print(zoomed_3d)

        # Squeeze to 2D for transposition
        zoomed_2d = zoomed_3d.squeeze()

        # Perform manual transpose
        transposed = manual_transpose(zoomed_2d)
        print(f"New shape after Transpose: {transposed.shape}")
        print(transposed)

        # Display rotated image
        plt.imshow(transposed, cmap="gray")
        plt.title("Transposed Animal")
        plt.show()

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
```
</details>

If your code executes cleanly without using any library transpose, you're done!

---

## 8. Exercise-Specific Knowledge

- **Evaluation Warning:** During peer evaluation, the evaluator will check your `rotate.py` for forbidden keywords:
  - `transpose`
  - `.T`
  - `swapaxes`
  - `rot90`
  Make sure your manual transposition code uses only custom loops/comprehensions.
- **Input Shape Format:** Slicing `[100:500, 450:850, 0:1]` produces `(400, 400, 1)`. Calling `.squeeze()` yields `(400, 400)` before transposing.
- **Expected Output:** The subject specifies `New shape after Transpose: (400, 400)`.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Using `np.transpose()` or `.T` | Easy shortcut | **Strictly forbidden** — write custom nested loops |
| Inverting loop variables | `[matrix[c, r] for c in ...] for r in ...` | Outer loop must iterate over columns $c$, inner over rows $r$ |
| Forgetting `.squeeze()` before transpose | 3D array has shape `(400, 400, 1)` | Index channel `[:, :, 0]` or `.squeeze()` to get 2D matrix |

---

## 10. Debugging Guide

- **Transposed array is identical to original**: You wrote `[matrix[r, c] for c in range(cols)] for r in range(rows)` instead of swapping the variables.
- **Plot is not rotated**: Check that you passed `transposed` to `plt.imshow()`, not `zoomed`.

---

## 11. Cheat Sheet

```python
# Manual transpose algorithm:
rows, cols = matrix.shape
transposed = np.array([
    [matrix[r, c] for r in range(rows)]
    for c in range(cols)
])
```

---

## 12. Knowledge Checklist

- [ ] I implemented matrix transposition manually using nested loops/comprehensions.
- [ ] I confirmed that neither `.T`, `np.transpose`, nor `swapaxes` are used anywhere in `rotate.py`.
- [ ] I displayed the transposed image using `matplotlib` with axes and scales.
- [ ] My printed output matches the required shapes `(400, 400, 1)` and `(400, 400)`.
- [ ] My code conforms to PEP 8 and passes `flake8` without warnings.
