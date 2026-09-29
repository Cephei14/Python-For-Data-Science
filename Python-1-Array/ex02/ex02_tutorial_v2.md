# Study Tutorial — Exercise 02: load_image.py

## 1. Exercise Overview

**What it asks:**
Create a module named `load_image.py` in directory `ex02/` containing a function:
```python
def ft_load(path: str) -> array:
```
- Loads an image file from the specified `path`.
- Prints the dimensions/format of the image:
  `The shape of image is: (<height>, <width>, <channels>)`
- Returns the pixel contents of the image in **RGB format** as a NumPy array.
- Must support at least **JPG** and **JPEG** image formats.
- Must handle all errors gracefully (non-existent file, unsupported formats, corrupt files, permission issues, non-string paths) with a **clear error message**.

**Rules and Constraints:**
- Must not crash on errors; unhandled exceptions will invalidate the exercise.
- Follow all 42 Python Norm rules: PEP 8 / `flake8` compliance, function and module docstrings, type annotations, and a `main()` function.
- Note: This `load_image.py` module will be **reused directly in exercises 03, 04, and 05**, so making it solid and modular is essential.

**Main concepts you'll learn:**
- Digital image representation in memory as a 3D tensor: $(\text{height}, \text{width}, \text{channels})$.
- Reading image files using Pillow (`PIL.Image`).
- Converting PIL Image objects into numeric NumPy arrays (`np.ndarray`).
- Ensuring the array is strictly in RGB format (converting from RGBA, Grayscale, or CMYK).
- Robust file I/O error handling.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **Array Shapes (Module 1 ex01):** Understanding dimensions like `(rows, cols)` which translate to `(height, width)` for images.
- **Error Handling (Module 0 ex04, ex05):** Using `try ... except` blocks to catch specific exceptions (`FileNotFoundError`, `OSError`, `ValueError`).
- **Module Imports (Module 0 ex01):** Importing and organizing functions across files.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `from PIL import Image` | Python Imaging Library (Pillow) for opening images | `pip install Pillow` |
| `import numpy as np` | High-performance array computing library | Standard for image arrays |
| `Image.open(path)` | Opens and identifies the given image file lazily | Raises `FileNotFoundError` or `UnidentifiedImageError` |
| `img.convert('RGB')` | Ensures image data has exactly 3 channels (Red, Green, Blue) | Converts RGBA, Grayscale, CMYK safely |
| `np.array(img)` | Converts the PIL Image object into a NumPy array | Yields an array with dtype `uint8` |
| `array.shape` | Tuple representing dimensions: `(height, width, channels)` | Height = rows, Width = columns |
| `os.path.exists(path)` | Checks if a file exists on disk | Useful for early validation |

**Common pitfalls:**
- **Height vs. Width Ordering:** In everyday speech, people say an image is "1920x1080" (width × height). But in NumPy and image processing matrices, the first dimension is **height (rows)** and the second dimension is **width (columns)**: `(height, width, channels)`. For `landscape.jpg`, shape is `(257, 450, 3)` (257 rows high, 450 columns wide).
- **Forgetting `.convert('RGB')`:** If a user passes an image with transparency (PNG/RGBA) or a single-channel grayscale image, `np.array(img)` will have shape `(H, W, 4)` or `(H, W)`. Calling `.convert('RGB')` guarantees 3 channels.
- **Forgetting to Close or Release Files:** Using a `with Image.open(path) as img:` context manager ensures file descriptors are cleaned up immediately.
- **Crashing on Missing Files:** Evaluators will test non-existent paths like `python tester.py "non_existent.jpg"`. The function must catch `FileNotFoundError` or check existence and print a clear error message.

---

## 4. Concepts You Need to Learn

### 4.1 How Computers Store Images
A digital color image is represented as a 3D grid of numbers:
- **Dimension 1 (Height / Rows):** Pixel row index from top ($0$) to bottom ($H-1$).
- **Dimension 2 (Width / Columns):** Pixel column index from left ($0$) to right ($W-1$).
- **Dimension 3 (Color Channels):** Typically 3 values:
  - Channel 0: **Red** (intensity $0$ to $255$)
  - Channel 1: **Green** (intensity $0$ to $255$)
  - Channel 2: **Blue** (intensity $0$ to $255$)

A pixel with value `[255, 0, 0]` is pure bright red. `[0, 0, 0]` is black, and `[255, 255, 255]` is white.

