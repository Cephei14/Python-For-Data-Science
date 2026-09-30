from PIL import Image
import numpy as np


def ft_load(path: str) -> np.ndarray | None:
    """Load an image file and return it as an RGB NumPy array."""
    try:
        with Image.open(path) as img:
            arr = np.array(img.convert("RGB"))
    except Exception as error:
        print(f"Error: could not load image ({error}).")
        return None
    print(f"The shape of image is: {arr.shape}")
    return arr
