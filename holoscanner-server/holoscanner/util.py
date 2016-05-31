import math
import numpy as np
from PIL import Image, ImageDraw
from scipy.signal import argrelextrema
from scipy.ndimage.filters import gaussian_filter1d
from scipy.misc import imsave, imresize
from skimage import morphology
from holoscanner import config


def quat_to_mat(x, y, z, w):
    n = w * w + x * x + y * y + z * z
    s = 0 if n == 0 else (2 / n)
    wx = s * w * x
    wy = s * w * y
    wz = s * w * z
    xx = s * x * x
    xy = s * x * y
    xz = s * x * z
    yy = s * y * y
    yz = s * y * z
    zz = s * z * z
    return np.array([
        [1 - (yy + zz), xy - wz, xz + wy],
        [xy + wz, 1 - (xx + zz), yz - wx],
        [xz - wy, yz + wx, 1 - (xx + yy)]])


def compute_hull_mask(faces, vertices, scale=config.HULL_SCALE,
                      remove_holes=True, closing=False):
    transformed = vertices.copy()
    transformed[:, 0] -= vertices[:, 0].min()
    transformed[:, 2] -= vertices[:, 2].min()
    transformed *= scale
    xmin = vertices[:, 0].min()
    zmin = vertices[:, 2].min()
    xmax = vertices[:, 0].max()
    zmax = vertices[:, 2].max()
    width = int(math.ceil(vertices[:, 0].max() -
                          vertices[:, 0].min()) * scale) + 1
    height = int(math.ceil(vertices[:, 2].max() -
                           vertices[:, 2].min()) * scale) + 1

    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    for face in faces:
        p = [(int(transformed[i, 0]), int(transformed[i, 2])) for i in face]
        draw.polygon(p, fill='#fff')

    im = np.array(im) == 255
    if closing:
        imsave('/home/kpar/www/test.png', im)
        im = morphology.binary_closing(im, morphology.square(40))
        imsave('/home/kpar/www/test2.png', im)
    if remove_holes and len(np.unique(im) >= 2):
        im = morphology.remove_small_holes(im, min_size=scale ** 2)
    return im.T, xmin, zmin, xmax, zmax


def find_floor_and_ceiling(y_coords, nbins, sigma=None):
    if sigma:
        y_coords = gaussian_filter1d(y_coords, sigma)

    hist, bin_edges = np.histogram(
        y_coords,
        bins=nbins)

    candate_planes = bin_edges[argrelextrema(hist, np.greater, order=2)]
    floor_y, ceiling_y = candate_planes.min(), candate_planes.max()

    return floor_y, ceiling_y
