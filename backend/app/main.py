import skimage as ski
from numpy.typing import NDArray
import numpy as np
from matplotlib import pyplot as plt
from segmentation import segment_img_by_colors
from morphology import clean_segments
from paint_map import generate_paint_map
from utils import calculate_scale_factor, show_image_pair, mm_to_pixels
from typing import Literal
from constants import A_FORMAT


def process_img(
    rgb_img: NDArray,
    num_of_colors=7,
    format_str: Literal["a3", "a4", "a5"] = "a4",
    min_mm_width=2,
    target_ppi=300,
    bilateral_filtering=False,
):
    format = A_FORMAT[format_str]

    # Bilateral filtering
    if bilateral_filtering:
        rgb_img: NDArray = ski.restoration.denoise_bilateral(rgb_img, channel_axis=-1)
        print("Bilateral filtering done.")

    # Rescale image to make K-Means computation more efficient
    (rows, cols, ch) = rgb_img.shape
    # A4 is 210 x 297 mm = 8.27 x 11.69 inches
    # Base size 827 is therefore the width of an portrait A4 at 100 PPI
    ppi = 100
    factor = calculate_scale_factor(width=cols, height=rows, base_size=827)
    rgb_img: NDArray = ski.transform.rescale(
        image=rgb_img, scale=factor, anti_aliasing=(factor < 1), channel_axis=2
    )

    # Convert to CIELAB
    lab_img: NDArray = ski.color.rgb2lab(rgb_img)

    # Segment image based on K colors
    (segmented_lab_img, labels, lab_cluster_centers) = segment_img_by_colors(
        lab_img, num_of_colors=num_of_colors
    )
    print("K-Means segmentation done.")

    # Apply morphological operations to clean up image
    cleaned_labels = clean_segments(
        labels,
        min_px_width=(mm_to_pixels(min_mm_width, ppi) // format["scale_factor"]),
    )
    # TODO: Notify if one segment is "lost" to the morphology
    print("Label cleaning done.")

    scaled_labels: NDArray = ski.transform.rescale(
        image=cleaned_labels,
        scale=format["scale_factor"] * (target_ppi / ppi),
        order=0,
    ).astype(np.uint8)

    # Convert back to RGB
    segmented_img = ski.color.lab2rgb(lab_cluster_centers[scaled_labels])

    # TODO: Match KMeans clusters against user defined colors

    (boundaries, paint_map) = generate_paint_map(
        labels=scaled_labels, line_gray_level=128
    )
    return segmented_img


# Load image
img: NDArray = ski.data.coffee()
result = process_img(rgb_img=img)
