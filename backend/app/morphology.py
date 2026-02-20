import skimage as ski
import numpy as np
from numpy.typing import NDArray


def clean_segments(labels: NDArray, min_radius=3) -> NDArray:
    """
    Cleans up the segmented image by applying morphological operations to remove unusable pixel segments.

    Args:
        labels: 2D matrix of cluster labels for each pixel (rows x cols)

        min_radius: Minimum radius for morphological opening. This parameter controls the size of the structuring element used in the opening operation.

    Returns:
        final_labels: 2D matrix of cleaned cluster labels for each pixel (rows x cols). The labels are zero-indexed and may have fewer unique values than the input labels due to the removal of small segments.

    """

    # Shift all labels one step (K-Means returns zero-indexed labels)
    labels = labels + 1

    # Generate list of unique label/segment numbers
    segments_list = np.unique(labels)

    # Initialize a blank canvas to be filled with valid segments
    cleaned_labels_map = np.zeros_like(labels)
    # TODO: Optionally sort segment order based on some criteria (segment area, color lightness, etc.)

    # Loop over labels
    for s in segments_list:
        # Isolate segment from label image
        segment = labels == s

        # Perform morphological opening to remove unusable segments
        cleaned_segment = ski.morphology.isotropic_opening(segment, radius=min_radius)

        # Add cleaned segment to the cleaned labels map
        cleaned_labels_map[cleaned_segment] = s

    # Expand the cleaned segments to fill in any gaps created by the morphological operations
    final_labels = ski.segmentation.expand_labels(cleaned_labels_map, distance=5000)

    # Shift labels back to zero-indexed
    return final_labels - 1
