# Study Tutorial — Module 1, Exercise 04: rotate.py

## 1. Exercise Overview

**What it asks:** Load `animal.jpeg`, crop a square region from it (similar to Exercise 03), then **transpose** it yourself — manually, without using a library's built-in transpose method — to produce a rotated-looking image. Display the result and print the new shape and data.

**Main concepts you'll learn:**
- What a "transpose" operation actually does, mathematically
- Implementing transpose manually with nested loops (no shortcuts allowed)
- Why transposing a 2D grid visually looks like a rotation/flip
- The difference between "using a tool" and "understanding what the tool does underneath"

**Why this matters:** `.T` or `.transpose()` in NumPy/pandas is something you'll call constantly without a second thought — but this exercise forces you to build it from scratch once, so you deeply understand what's happening to the data's layout. That understanding pays off later when you're debugging shape mismatches in real array/DataFrame code.

**Skills after completing it:**
- Understand transpose as "swap rows and columns"
- Implement transpose manually using nested loops and index manipulation
- Recognize when reaching for a shortcut method is (and isn't) appropriate

---

## 2. Prerequisites

- Exercise 03's cropping/slicing concepts
- Nested loops (`for` inside `for`)
- 2D indexing: `array[row][col]` or `array[row, col]`

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| Nested `for` loops | Iterate over every row and column combination | Used to build the transposed array by hand |
| `numpy.zeros((rows, cols))` | Creates an array of zeros with a given shape, as a canvas to fill in | Useful for pre-allocating the transposed result |
| **Forbidden:** `.T`, `.transpose()`, `np.transpose()` | NumPy's built-in transpose | Explicitly disallowed for this exercise — you must implement it yourself |

Common pitfalls:
- Reaching for `.T` out of habit — the subject is explicit: *"You have to do the transpose yourself, no library is allowed for the transpose."*
- Mixing up which index becomes which after transposing — the value at `original[i][j]` must end up at `transposed[j][i]`, not the other way around.
- Forgetting to size your output array correctly: if the input is `(H, W)`, the transposed output must be `(W, H)` — swapped, not identical.

---

## 4. Concepts You Need to Learn

### 4.1 What transpose means
Transposing a 2D array swaps its rows and columns: the element at row `i`, column `j` in the original ends up at row `j`, column `i` in the result.
```
Original (2x3):        Transposed (3x2):
1 2 3                    1 4
4 5 6                    2 5
                          3 6
```
Notice the shape itself flips: a `(2, 3)` array becomes `(3, 2)`.

### 4.2 Why this looks like a "rotation" visually
For an image, swapping rows and columns effectively reflects the image across its main diagonal — visually this often *looks* similar to a rotation combined with a flip, which is why this exercise is titled "rotate me," even though the underlying operation is a transpose, not a true rotation.

### 4.3 Implementing it manually
The core idea: build a new array where `new[j][i] = old[i][j]` for every valid `i`, `j`.
```python
def my_transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0] * rows for _ in range(cols)]  # note: shape swapped!
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result
```

---

## 5. Syntax and Examples

### Small hand-worked example
```python
matrix = [[1, 2, 3],
          [4, 5, 6]]
# shape (2, 3)

def my_transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result

print(my_transpose(matrix))
# [[1, 4], [2, 5], [3, 6]]
```
Walking through it: `rows = 2`, `cols = 3`, so `result` starts as a `3×2` grid of zeros. For `i=0, j=0`: `matrix[0][0] = 1` goes to `result[0][0]`. For `i=0, j=1`: `matrix[0][1] = 2` goes to `result[1][0]`. And so on — every value's row/column position is swapped.

### Building the empty result grid correctly
```python
rows, cols = 2, 3
result = [[0] * rows for _ in range(cols)]
print(result)
# [[0, 0], [0, 0], [0, 0]]  -- 3 rows of 2 zeros each: the SWAPPED shape
```
Be careful: `[[0] * rows for _ in range(cols)]` uses `cols` as the *outer* loop count and `rows` as the *inner* list length — that's intentional, since the output shape is `(cols, rows)`.

### Applying it to a NumPy array
If you're working with a NumPy array (as is likely, given Exercise 02/03), you can still index it with `[i, j]` instead of `[i][j]`:
```python
import numpy as np

def my_transpose(arr):
    rows, cols = arr.shape[0], arr.shape[1]
    result = np.zeros((cols, rows), dtype=arr.dtype)
    for i in range(rows):
        for j in range(cols):
            result[j, i] = arr[i, j]
    return result
```

---

## 6. How to Think About the Exercise

1. Load the image and crop a square region, just as in Exercise 03 (the subject builds directly on that pattern).
2. Note the cropped array's shape — for a 2D (single-channel) array, transpose swaps the two dimensions; if you're working with a 3D array (with a channel axis of size 1 or 3), think about whether you're transposing just the spatial axes or restructuring all three — the exercise's example works with a single-channel `(400, 400, 1)`/`(400, 400)` image, which simplifies this to a clean 2D transpose.
3. Implement `my_transpose` (or whatever you name it) using nested loops — no `.T`, no `.transpose()`.
4. Print the new shape (rows and columns swapped) and the transposed data.
5. Display the transposed result — note how it visually looks rotated/flipped compared to the original.
6. As always, wrap this in error handling so bad/missing image files don't crash the program.

---

## 7. Guided Practice

**Practice 1 (Easy):** By hand (on paper or in your head), transpose the matrix `[[1, 2], [3, 4]]`.
<details><summary>Solution</summary>

```
[[1, 3], [2, 4]]
```
Element at (0,1)=2 moves to (1,0); element at (1,0)=3 moves to (0,1).
</details>

**Practice 2 (Easy):** Write a function that returns the shape `(rows, cols)` a matrix *would have* after transposing, without actually transposing it.
<details><summary>Solution</summary>

```python
def transposed_shape(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    return (cols, rows)  # swapped!
```
</details>

**Practice 3 (Medium):** Implement `my_transpose` for a plain list-of-lists matrix, and verify it against a 3×2 example.
<details><summary>Solution</summary>

```python
def my_transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0] * rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result

m = [[1, 2], [3, 4], [5, 6]]  # shape (3, 2)
print(my_transpose(m))  # [[1, 3, 5], [2, 4, 6]] -- shape (2, 3)
```
</details>

**Practice 4 (Close to the real exercise):** Adapt your manual transpose to work on a NumPy 2D array using `[i, j]` indexing instead of `[i][j]`.
<details><summary>Solution</summary>

```python
import numpy as np

def my_transpose(arr):
    rows, cols = arr.shape
    result = np.zeros((cols, rows), dtype=arr.dtype)
    for i in range(rows):
        for j in range(cols):
            result[j, i] = arr[i, j]
    return result

test = np.array([[1, 2, 3], [4, 5, 6]])
print(my_transpose(test))
# [[1 4]
#  [2 5]
#  [3 6]]
```
</details>

---

## 8. Exercise-Specific Knowledge

- The subject explicitly forbids using any library's transpose function — you must implement it with your own logic (nested loops).
- The example works from a square-cropped, single-channel image (following the same crop pattern as Exercise 03): original shape `(400, 400, 1)`/`(400, 400)`, transposed to `(400, 400)`.
- Must print the shape *and* data both before and after the transpose, and display the transposed image.
- Must reuse `load_image.py`; turn in both `load_image.py` and `rotate.py`.
- Your specific pixel values/crop region can differ from the subject's example — only the *mechanism* (manual transpose) is graded strictly.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Using `.T` or `.transpose()` "just to check," then forgetting to remove it | Convenient built-in, easy to leave in by accident | Double-check your final submission has no transpose shortcuts anywhere |
| Building the result array with the *original* (unswapped) shape | Not realizing the output dimensions are swapped from the input | Result shape must be `(cols, rows)` if the input was `(rows, cols)` |
| Index swap done backwards (`result[i][j] = matrix[j][i]` vs. `result[j][i] = matrix[i][j]`) | Both look superficially similar | Carefully verify with a small hand-worked example first, like the `[[1,2],[3,4]]` → `[[1,3],[2,4]]` case |
| Applying manual transpose logic to a 3-channel image without adjusting for the channel axis | Treating a 3D array exactly like a 2D one | For multi-channel data, decide explicitly whether you're transposing per-channel or reducing to a single channel first (as the example does) |

---

## 10. Debugging Guide

- **Output shape isn't swapped** → check your result array's initial allocation uses `(cols, rows)`, not `(rows, cols)`.
- **Values look scrambled, not cleanly transposed** → verify your index assignment direction with the smallest possible hand-worked example (a 2×2 matrix) before trusting it on the full image.
- **`IndexError` in the nested loop** → double-check your loop ranges (`range(rows)`, `range(cols)`) match the *original* array's dimensions, not the (swapped) result's.
- Useful inspection: test your `my_transpose` against NumPy's own `.T` on a small throwaway array (`np.array_equal(my_transpose(test), test.T)`) purely as a *local sanity check* — just don't ship `.T` in your final submission.

---

## 11. Cheat Sheet

```python
def my_transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    result = [[0] * rows for _ in range(cols)]  # note swapped dims
    for i in range(rows):
        for j in range(cols):
            result[j][i] = matrix[i][j]
    return result
```

Key rule: `new[j][i] = old[i][j]` — row/column indices swap on assignment.

---

## 12. Knowledge Checklist

- [ ] I can explain what transpose does to a matrix's shape and values.
- [ ] I can implement transpose manually with nested loops, without using a built-in method.
- [ ] I understand why the output shape's dimensions are swapped relative to the input.
- [ ] I can verify my manual implementation against a small, hand-worked example.
- [ ] I understand why forcing a manual implementation here builds real intuition for what `.T` does later.
