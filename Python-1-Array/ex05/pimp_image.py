import matplotlib.pyplot as plt


def _show(res):
    """Display an image array."""
    plt.figure()
    plt.imshow(res)
    plt.show()


def ft_invert(array):
    """Inverts the color of the image received."""
    res = 255 - array
    print(f"The shape of image is: {res.shape}\n {res}")
    _show(res)
    return res


def ft_red(array):
    """Removes the Green and Blue channels by multiplication"""
    res = array.copy()
    res[:, :, 1] = res[:, :, 1] * 0
    res[:, :, 2] = res[:, :, 2] * 0
    _show(res)
    return res


def ft_green(array):
    """Removes the Red and Blue channels by substraction"""
    res = array.copy()
    res[:, :, 0] = res[:, :, 0] - res[:, :, 0]
    res[:, :, 2] = res[:, :, 2] - res[:, :, 2]
    _show(res)
    return res


def ft_blue(array):
    """Removes the Green and Red channels by assignment"""
    res = array.copy()
    res[:, :, 0] = 0
    res[:, :, 1] = 0
    _show(res)
    return res


def ft_grey(array):
    """Makes all channels equal to green, which gives grey"""
    res = array.copy()
    res[:, :, 0] = res[:, :, 1]
    res[:, :, 2] = res[:, :, 1]
    _show(res)
    return res
