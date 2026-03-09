import skimage as ski
from numpy.typing import NDArray
from sklearn.cluster import KMeans
from utils import calculate_scale_factor


def segment_img_by_colors(
    lab_img: NDArray,
    num_of_colors=10,
    kmeans_ppi=100,
    target_ppi=300,
    max_kmeans_iter=300,
) -> tuple[NDArray, NDArray]:
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
    
    # Rescale image to make K-Means computation more efficient
    # A4 is 210 x 297 mm = 8.27 x 11.69 inches
    # Base size 827 is therefore the width of an portrait A4 at 100 PPI
    kmeans_scale_factor = calculate_scale_factor(
        width=cols, height=rows, base_size=(8.27 * kmeans_ppi)
    )
    kmeans_lab_img: NDArray = ski.transform.rescale(
        image=lab_img,
        scale=kmeans_scale_factor,
        anti_aliasing=(kmeans_scale_factor < 1),
        channel_axis=2,
    )

    # Flatten image matrix into a list of LAB triplets (3D matrix -> 2D matrix)
    # Ex: [400 x 600 x 3] to [240000 x 3] = [400 x 600, 3]
    img_data = kmeans_lab_img.reshape(-1, 3)

    # Fit K-Means clusters
    kmeans = KMeans(n_clusters=num_of_colors, max_iter=max_kmeans_iter, random_state=1)
    kmeans.fit(img_data)

    # Rescale original image to target PPI
    target_scale_factor = calculate_scale_factor(
        width=cols, height=rows, base_size=(8.27 * target_ppi)
    )
    scaled_lab_img: NDArray = ski.transform.rescale(
        image=lab_img,
        scale=target_scale_factor,
        anti_aliasing=(target_scale_factor < 1),
        channel_axis=2,
    )
    (scaled_rows, scaled_cols, scaled_ch) = scaled_lab_img.shape

    # Segment image by replacing each pixel with its nearest cluster center
    labels = kmeans.predict(scaled_lab_img.reshape(-1, 3))

    # Reshape labels to 3D matrix
    labels_img = labels.reshape(scaled_rows, scaled_cols)

    return (labels_img, kmeans.cluster_centers_)
