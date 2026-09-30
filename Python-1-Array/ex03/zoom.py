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
        print(img)
        print(f"New shape after slicing: {slc1.shape} or {slc2.shape}\n"
              f" {slc1}")
        plt.imshow(slc2, cmap="gray")
        plt.show()
    except Exception as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
