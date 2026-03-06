from numpy.typing import NDArray
from sklearn.metrics import pairwise_distances
from scipy.optimize import linear_sum_assignment
import skimage as ski
import numpy as np


def map_colors_to_clusters(user_colors: NDArray, cluster_colors: NDArray) -> NDArray:
    """
    Order user defined colors according to cluster colors from K-Means segmentation.
    Expects CIELab colors in [K x 3] format
    """

    # Match each user color against a cluster color and, for each pair,
    # calculate the "distance" in color according to custom metric
    distance_matrix = pairwise_distances(
        X=user_colors, Y=cluster_colors, metric=ski.color.deltaE_ciede2000, kL=0.5
    )

    # Find the optimal color pairs
    (row_ind, col_ind) = linear_sum_assignment(distance_matrix)

    # Define placeholder with all colors set to [0, 0, 0]
    ordered_user_colors = np.zeros_like(user_colors)

    # Rearrange colors in labeling order according to match
    ordered_user_colors[col_ind] = user_colors[row_ind]

    return ordered_user_colors
