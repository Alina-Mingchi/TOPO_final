import numpy as np
import scipy as sp


def bicubic(source_img, scaling_factor):
    source_img_size1 = source_img.shape[0]
    source_img_size2 = source_img.shape[1]
    x = np.array(list(range(0, int(source_img_size1)))).astype(float)
    y = np.array(list(range(0, int(source_img_size2)))).astype(float)
    int_img = sp.interpolate.RectBivariateSpline(x, y, source_img)
    x_up = np.array(list(range(0, source_img_size1 * scaling_factor))).astype(float) / scaling_factor - 0.5
    y_up = np.array(list(range(0, source_img_size2 * scaling_factor))).astype(float) / scaling_factor - 0.5

    x_grid, y_grid = np.meshgrid(x_up, y_up, indexing="ij")
    return int_img.ev(x_grid, y_grid)