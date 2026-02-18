import skimage as ski
from numpy.typing import NDArray
from sklearn.cluster import KMeans


def segment(
    lab_img: NDArray, num_of_colors=10, max_kmeans_iter=300
) -> tuple[NDArray, NDArray, NDArray]:
    """
    Segments an image using K-Means clustering, based on K number of colors.
    Args:
        lab_img: Image in CIELAB color space (3D matrix, [rows x cols x channels])

        num_of_colors: Number of colors to segment the image into (K in K-Means)

        max_kmeans_iter: Maximum number of iterations for K-Means to converge

    Returns:
        segmented_data: Image with each pixel replaced by its cluster center (3D matrix)

        labels: 2D matrix of cluster labels for each pixel (rows x cols)

        lab_cluster_centers: 2D matrix of cluster centers in CIELAB color space (num_of_colors x channels). These are the K optimal colors that represent the image after segmentation.
    """

    # Get original dimensions
    (rows, cols, ch) = lab_img.shape

    # Flatten image matrix into a list of LAB triplets (3D matrix -> 2D matrix)
    # Ex: [400 x 600 x 3] to [240000 x 3] = [400 x 600, 3]
    img_data = lab_img.reshape(-1, 3)

    # Fit K-Means clusters
    kmeans = KMeans(n_clusters=num_of_colors, max_iter=max_kmeans_iter)
    kmeans.fit(img_data)

    # Reshape labels to 3D matrix
    labels = kmeans.labels_.reshape(rows, cols)

    # Replace all pixels in original CIELAB image
    lab_cluster_centers = kmeans.cluster_centers_
    segmented_data = lab_cluster_centers[labels]

    return (segmented_data, labels, lab_cluster_centers)
