import math, os
import numpy as np
from PIL import Image, ImageDraw
from scipy.signal import argrelextrema
from scipy.ndimage.filters import gaussian_filter1d
from scipy.misc import imsave, imresize, toimage
from scipy.stats import binned_statistic_2d
from skimage import morphology
from holoscanner import config
from holoscanner import base_logger


logger = base_logger.getChild(__name__)


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
        imsave(os.path.join(config.IMAGE_SAVE_DIR, 'test.png'), im)
        im = morphology.binary_closing(im, morphology.square(40))
        imsave(os.path.join(config.IMAGE_SAVE_DIR, 'test2.png'), im)
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


def compute_2d_normals(vertices, per_vertex_normals, floor, ceiling,
                       global_hull_mask):
    filt = (vertices[:, 1] > floor + 0.2) & (vertices[:, 1] < ceiling - 0.2)
    wall_vertices = vertices[filt, :]
    wall_vertex_normals = per_vertex_normals[filt, :]

    hist_bins = (int(global_hull_mask.shape[0] / 2),
                 int(global_hull_mask.shape[1] / 2))
    print(hist_bins)

    hist, binx, binz = np.histogram2d(wall_vertices[:, 0], wall_vertices[:, 2],
                                bins=hist_bins)
    hist[hist < np.percentile(hist, 94)] = 0
    normal_mean_x, _, _, _ = binned_statistic_2d(wall_vertices[:, 0],
                                                 wall_vertices[:, 2],
                                                 values=wall_vertex_normals[:,
                                                        0],
                                                 statistic='mean',
                                                 bins=hist_bins)
    normal_mean_z, _, _, _ = binned_statistic_2d(wall_vertices[:, 0],
                                                 wall_vertices[:, 2],
                                                 values=wall_vertex_normals[:,
                                                        2],
                                                 statistic='mean',
                                                 bins=hist_bins)
    normal_mean_x[hist == 0] = np.nan
    normal_mean_z[hist == 0] = np.nan

    return normal_mean_x, normal_mean_z, binx, binz


def _coord_neighbors(y, x, visited):
    neighbors = [(y + dy, x + dx) for dx in [-1, 0, 1] for dy in [-1, 0, 1]
                 if (0 <= x + dx < visited.shape[1] and
                     0 <= y + dy < visited.shape[0] and
                     not visited[y + dy, x + dx])]
    return neighbors


def bfs_sdf(normal_mean_x, normal_mean_z):
    visited = ~np.isnan(normal_mean_z) & ~np.isnan(normal_mean_x)
    distance_map = np.zeros(visited.shape)
    start_y, start_x = np.where(visited)

    queue = []
    start_coords = [coord for coord in zip(start_y, start_x)]
    for y, x in start_coords:
        visited[y, x] = True
        for ny, nx in _coord_neighbors(y, x, visited):
            normal = [normal_mean_x[y, x],
                      normal_mean_z[y, x]]
            direction = np.subtract((y, x), (ny, nx))
            direction = direction / np.sum(direction ** 2)
            dot = (direction.dot(normal))
            if abs(dot) >= 0.5:
                distance_map[ny, nx] = dot
                visited[ny, nx] = True
                queue.append((ny, nx))

    save_im(os.path.join(config.IMAGE_SAVE_DIR, 'tst.png'), distance_map)

    while len(queue) > 0:
        y, x = queue.pop(0)
        curdist = distance_map[y, x]
        for ny, nx in _coord_neighbors(y, x, visited):
            distance_map[
                ny, nx] = curdist - 0.1 if curdist < 0 else curdist + 0.1
            visited[ny, nx] = True
            queue.append((ny, nx))

    return distance_map


def save_im(dir, im):
    toimage(im, cmin=im.min(), cmax=im.max()).save(dir)
