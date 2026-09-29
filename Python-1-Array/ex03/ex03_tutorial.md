# Study Tutorial — Module 1, Exercise 03: zoom.py

## 1. Exercise Overview

**What it asks:** Load `animal.jpeg`, print information about it (pixel dimensions, number of channels, pixel content), then "zoom" into it — crop a sub-region using array slicing — and display the result. The example also reduces the image to a single channel (grayscale-like) as part of the zoom.

**Main concepts you'll learn:**
- Multi-dimensional array slicing (slicing along more than one axis at once)
- The relationship between image dimensions and array axes
- Displaying an array as an image (visualization)
- Reducing a 3-channel image to 1 channel via slicing

**Why this matters:** Cropping/zooming is 2D+ slicing in action — the exact same mechanic you used on rows in Exercise 01, just extended to more dimensions. This is your first real taste of multi-axis indexing, a skill that carries over directly to NumPy arrays and pandas DataFrames (`df.iloc[rows, cols]`) later.

**Skills after completing it:**
- Slice a 3D array along multiple axes simultaneously
- Reduce/select a single channel from a multi-channel image
- Display an array visually using Matplotlib
- Report shape information for both the original and the sliced array

---

## 2. Prerequisites

- Exercise 01's slicing concepts, and Exercise 02's image-loading (`ft_load`)
- Understanding of a 3D array shape `(height, width, channels)`

---

## 3. Tools and Libraries

| Tool | What it does | Notes |
|---|---|---|
| `array[a:b, c:d]` | Slices a 2D+ array along **two axes at once**, separated by a comma | Rows `a:b`, columns `c:d` |
| `array[a:b, c:d, e:f]` | Slices along three axes (rows, columns, channels) | Used to both crop *and* pick specific channel(s) |
| `matplotlib.pyplot.imshow(array)` | Displays an array as an image | From `matplotlib.pyplot` |
| `matplotlib.pyplot.show()` | Actually renders the displayed figure on screen | Needed after `imshow` |

Common pitfalls:
- Forgetting that slicing a 3D array needs commas to separate the axes: `array[100:500, 100:500]` slices rows and columns but leaves the channel axis untouched (which is fine if you want all channels); `array[100:500, 100:500, 0:1]` additionally restricts to just the first channel.
- Confusing "cropping" (selecting a rectangular region of rows/columns) with "reducing channels" (selecting a subset of the third axis) — the exercise's example output does *both* at once (400×400 spatial crop **and** 1 channel).
- Forgetting `plt.show()` — without it, `imshow()` alone won't actually display anything in many environments.

---

## 4. Concepts You Need to Learn

### 4.1 Multi-axis slicing
For a 1D list, you slice with `list[start:end]`. For a multi-dimensional array, you can slice each axis independently, separated by commas:
```python
import numpy as np
arr = np.arange(24).reshape(4, 6)   # 4 rows, 6 columns
print(arr[1:3, 2:5])
# rows 1-2, columns 2-4
```
The general pattern for a 3D image array is `arr[row_start:row_end, col_start:col_end, channel_start:channel_end]`.

### 4.2 Selecting a single channel
An RGB image has shape `(H, W, 3)` — channel 0 is Red, 1 is Green, 2 is Blue. To keep only one channel as a "grayscale-like" single-channel image:
```python
one_channel = arr[:, :, 0:1]   # shape (H, W, 1) -- Red channel only, kept as 3D
# or
one_channel_2d = arr[:, :, 0]  # shape (H, W)     -- Red channel only, flattened to 2D
```
Using `0:1` (a slice) keeps the array 3-dimensional with a channel axis of size 1; using a plain index `0` (not a slice) drops that axis entirely, giving a 2D array. Either can be valid depending on what shape you want to report — the subject's example output shows both possible shapes: `(400, 400, 1)` or `(400, 400)`.

### 4.3 Displaying an array as an image
```python
import matplotlib.pyplot as plt
plt.imshow(arr)
plt.show()
```
`imshow` interprets a `(H, W, 3)` array as RGB, and a `(H, W)` (2D) array as grayscale by default.

---

## 5. Syntax and Examples

### Cropping a region
```python
import numpy as np
arr = np.random.randint(0, 255, size=(768, 1024, 3))  # dummy image data
zoomed = arr[100:500, 200:600]
print(zoomed.shape)  # (400, 400, 3)
```

### Cropping and reducing to one channel
```python
zoomed_one_channel = arr[100:500, 200:600, 0:1]
print(zoomed_one_channel.shape)  # (400, 400, 1)
```

### Displaying with axis scale
```python
import matplotlib.pyplot as plt
plt.imshow(zoomed_one_channel.squeeze(), cmap="gray")
plt.show()
```
`.squeeze()` removes axes of size 1 (turning `(400, 400, 1)` into `(400, 400)`) which some display functions expect for grayscale rendering; `cmap="gray"` tells Matplotlib to render single-channel data as greyscale rather than a default colormap.

---

## 6. How to Think About the Exercise

