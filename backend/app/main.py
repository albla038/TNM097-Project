import skimage as ski
from numpy.typing import NDArray
import numpy as np
from matplotlib import pyplot as plt
from segmentation import segment_img_by_colors
from morphology import clean_segments
from contour_map import generate_contour_map, find_region_centers
from utils import calculate_scale_factor, mm_to_pixels, hex_to_RGB
from typing import Literal
from constants import A_FORMAT
from pdf import generate_pdf_buffer
from color_matching import map_colors_to_clusters


def process_img(
    rgb_img: NDArray,
    rgb_colors: NDArray,
    format_str: Literal["a3", "a4", "a5"] = "a4",
    min_mm_width=2,
    target_ppi=300,
    bilateral_filtering=False,
):
    # Convert user defined colors to CIELAB in [K x 3] shape
    lab_colors = ski.color.rgb2lab(rgb_colors.reshape(1, -1, 3)).reshape(-1, 3)

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
    factor = calculate_scale_factor(width=cols, height=rows, base_size=(8.27 * ppi))
    rgb_img: NDArray = ski.transform.rescale(
        image=rgb_img, scale=factor, anti_aliasing=(factor < 1), channel_axis=2
    )

    # Convert to CIELAB
    lab_img: NDArray = ski.color.rgb2lab(rgb_img)

    # Segment image based on K colors
    (segmented_lab_img, labels, lab_cluster_centers) = segment_img_by_colors(
        lab_img, num_of_colors=len(lab_colors)
    )
    print("K-Means segmentation done.")

    # Apply morphological operations to clean up image
    cleaned_labels = clean_segments(
        labels,
        min_px_width=(mm_to_pixels(min_mm_width, ppi) // format["scale_factor"]),
    )
    if np.unique(labels).size != np.unique(cleaned_labels).size:
        print(
            "Warning: Number of segments after cleaning is different from before cleaning. Consider adjusting the min_mm_width parameter."
        )
    print("Label cleaning done.")

    scaled_labels: NDArray = ski.transform.rescale(
        image=cleaned_labels,
        scale=format["scale_factor"] * (target_ppi / ppi),
        order=0,
    ).astype(np.uint8)

    # Match K-Means clusters against user defined colors
    ordered_lab_colors = map_colors_to_clusters(
        user_colors=lab_colors, cluster_colors=lab_cluster_centers
    )

    # Convert back to RGB
    segmented_img_cluster_colors = ski.color.lab2rgb(lab_cluster_centers[scaled_labels])
    segmented_img_user_colors = ski.color.lab2rgb(ordered_lab_colors[scaled_labels])

    (contours, contour_map) = generate_contour_map(
        labels=scaled_labels, line_gray_level=128, target_ppi=target_ppi
    )
    print("Paint map generation done.")

    # Find region center positions with label
    region_details = find_region_centers(scaled_labels)

    # Generate PDF
    pdf_buffer = generate_pdf_buffer(
        img_data=contour_map,
        region_details=region_details,
        page_size=format["page_size"],
    )

    return segmented_img_cluster_colors, segmented_img_user_colors


# Load image
img: NDArray = ski.data.coffee()
result = process_img(rgb_img=img)
