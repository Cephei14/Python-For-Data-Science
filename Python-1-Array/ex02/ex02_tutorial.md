# Study Tutorial — Module 1, Exercise 02: load_image.py

## 1. Exercise Overview

**What it asks:** Write a function `ft_load(path)` that loads an image file from disk and returns it as an array of pixel values (RGB), printing its shape along the way. It must support at least JPG/JPEG, and handle errors (missing file, unsupported format, etc.) with clear messages.

**Main concepts you'll learn:**
- What a digital image *is*, structurally — a 3D array of numbers
- How color images are represented (height × width × channels)
- Using an image-loading library to convert a file into an array
- Handling file-related errors (missing files, bad formats)

**Why this matters:** This is your first encounter with a real-world, non-trivial "array" as used in data science: an image. Every computer vision task, and many data-science pipelines that include images (medical imaging, satellite data, product photos), start from exactly this operation — load a file, get back a numeric array you can compute on. Understanding the shape `(height, width, channels)` is foundational.

**Skills after completing it:**
- Load an image file into a NumPy array using a library like PIL/Pillow
- Understand and report an image's shape
- Handle file I/O errors gracefully

---

## 2. Prerequisites

- Basic file paths and the idea that files can fail to open (don't exist, wrong permissions, wrong format)
- What an "array" is conceptually — organized numeric data with a defined shape (from Exercise 01)
- No prior image-processing knowledge assumed — taught below

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `PIL.Image.open(path)` (from the Pillow library) | Opens an image file, returns an `Image` object | Install with `pip install Pillow`; import as `from PIL import Image` |
| `numpy.array(image)` | Converts a PIL `Image` object into a NumPy array of pixel values | This is the standard image → array bridge |
| `array.shape` | A NumPy array attribute giving its dimensions as a tuple | For a color image: `(height, width, channels)` |
| `try / except` | Catches errors during file loading | Used to handle missing files, corrupt images, unsupported formats |

Common pitfalls:
- Confusing width and height order — NumPy image arrays are `(height, width, channels)`, but when people casually say "an image is 450×257," they often mean width×height, which is the *reverse* order from the array shape. Always check `.shape` directly rather than assuming.
- Forgetting to actually convert the PIL `Image` into a NumPy array — `Image.open()` alone gives you a PIL object, not an array; you need `np.array(img)` on top.
- Not handling the case where the file doesn't exist — this raises `FileNotFoundError`, which you're expected to catch and report clearly rather than letting the program crash.

---

## 4. Concepts You Need to Learn

### 4.1 What a digital color image actually is
A color image is a 3-dimensional grid of numbers:
- **Height**: number of rows of pixels (top to bottom)
- **Width**: number of columns of pixels (left to right)
- **Channels**: usually 3 numbers per pixel — Red, Green, Blue — each ranging 0–255

So a `257 × 450` pixel color photo is stored as an array of shape `(257, 450, 3)`: for every one of the 257×450 = 115,650 pixels, there are 3 numbers describing its color.

### 4.2 Loading with Pillow + NumPy
```python
from PIL import Image
import numpy as np

img = Image.open("landscape.jpg")   # a PIL Image object
arr = np.array(img)                  # a NumPy array of pixel values
print(arr.shape)                     # (257, 450, 3)
```

### 4.3 Handling errors clearly
Two common failure modes:
- The file doesn't exist → `FileNotFoundError`
- The file exists but isn't a valid/supported image → various errors depending on the library (e.g. `PIL.UnidentifiedImageError`)

```python
try:
    img = Image.open(path)
except FileNotFoundError:
    print(f"Error: file '{path}' not found.")
except Exception as e:
    print(f"Error: could not load image ({e}).")
```

---

## 5. Syntax and Examples

### Basic load and shape print
```python
from PIL import Image
import numpy as np

def ft_load(path):
    img = Image.open(path)
    arr = np.array(img)
    print(f"The shape of image is: {arr.shape}")
    return arr
```
Small example: loading a tiny 2×2 test image would give `arr.shape == (2, 2, 3)` if it's RGB.

### With error handling
```python
def ft_load(path):
    try:
        img = Image.open(path)
    except FileNotFoundError:
        print(f"Error: '{path}' does not exist.")
        return None
    except Exception as e:
        print(f"Error: unable to load image ({e}).")
        return None
    arr = np.array(img)
    print(f"The shape of image is: {arr.shape}")
    return arr
```
Note: returning `None` on error is one valid approach; the important part (per the subject) is that the program doesn't crash and prints something clear.

### Inspecting pixel values
```python
arr = ft_load("landscape.jpg")
print(arr)
# [[[19 42 83]
#   [23 42 84]
#   ...
```
Each innermost group of 3 numbers `[19 42 83]` is one pixel's Red, Green, Blue values.

---

## 6. How to Think About the Exercise

1. Pick an image-loading library — Pillow (`PIL`) is the most common and beginner-friendly choice, though the subject allows "all libs for load images."
2. Load the file, wrapped in error handling, since a bad path or unsupported format shouldn't crash the program.
3. Convert the loaded image into a NumPy array — this is the actual "load my image as data" step.
4. Print the shape, matching the format `"The shape of image is: (H, W, C)"`.
5. Return the array (or print it, per the subject's tester which does `print(ft_load(...))`).
6. Test with both a valid JPG and a deliberately bad path, to confirm your error handling actually triggers and prints something clear rather than an ugly traceback.

---

## 7. Guided Practice

**Practice 1 (Easy):** Load any image file on your system with PIL and print its `.size` (note: PIL's own `.size` is `(width, height)` — different order from a NumPy array's `.shape`!).
<details><summary>Solution</summary>

```python
from PIL import Image
img = Image.open("some_image.jpg")
print(img.size)  # (width, height)
```
</details>

**Practice 2 (Easy):** Convert that same image to a NumPy array and print its `.shape`.
<details><summary>Solution</summary>

```python
import numpy as np
arr = np.array(img)
print(arr.shape)  # (height, width, channels)
```
</details>

**Practice 3 (Medium):** Write a function that safely tries to open a file path, returning `None` and printing a friendly message if the file doesn't exist.
<details><summary>Solution</summary>

```python
def safe_open(path):
    try:
        return Image.open(path)
    except FileNotFoundError:
        print(f"Error: '{path}' not found.")
        return None
```
</details>

**Practice 4 (Close to the real exercise):** Combine loading, array conversion, shape printing, and error handling into one `ft_load` function.
<details><summary>Solution</summary>

```python
from PIL import Image
import numpy as np

def ft_load(path):
    """Load an image file and return it as a NumPy array."""
    try:
        img = Image.open(path)
    except Exception as e:
        print(f"Error: {e}")
        return None
    arr = np.array(img)
    print(f"The shape of image is: {arr.shape}")
    return arr
```
</details>

---

## 8. Exercise-Specific Knowledge

- Prototype: `def ft_load(path: str) -> array:` — the return type is flexible ("you can return to the desired format"), but a NumPy array is the natural and expected choice.
- Must handle, at minimum, JPG and JPEG formats.
- Must print `"The shape of image is: (H, W, C)"` and the pixel content.
- Any error must be handled clearly (no raw traceback / crash).
- Allowed tools: "all libs for load images and table manipulation" — Pillow + NumPy is the standard combo, but OpenCV (`cv2`) or `imageio` are also acceptable if you prefer.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Confusing `.size` (PIL, width×height) with `.shape` (NumPy, height×width×channels) | Different libraries, different conventions | Always double-check by printing `.shape` directly rather than assuming |
| Forgetting to convert to a NumPy array at all | Returning the raw PIL `Image` object | Wrap with `np.array(img)` before returning |
| Letting a missing file crash the program | No `try/except` around `Image.open()` | Always wrap file loading in error handling |
| Only testing with a perfectly valid file | Not exercising the error path | Deliberately test with a nonexistent path too |

---

## 10. Debugging Guide

- **`FileNotFoundError`** → the path is wrong or the file doesn't exist; print the path you attempted to help debug.
- **`PIL.UnidentifiedImageError`** → the file exists but isn't a recognized image format (or is corrupted); catch this alongside `FileNotFoundError`.
- **Shape has only 2 dimensions instead of 3** → the image might be grayscale (no color channels) rather than RGB — this is expected for grayscale images and will matter again in Exercise 03/04.
- Useful inspection: `print(type(img))` right after `Image.open()` to confirm you actually got a valid `Image` object before converting to an array.

---

## 11. Cheat Sheet

```python
from PIL import Image
import numpy as np

img = Image.open(path)      # PIL Image object
arr = np.array(img)          # NumPy array, shape (H, W, C)
arr.shape                    # (height, width, channels)

try:
    ...
except FileNotFoundError:
    ...
except Exception as e:
    ...
```

---

## 12. Knowledge Checklist

- [ ] I can explain what a digital color image's shape `(H, W, C)` represents.
- [ ] I can load an image file into a NumPy array using Pillow.
- [ ] I know the difference between PIL's `.size` and NumPy's `.shape`.
- [ ] I can handle file-loading errors without crashing the program.
- [ ] I understand images are just structured numeric arrays, setting up the next exercises (slicing, transposing, filtering images).