1. Load the image with your `ft_load` function from Exercise 02 (the subject expects you to reuse `load_image.py`).
2. Print the original shape and pixel content, matching the required format.
3. Decide on a crop region — the example produces a `400×400` result from a `768×1024` source, so pick `start`/`end` indices for both the row and column axes that give you a 400-pixel span each (the exact region can differ from the subject's example, as the info box notes).
4. Apply the slice across both spatial axes at once — and, per the example, also reduce to a single channel.
5. Print the new shape and its pixel content.
6. Display the result with Matplotlib, including axis scales (tick marks along X and Y) — `imshow` does this by default; just make sure you don't accidentally turn off the axes.
7. Wrap the whole thing in error handling so a bad image path or invalid crop region doesn't crash the program.

---

## 7. Guided Practice

**Practice 1 (Easy):** Given a 2D NumPy array of shape `(10, 10)`, slice out the middle `4×4` region (rows 3–6, columns 3–6).
<details><summary>Solution</summary>

```python
import numpy as np
arr = np.arange(100).reshape(10, 10)
middle = arr[3:7, 3:7]
print(middle.shape)  # (4, 4)
```
</details>

**Practice 2 (Easy):** Given a 3D array of shape `(20, 20, 3)`, slice out just the Green channel (index 1), keeping it 2D.
<details><summary>Solution</summary>

```python
arr = np.random.randint(0, 255, size=(20, 20, 3))
green = arr[:, :, 1]
print(green.shape)  # (20, 20)
```
</details>

**Practice 3 (Medium):** Crop a `20×20×3` array down to its top-left `10×10` region, keeping all 3 channels.
<details><summary>Solution</summary>

```python
cropped = arr[0:10, 0:10]
print(cropped.shape)  # (10, 10, 3)
```
</details>

**Practice 4 (Close to the real exercise):** Combine cropping and single-channel selection: crop `arr` (shape `(768, 1024, 3)`) to `(400, 400)` starting at row 200, column 300, keeping only the Blue channel.
<details><summary>Solution</summary>

```python
zoomed = arr[200:600, 300:700, 2:3]
print(zoomed.shape)  # (400, 400, 1)
```
</details>

---

## 8. Exercise-Specific Knowledge

- Must print: pixel size on X and Y axes, number of channels, and pixel content — both before and after zooming.
- Output shape after zoom in the subject's example: `(400, 400, 1)` or `(400, 400)` — either is acceptable, and the exact crop region/values can differ from the example (explicitly noted in the subject).
- Must display the zoomed image with axis scales visible (the example figure shows tick marks 0–350+ on both axes).
- Errors must be handled without the program stopping abruptly.
- Reuses `load_image.py` from Exercise 02 — turn in both `load_image.py` and `zoom.py`.

---

## 9. Common Mistakes

| Mistake | Why it happens | Fix |
|---|---|---|
| Forgetting the comma between axis slices | Writing `arr[100:500][200:600]` (chained single-axis slicing) instead of `arr[100:500, 200:600]` | Use comma-separated slices for true multi-axis slicing — chaining can behave differently and is less efficient |
| Cropped region goes out of bounds | Picking start/end indices without checking the original image's actual dimensions first | Print/check the original shape before choosing crop coordinates |
| Displayed image looks like the wrong colors | Accidentally slicing away 2 of the 3 color channels without intending to, then displaying with a default (non-grayscale) colormap | If down to 1 channel, either restore 3 channels or explicitly set `cmap="gray"` in `imshow` |
| No axis scale visible on the displayed plot | Calling something that hides axes (e.g., `plt.axis("off")`) | Leave the default axes on, as the subject's example specifically shows tick marks |

---

## 10. Debugging Guide

- **`IndexError` or an unexpectedly small cropped shape** → your crop indices likely exceed the image's actual dimensions; print the original `.shape` first to sanity-check your slice bounds.
- **Displayed image is blank/black** → check whether you accidentally sliced a channel range that's entirely out of bounds (e.g., `[:, :, 5:6]` on a 3-channel image).
- **Colors look inverted or wrong** → check whether you're displaying a single-channel array without `cmap="gray"`, which can render oddly under default colormaps.
- Useful inspection: `print(zoomed.shape, zoomed.dtype)` to confirm both the shape and the data type (should typically be `uint8` for standard 0–255 image data) are what you expect.

---

## 11. Cheat Sheet

```python
arr[row_start:row_end, col_start:col_end]                 # crop spatially, all channels
arr[row_start:row_end, col_start:col_end, ch_start:ch_end]  # crop + select channel(s)
arr[:, :, 0]                                                # single channel, 2D
arr[:, :, 0:1]                                              # single channel, kept 3D

import matplotlib.pyplot as plt
plt.imshow(arr, cmap="gray")  # cmap only matters for 2D/1-channel arrays
plt.show()
```

---

## 12. Knowledge Checklist

- [ ] I can slice a multi-dimensional array along more than one axis at once using comma-separated slices.
- [ ] I can select a single channel from a multi-channel image array.
- [ ] I understand the difference between using a slice (`0:1`) vs. a plain index (`0`) on an axis.
- [ ] I can display an array as an image using Matplotlib, including axis scales.
- [ ] I can wrap image loading and cropping in error handling so bad input doesn't crash the program.
