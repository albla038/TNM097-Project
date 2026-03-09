import math
from numpy.typing import NDArray
from matplotlib import pyplot as plt
from typing import Callable


def calculate_scale_factor(width: int, height: int, base_size=800):
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


def show_image_pair(img1: NDArray, img2: NDArray):
    plt.figure()
    plt.subplot(121)
    plt.imshow(img1)

    plt.subplot(122)
    plt.imshow(img2)
    plt.show()


def mm_to_pixels(mm: float, ppi=300):
    inches = mm / 25.4
    pixels = inches * ppi
    return round(pixels)


def create_coordinate_scales(
    img_width: float, img_height: float, page_width: float, page_height: float
) -> tuple[Callable[[float], float], Callable[[float], float]]:
    """
    Creates scaling functions to convert image pixel coordinates to PDF canvas coordinates.
    The image is scaled to fit the page while maintaining the aspect ratio, and centered on the page.
    """

    scale = min(page_width / img_width, page_height / img_height)

    print_width = scale * img_width
    print_height = scale * img_height

    x_offset = (page_width - print_width) / 2
    y_offset = (page_height - print_height) / 2

    def scale_x(px: float):
        return x_offset + (scale * px)

    def scale_y(py: float):
        # Invert y-axis for PDF coordinates
        return y_offset + (print_height - scale * py)

    return (scale_x, scale_y)


def hex_to_RGB(hex: str) -> list[int]:
    hex = hex.lstrip("#")
    return list(int(hex[i : i + 2], 16) for i in (0, 2, 4))
