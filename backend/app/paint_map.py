import numpy as np
import skimage as ski
from numpy.typing import NDArray


def generate_paint_map(labels: NDArray, line_gray_level=128):
    boundaries = ski.segmentation.find_boundaries(
        label_img=labels, connectivity=1, mode="inner", background=-1
    )

    # Initialize RGBA image with correct img dims (rows x cols x 4)
    paint_map = np.zeros((*labels.shape, 4), dtype=np.uint8)
    # Initialize map with transparent pixels
    paint_map[:] = [255, 255, 255, 0]

    paint_map[boundaries] = [
        line_gray_level,
        line_gray_level,
        line_gray_level,
        255,
    ]

    return (boundaries, paint_map)
