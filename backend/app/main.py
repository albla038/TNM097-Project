import skimage as ski
from numpy.typing import NDArray
import numpy as np
from matplotlib import pyplot as plt
from segmentation import segment_img_by_colors
from morphology import clean_segments
from paint_map import generate_paint_map
from utils import calculateScaleFactor, showImagePair


def process_img(
    rgb_img: NDArray, num_of_colors=7, rescale=True, bilateral_filtering=False
):

    # Bilateral filtering
    if bilateral_filtering:
        rgb_img: NDArray = ski.restoration.denoise_bilateral(rgb_img, channel_axis=-1)
        print("Bilateral filtering done.")

    if rescale:
        # Rescale (with smart resulting dimensions)
        (rows, cols, ch) = rgb_img.shape
        factor = calculateScaleFactor(width=cols, height=rows, base_size=800)
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
    cleaned_labels = clean_segments(labels, min_radius=3)
    # TODO: Notify if one segment is "lost" to the morphology
    print("Label cleaning done.")

    # Convert back to RGB
    segmented_img = ski.color.lab2rgb(lab_cluster_centers[cleaned_labels])

    # TODO: Match KMeans clusters against user defined colors

    paint_map = generate_paint_map(cleaned_labels)
    return segmented_img


# Load image
img: NDArray = ski.data.coffee()
result = process_img(rgb_img=img)
