import numpy as np
import skimage as ski


def generate_paint_map(labels):
    # Create a black background
    black_bg = np.zeros(labels.shape)

    # Mark gray 1px boundaries between segments
    paint_map = ski.segmentation.mark_boundaries(
        image=black_bg,
        label_img=labels,
        color=(0.1, 0.1, 0.1),
        mode="subpixel",
    )

    paint_map_rgb = ski.util.img_as_ubyte(paint_map)

    # Set the black background to white (255)
    paint_map_rgb[paint_map_rgb == 0] = 255

    return paint_map_rgb
