import skimage as ski
import numpy as np
from numpy.typing import NDArray
from matplotlib import pyplot as plt


def clean_segments(labels: NDArray, min_radius=3) -> NDArray:
    S_E = ski.morphology.disk(min_radius)

    opened_labels = ski.morphology.opening(labels, footprint=S_E)
    cleaned_lables = ski.morphology.closing(opened_labels, footprint=S_E)

    return cleaned_lables
