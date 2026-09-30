import numpy as np
import matplotlib.pyplot as plt
from load_image import ft_load


def main():
    """Main function"""
    try:
        img = ft_load("animal.jpeg")
        if img is None:
            return
        slc1 = img[78:-290, 484:-140, 0:1]
        slc2 = img[78:-290, 484:-140, 0]
        if slc2.size == 0:
            raise ValueError("image too small for the zoom area")
        print(f"The shape of image is: {slc1.shape} or {slc2.shape}")
        print(slc1)
        rows, cols = slc2.shape
        rot = np.zeros((cols, rows), dtype=slc2.dtype)
        rot = np.array([[row[j] for row in slc2] for j in range(cols)])
        print(f"New shape after Transpose: {rot.shape}\n {rot}")
        plt.figure()
        plt.imshow(rot, cmap="gray")
        plt.show()
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
