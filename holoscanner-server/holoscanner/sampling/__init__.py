import numpy as np
from holoscanner import base_logger

from .poisson_disk import sample_poisson_uniform

logger = base_logger.getChild(__name__)


def mask_bbox(mask):
    yinds, xinds = np.where(mask)
    return np.min(yinds), np.max(yinds), np.min(xinds), np.max(xinds)


def sample_poisson_mask(mask, r, k):
    ymin, ymax, xmin, xmax = mask_bbox(mask)
    height = ymax - ymin
    width = xmax - xmin
    points = np.array(sample_poisson_uniform(height, width, r, k,
                                             mask[ymin:ymax, xmin:xmax]))
    points[:, 0] += ymin
    points[:, 1] += xmin
    points = np.floor(points).astype(int)
    return points
