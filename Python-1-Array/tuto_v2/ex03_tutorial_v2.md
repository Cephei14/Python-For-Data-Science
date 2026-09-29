# Study Tutorial — Exercise 03: zoom.py

## 1. Exercise Overview

**What it asks:**
Create a program named `zoom.py` (along with `load_image.py`) in directory `ex03/` that:
1. Loads the image `"animal.jpeg"` using `ft_load` from `load_image.py`.
2. Prints initial information about the loaded image:
   - Dimensions on X and Y axes and number of channels: `The shape of image is: (768, 1024, 3)`
   - The initial RGB pixel contents.
3. Crops/slices a square region (400×400 pixels) centered on the interesting part of the image (the animal's face).
4. Converts the crop to a single color channel (grayscale) with shape `(400, 400, 1)` or `(400, 400)`.
5. Prints the new sliced shape and its pixel data:
   `New shape after slicing: (400, 400, 1)` (or `(400, 400)`)
   Followed by the pixel content array.
6. Displays the zoomed image using `matplotlib.pyplot.imshow()`:
   - Uses a grayscale colormap (`cmap="gray"`).
   - Displays numeric scale ticks on both the X and Y axes.
7. Must handle all errors gracefully without crashing abruptly.

**Rules and Constraints:**
- The program must not crash if the image is missing or corrupted; catch exceptions and display clear messages.
- Must follow 42 Python Norm rules: PEP 8 / `flake8` clean, docstrings on all functions and modules, type annotations, and a `main()` function.

**Main concepts you'll learn:**
- Multi-dimensional array slicing on image tensors: `image[y_start:y_end, x_start:x_end, channel_slice]`.
- Channel reduction and grayscale conversion.
- Rendering images with coordinate axes and custom colormaps using `matplotlib.pyplot`.
- Structuring multi-file Python projects.

---

## 2. Prerequisites (What You Know From Earlier Exercises)

- **2D Slicing (Module 1 ex01):** Understanding slicing ranges `[start:end]` and indexing.
- **Image Loading & NumPy Arrays (Module 1 ex02):** Using `ft_load()` to obtain an image tensor of shape `(H, W, 3)`.
- **Exception Handling (Module 0 ex04, ex05):** Encapsulating execution inside `try ... except` blocks in `main()`.

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `from load_image import ft_load` | Reuses the image loading function from ex02 | Loads file and returns RGB array |
| `import matplotlib.pyplot as plt` | Plotting library for displaying images and graphs | `pip install matplotlib` |
| `array[y1:y2, x1:x2]` | NumPy 2D slicing for spatial cropping | `y` is height (rows), `x` is width (columns) |
| `array[..., 0:1]` | Channel slicing keeping the 3rd dimension | Results in shape `(H, W, 1)` |
| `array[..., 0]` | Channel indexing collapsing the 3rd dimension | Results in shape `(H, W)` |
| `plt.imshow(img, cmap="gray")` | Renders array as an image in grayscale | Required to visualize single-channel images |
| `plt.show()` | Opens interactive GUI window displaying the plot | Displays pixel coordinate scales on axes |

**Common pitfalls:**
- **$(X, Y)$ vs $(Y, X)$ Row-Column Inversion:** In coordinate geometry, you write $(x, y)$. In NumPy matrices and image arrays, index order is `[row, column]`, which is `[y, x]`!
  - `y1:y2` selects vertical rows (height).
  - `x1:x2` selects horizontal columns (width).
- **Losing the Channel Dimension:** Slicing `array[y1:y2, x1:x2, 0]` produces shape `(400, 400)`. Slicing `array[y1:y2, x1:x2, 0:1]` preserves the channel dimension as `(400, 400, 1)`. The subject accepts either: `(400, 400, 1) or (400, 400)`.
- **Forgetting `cmap="gray"`:** If you pass a 2D array to `plt.imshow()` without `cmap="gray"`, Matplotlib defaults to the `'viridis'` colormap (green/yellow/purple) instead of black & white!
- **Missing Axis Ticks:** Matplotlib displays axis ticks by default. Do not call `plt.axis("off")`, because the subject requires: *"Display the scale on the x and y axis on the image"*.

---

## 4. Concepts You Need to Learn

### 4.1 Cropping an Image with NumPy Slicing
In a 3D NumPy array `arr[height, width, channels]`:
- To crop a vertical range from row $100$ to row $500$ (height of $400$ pixels): `100:500`.
- To crop a horizontal range from column $450$ to column $850$ (width of $400$ pixels): `450:850`.
```python
cropped = arr[100:500, 450:850]
print(cropped.shape)  # (400, 400, 3)
```

### 4.2 Slicing a Single Channel (Grayscale / Mono)
To isolate a single channel while keeping the 3D tensor shape `(400, 400, 1)`:
```python
mono = cropped[:, :, 0:1]
print(mono.shape)  # (400, 400, 1)
```
Or to produce a 2D array of shape `(400, 400)`:
```python
mono = cropped[:, :, 0]
print(mono.shape)  # (400, 400)
```
Both are explicitly permitted by the subject.

### 4.3 Displaying with Matplotlib
```python
import matplotlib.pyplot as plt

# If mono has shape (400, 400, 1), squeeze it to (400, 400) for imshow
display_arr = mono.squeeze() if mono.ndim == 3 else mono

plt.imshow(display_arr, cmap="gray")
plt.title("Zoom on Animal")
plt.xlabel("X axis (pixels)")
plt.ylabel("Y axis (pixels)")
plt.show()
```

---

## 5. Syntax and Examples

### Finding the Animal's Face Coordinates
Given `animal.jpeg` of size `(768, 1024, 3)`:
- Raccoon face is roughly between rows $100$ and $500$, and columns $450$ and $850$.
- Slicing:
  ```python
  zoomed = image[100:500, 450:850, 0:1]
  ```

---

## 6. How to Think About the Exercise

1. **Step 1: Load image.** Call `ft_load("animal.jpeg")`. If loading fails (`None` returned), exit cleanly.
2. **Step 2: Print original image info.** Print original pixel array representation.
3. **Step 3: Crop 400×400 region.** Slice rows and columns `[100:500, 450:850, 0:1]`.
4. **Step 4: Print zoomed shape and data.**
   Print `New shape after slicing: {zoomed.shape}` followed by `zoomed`.
5. **Step 5: Visualize.** Use `plt.imshow(zoomed.squeeze(), cmap="gray")`, show scale ticks, and call `plt.show()`.
6. **Step 6: Handle errors.** Catch any exception so the script prints `Error: <msg>` without crashing.

---

## 7. Guided Practice

**Practice 1 (Easiest — Load and inspect `animal.jpeg`):**
Write a script that loads `animal.jpeg` using `ft_load` and prints its shape and content.

Expected output:
```
The shape of image is: (768, 1024, 3)
[[[120 111 132] ...
```

<details><summary>Solution</summary>

```python
from load_image import ft_load

img = ft_load("animal.jpeg")
if img is not None:
    print(img)
```
</details>

**Practice 2 (Spatial slicing 400×400):**
Slice rows `100:500` and columns `450:850` from the image and print the cropped shape.

Expected output:
```python
(400, 400, 3)
```

<details><summary>Solution</summary>

```python
from load_image import ft_load

img = ft_load("animal.jpeg")
crop = img[100:500, 450:850]
print(crop.shape)
```
</details>

**Practice 3 (Extract 1 channel to shape `(400, 400, 1)`):**
Extract the first channel using slice notation `0:1` so the resulting shape is `(400, 400, 1)`.

Expected output:
```
New shape after slicing: (400, 400, 1)
```

<details><summary>Solution</summary>
```python
zoomed = crop[:, :, 0:1]
print(f"New shape after slicing: {zoomed.shape}")
print(zoomed)
```
</details>

**Practice 4 (Plotting with grayscale colormap and axes):**
Render `zoomed` with `matplotlib.pyplot` using `cmap="gray"`. Ensure the x and y axes with pixel tick marks are visible.

Expected output:
A GUI window appears displaying the zoomed raccoon face in black-and-white with coordinate axes on the left and bottom.

<details><summary>Solution</summary>

```python
import matplotlib.pyplot as plt

plt.imshow(zoomed.squeeze(), cmap="gray")
plt.show()
```
</details>

**Practice 5 (Hardest — the full, rule-compliant `zoom.py`):**
Write the complete `zoom.py` script with docstrings, PEP 8 formatting, and `main()` function with error handling.

Expected output when running `python zoom.py`:
```
$> python zoom.py
The shape of image is: (768, 1024, 3)
[[[120 111 132]
  [139 130 151]
  [155 146 167]
  ...
  [120 156  94]
  [119 154  90]
  [118 153  89]]]
New shape after slicing: (400, 400, 1) or (400, 400)
[[[167]
  [180]
  [194]
  ...
  [102]
  [104]
  [103]]]
```
*(A plot window opens showing the cropped raccoon image with x and y scales).*

<details><summary>Solution</summary>

```python
"""Program to zoom in on a region of an image and display it."""

import matplotlib.pyplot as plt
from load_image import ft_load


def main():
    """Load animal.jpeg, crop a 400x400 grayscale slice, and display it."""
    try:
        image = ft_load("animal.jpeg")
        if image is None:
            raise FileNotFoundError("Could not load image 'animal.jpeg'.")

        print(image)

        # Slice 400x400 area around the animal's face, keeping 1 channel
        zoomed = image[100:500, 450:850, 0:1]

        print(f"New shape after slicing: {zoomed.shape}")
        print(zoomed)

        # Display the zoomed image in grayscale with axes
        plt.imshow(zoomed.squeeze(), cmap="gray")
        plt.title("Zoom on Animal")
        plt.show()

    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
```
</details>

If your script prints the expected shapes and displays the image window cleanly, you're done!

---

## 8. Exercise-Specific Knowledge

- **Exact Expected Output Format:**
  ```
  The shape of image is: (768, 1024, 3)
  <image pixel data>
  New shape after slicing: (400, 400, 1)
  <sliced pixel data>
  ```
- **Area Coordinates:** The subject notes: *"Your array after slicing and the zoom area may be different."* Slicing `[100:500, 450:850]` nicely centers on the raccoon.
- **Grayscale Display:** Single-channel 2D arrays require `cmap="gray"`. If you leave the default, Matplotlib will use a false-color heatmap.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Inverted axes in slice | Writing `[450:850, 100:500]` | First slice is Y (vertical rows), second is X (horizontal columns) |
| Missing coordinate scales | Calling `plt.axis('off')` | Leave default axis display enabled |
| Image appears purple/yellow | Missing `cmap='gray'` in `plt.imshow()` | Specify `cmap='gray'` |
| Squeeze crash on 2D array | Calling `.squeeze()` on already 2D array | Check `zoomed.ndim == 3` before squeezing |

---

## 10. Debugging Guide

- **`UserWarning: Matplotlib is currently using agg...`**: If running on a headless VM without a display server (X11/Wayland), `plt.show()` may warn or fail. On Linux desktops, ensure an active desktop session.
- **Slice out of bounds**: Ensure `y2 <= image.shape[0]` and `x2 <= image.shape[1]`.

---

## 11. Cheat Sheet

```python
# Crop 400x400 with 1 channel:
zoomed = image[y_start:y_end, x_start:x_end, 0:1]

# Display with matplotlib in grayscale:
plt.imshow(zoomed.squeeze(), cmap="gray")
plt.show()
```

---

## 12. Knowledge Checklist

- [ ] I can crop a 3D NumPy array using multi-dimensional slicing `[y1:y2, x1:x2, c1:c2]`.
- [ ] I understand the difference between `arr[:, :, 0]` `(400, 400)` and `arr[:, :, 0:1]` `(400, 400, 1)`.
- [ ] I can display single-channel images using `matplotlib.pyplot.imshow` with `cmap="gray"`.
- [ ] I verified that the scale on the x and y axes is visible.
- [ ] My code conforms to PEP 8 and passes `flake8` without warnings.
