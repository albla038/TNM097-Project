import numpy as np
import skimage as ski
from numpy.typing import NDArray
from utils import mm_to_pixels
from definitions import RegionDetail
from scipy.ndimage import distance_transform_edt


def generate_contour_map(labels: NDArray, line_gray_level=128, target_ppi=300):
    contours = ski.segmentation.find_boundaries(
        label_img=labels, connectivity=1, mode="inner", background=-1
    )

    line_thickness = mm_to_pixels(0.1, target_ppi)

    # Thicken up lines to 0.1 mm
    contours = ski.morphology.isotropic_dilation(contours, line_thickness / 2)

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


def find_region_centers(labels: NDArray, color_lookup_table: dict[int, int]):
    # Shift all labels one step (K-Means returns zero-indexed labels)
    labels = labels + 1

    region_details: list[RegionDetail] = []

    # Loop over unique segments
    for s in np.unique(labels):
        # Isolate segment from label image
        segment = labels == s

        # Find connected components
        region_labels = ski.measure.label(segment)

        # Loop over each region in segment
        for region in ski.measure.regionprops(region_labels):

            padded_region = np.pad(
                region.image, pad_width=1, mode="constant", constant_values=False
            )

            # Find distance from each pixel in region to nearest edge pixel (distance transform)
            dist_map = distance_transform_edt(padded_region)

            # Find coords of pixel with max distance to edge
            (local_y, local_x) = np.unravel_index(np.argmax(dist_map), dist_map.shape)

            # Account for padding
            local_x -= 1
            local_y -= 1

            (min_y, min_x, _, _) = region.bbox
            global_x = min_x + local_x
            global_y = min_y + local_y

            # Find max size that can fit in region (for label size)
            max_size_px = np.floor(2 * np.max(dist_map))

            region_details.append(
                {
                    "label": color_lookup_table[s - 1] + 1,
                    "row": int(np.rint(global_y)),
                    "col": int(np.rint(global_x)),
                    "max_size_px": int(max_size_px),
                }
            )

    return region_details