### 4.2 Loading with Pillow and Converting to NumPy
```python
from PIL import Image
import numpy as np

# Open image file
with Image.open("landscape.jpg") as img:
    # Ensure standard RGB format
    rgb_img = img.convert("RGB")
    # Convert to NumPy array
    arr = np.array(rgb_img)

print(arr.shape)  # e.g., (257, 450, 3)
```

### 4.3 Error Handling Requirements
The subject states:
> *"You have to handle, at least, JPG and JPEG format."*
> *"You need to handle any error with a clear error message"*

Errors to guard against:
1. `path` is not a string (`TypeError`).
2. File does not exist (`FileNotFoundError`).
3. File is not an image or is corrupted (`PIL.UnidentifiedImageError` or `OSError`).
4. File extension is not supported (`.jpg` or `.jpeg`).

---

## 5. Syntax and Examples

### Complete Loading Pattern
```python
import os
from PIL import Image, UnidentifiedImageError
import numpy as np


def ft_load(path: str) -> np.ndarray:
    """Load an image, print its shape, and return its RGB pixel array."""
    try:
        if not isinstance(path, str):
            raise TypeError("Path must be a string.")
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: '{path}'")
        if not path.lower().endswith((".jpg", ".jpeg")):
            raise ValueError("Unsupported format: only JPG and JPEG supported.")

        with Image.open(path) as img:
            rgb_img = img.convert("RGB")
            arr = np.array(rgb_img)
            print(f"The shape of image is: {arr.shape}")
            return arr
    except Exception as error:
        print(f"Error: {error}")
        return None
```

---

## 6. How to Think About the Exercise

1. **Step 1: Validate input parameter.** Ensure `path` is a non-empty string.
2. **Step 2: Check file accessibility.** Verify file existence and validate the extension.
3. **Step 3: Open and format image.** Use Pillow's `Image.open()`, convert to RGB with `.convert('RGB')`.
4. **Step 4: Convert to array and report shape.** Transform to NumPy array, print `The shape of image is: <shape>`.
5. **Step 5: Return array.** Return the resulting `np.ndarray`.
6. **Step 6: Handle all exceptions.** Wrap everything in a `try ... except` block so any problem prints a helpful error message instead of an unhandled crash.

---

## 7. Guided Practice

**Practice 1 (Easiest — Open an image with Pillow):**
Write a Python snippet to open an image `"landscape.jpg"` using Pillow, convert it to RGB, and print its format and size.

Expected output:
```python
RGB (450, 257)
```
*(Note that PIL's `.size` is `(width, height)`, reverse of NumPy's `(height, width)`).*

<details><summary>Solution</summary>

```python
from PIL import Image

with Image.open("landscape.jpg") as img:
    rgb = img.convert("RGB")
    print(rgb.mode, rgb.size)
```
</details>

**Practice 2 (Convert image to NumPy array and inspect):**
Convert the loaded image into a NumPy array, print its `.shape`, data type (`.dtype`), and the RGB values of the top-left pixel.

Expected output:
```python
Shape: (257, 450, 3)
Dtype: uint8
Top-left pixel: [19 42 83]
```

<details><summary>Solution</summary>

```python
from PIL import Image
import numpy as np

with Image.open("landscape.jpg") as img:
    arr = np.array(img.convert("RGB"))
    print(f"Shape: {arr.shape}")
    print(f"Dtype: {arr.dtype}")
    print(f"Top-left pixel: {arr[0, 0]}")
```
</details>

**Practice 3 (Format shape printing and return):**
Write a function `load_simple(path)` that prints `The shape of image is: (H, W, C)` and returns the array.

Expected output:
```
The shape of image is: (257, 450, 3)
```

<details><summary>Solution</summary>

```python
from PIL import Image
import numpy as np


def load_simple(path: str) -> np.ndarray:
    """Load image and display shape."""
    with Image.open(path) as img:
        arr = np.array(img.convert("RGB"))
        print(f"The shape of image is: {arr.shape}")
        return arr
```
</details>

**Practice 4 (Error handling for invalid paths and corrupt files):**
Add checks for non-existent files, wrong extensions, and non-image files. Ensure the function catches all exceptions and prints `Error: <message>`.

Expected output:

| Call | Result |
|---|---|
| `ft_load("landscape.jpg")` | Prints shape and returns array |
| `ft_load("non_existent.jpg")` | Prints `Error: File not found...` and returns `None` |
| `ft_load("text.txt")` | Prints `Error: Unsupported format...` and returns `None` |

<details><summary>Solution</summary>

