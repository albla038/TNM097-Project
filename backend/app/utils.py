import math
from numpy.typing import NDArray
from matplotlib import pyplot as plt


def calculateScaleFactor(width: int, height: int, base_size=800):
    """
    Calculate the scale factor to resize the image to an A-standard (A3, A4 print sizes etc.) size while maintaining the aspect ratio.
    """

    # Define the target bounding box for A-standard
    short_side = base_size
    long_side = base_size * math.sqrt(2)

    if width >= height:
        # Landscape layout
        scale_x = short_side / height
        scale_y = long_side / width
    else:
        # Portrait layout
        scale_x = long_side / height
        scale_y = short_side / width

    return min(scale_x, scale_y)


def showImagePair(img1: NDArray, img2: NDArray):
    plt.figure()
    plt.subplot(121)
    plt.imshow(img1)

    plt.subplot(122)
    plt.imshow(img2)
    plt.show()
