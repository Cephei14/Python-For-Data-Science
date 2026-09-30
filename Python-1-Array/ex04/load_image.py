from PIL import Image
import numpy as np


def ft_load(path: str) -> list:
    """Load an image file and return it as a NumPy array."""
    try:
        img = Image.open(path)
    except OSError as error:
        print(f"Error: could not load image ({error}).")
        return None
    arr = np.array(img)
    return arr
