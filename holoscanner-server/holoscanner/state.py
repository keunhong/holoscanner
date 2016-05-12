import threading
import asyncio
import numpy as np
from scipy.signal import argrelextrema
from scipy.ndimage.filters import gaussian_filter1d
from holoscanner import config
from holoscanner.proto import holoscanner_pb2 as pb
from holoscanner import base_logger

logger = base_logger.getChild(__name__)


class Mesh:
    def __init__(self, mesh_pb):
        self.nvertices = len(mesh_pb.vertices)
        self.nfaces = len(mesh_pb.faces)
        self.vertices = np.ndarray((self.nvertices, 3))
        for i, vert_pb in enumerate(mesh_pb.vertices):
            self.vertices[i, :] = (vert_pb.x, vert_pb.y, vert_pb.z)

    def __repr__(self):
        return 'Mesh(nvertices={}, nfaces={})'.format(
            self.nvertices, self.nfaces)


def find_planes(y_coords, nbins, sigma=None):
    if sigma:
        y_coords = gaussian_filter1d(y_coords, sigma)

    hist, bin_edges = np.histogram(
        y_coords,
        bins=nbins)

    candate_planes = bin_edges[argrelextrema(hist, np.greater, order=5)]
    floor_y, ceiling_y = candate_planes.min(), candate_planes.max()

    return floor_y, ceiling_y


def create_mesh_message(mesh_pb):
    msg = pb.Message()
    msg.type = pb.Message.MESH
    msg.device_id = 1
    msg.mesh.MergeFrom(mesh_pb)
    return msg


class GameState:
    mesh_pbs = []
    meshes = []
    lock = threading.RLock()
    message_queue = asyncio.Queue()

    floor = -10
    ceiling = 10

    def new_mesh(self, mesh_pb):
        with self.lock:
            self.mesh_pbs.append(mesh_pb)
            print(len(self.mesh_pbs))
            self.meshes.append(Mesh(mesh_pb))

        self.message_queue.put_nowait(create_mesh_message(mesh_pb))

        self.update_planes()

    def update_planes(self):
        y_coords = np.sort(np.vstack(
            [m.vertices for m in self.meshes])[:, 1])
        sigma = len(y_coords) / config.MESH_PLANE_FINDING_BINS
        self.floor, self.ceiling = find_planes(
            y_coords, config.MESH_PLANE_FINDING_BINS, sigma)
        logger.info('Planes updates: floor={}, ceiling={}'.format(
            self.floor, self.ceiling))


game_state = GameState()
