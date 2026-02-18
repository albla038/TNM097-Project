import skimage as ski
from numpy.typing import NDArray
from matplotlib import pyplot as plt
from segment import segment


def process_img(rgb_img: NDArray, bilateral_filtering=False):

    # Bilateral filtering?

    if bilateral_filtering:
        rgb_img = ski.restoration.denoise_bilateral(rgb_img, channel_axis=-1)

    # TODO: downsample (with smart resulting dimensions)

    # Convert to CIELAB
    lab_img: NDArray = ski.color.rgb2lab(rgb_img)

    # Segment image based on K colors
    (segmented_lab_img, labels, lab_cluster_centers) = segment(lab_img, 5)

    # Convert back to RGB
    segmented_img = ski.color.lab2rgb(segmented_lab_img)

    # TODO: Apply morphological operations to clean up image

    # TODO: Match KMeans clusters against user defined colors

    return segmented_img


# Load image
img: NDArray = ski.data.coffee()
result = process_img(rgb_img=img)
