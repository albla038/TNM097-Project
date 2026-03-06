import numpy as np
import skimage as ski
from numpy.typing import NDArray


def generate_contour_map(labels: NDArray, line_gray_level=128, target_ppi=300):
    contours = ski.segmentation.find_boundaries(
        label_img=labels, connectivity=1, mode="inner", background=-1
    )

    # Initialize RGBA image with correct img dims (rows x cols x 4)
    contour_map = np.zeros((*labels.shape, 4), dtype=np.uint8)
    # Initialize map with transparent pixels
    contour_map[:] = [255, 255, 255, 0]

    contour_map[contours] = [
        line_gray_level,
        line_gray_level,
        line_gray_level,
        255,
    ]

    return (contours, contour_map)