```python
import os
from PIL import Image, UnidentifiedImageError
import numpy as np


def ft_load(path: str) -> np.ndarray | None:
    """Load image with comprehensive error checks."""
    try:
        if not isinstance(path, str):
            raise TypeError("Path must be a string.")
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: '{path}'")
        if not path.lower().endswith((".jpg", ".jpeg")):
            raise ValueError("Unsupported format: expected .jpg or .jpeg")
        with Image.open(path) as img:
            arr = np.array(img.convert("RGB"))
            print(f"The shape of image is: {arr.shape}")
            return arr
    except Exception as error:
        print(f"Error: {error}")
        return None
```
</details>

**Practice 5 (Hardest — the full, rule-compliant `load_image.py`):**
Write the complete module with prototypes, full type annotations, docstrings, and a `main()` function testing the tester commands.

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
```

<details><summary>Solution</summary>

```python
"""Module to load image files and return RGB pixel arrays."""

import os
from PIL import Image, UnidentifiedImageError
import numpy as np


def ft_load(path: str) -> np.ndarray:
    """Load an image from disk, display its dimensions, and return RGB pixels.

    Args:
        path: Path to the image file (JPG or JPEG).

    Returns:
        NumPy ndarray containing the RGB pixel values, or None on error.

    Raises:
        AssertionError: If arguments or file formats are invalid.
    """
    try:
        if not isinstance(path, str):
            raise AssertionError("Path must be a string.")
        if not os.path.exists(path):
            raise AssertionError(f"No such file: '{path}'")
        if not path.lower().endswith((".jpg", ".jpeg")):
            raise AssertionError("Format not supported: only JPG/JPEG allowed.")

        with Image.open(path) as img:
            rgb_img = img.convert("RGB")
            arr = np.array(rgb_img)
            print(f"The shape of image is: {arr.shape}")
            return arr

    except (UnidentifiedImageError, AssertionError, Exception) as error:
        print(f"Error: {error}")
        return None


def main():
    """Test loading valid and invalid image files."""
    try:
        print(ft_load("landscape.jpg"))
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
```
</details>

If your test output matches the subject exactly and passes `flake8`, you're done!

---

## 8. Exercise-Specific Knowledge

- **Exact Subject Tester (`tester.py`):**
  ```python
  from load_image import ft_load

  print(ft_load("landscape.jpg"))
  ```
  Expected output:
  ```
  The shape of image is: (257, 450, 3)
  [[[19 42 83]
    [23 42 84]
    [28 43 84]
    ...
    [ 0  0  0]
    [ 1  1  1]
    [ 1  1  1]]]
  ```
- **Reuse in Later Exercises:** You will copy or import this exact `ft_load` in `ex03` (`zoom.py`), `ex04` (`rotate.py`), and `ex05` (`pimp_image.py`). Make sure it is bug-free!
- **Displaying the Pixel Array:** Note that `ft_load` prints the shape string internally, and returning the array causes `print(ft_load(...))` in `tester.py` to print the NumPy array representation.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Crashing on non-existent file | Not catching `FileNotFoundError` | Use `try ... except` and check `os.path.exists()` |
| Shape has 4 channels (RGBA) | Loading PNG or transparent JPG | Always call `.convert("RGB")` |
| Printing `(width, height)` | Using PIL `.size` directly | Use `arr.shape` which is `(height, width, channels)` |
| Leaving files open | Calling `Image.open()` without context manager | Use `with Image.open(path) as img:` |

---

## 10. Debugging Guide

- **`UnidentifiedImageError: cannot identify image file`**: The file is corrupt or is not an image (e.g. a text file renamed to `.jpg`). Catch this exception and display a clear error message.
- **NumPy array has 2 dimensions instead of 3**: The image is black-and-white (grayscale). `.convert("RGB")` converts it into 3 equal channels `(H, W, 3)`.

---

## 11. Cheat Sheet

```python
from PIL import Image
import numpy as np

# Load RGB image to NumPy array:
with Image.open(path) as img:
    arr = np.array(img.convert("RGB"))

# Report shape:
print(f"The shape of image is: {arr.shape}")
```

---

## 12. Knowledge Checklist

- [ ] I understand why an image array has shape `(height, width, channels)`.
- [ ] I can load image files using Pillow and convert them to NumPy arrays.
- [ ] I use `.convert("RGB")` to enforce 3-channel RGB mode.
- [ ] I handled all file I/O error scenarios with clear messages.
- [ ] My code conforms to PEP 8 and passes `flake8` without warnings.
