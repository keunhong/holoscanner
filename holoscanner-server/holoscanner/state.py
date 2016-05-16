import threading
import random
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

    candate_planes = bin_edges[argrelextrema(hist, np.greater, order=2)]
    floor_y, ceiling_y = candate_planes.min(), candate_planes.max()

    return floor_y, ceiling_y


class GameState:
    mesh_pbs = []
    meshes = []
    lock = threading.RLock()
    message_queue = asyncio.Queue()

    floor = -10
    ceiling = 10
    targets = []

    def new_mesh(self, mesh_pb):
        with self.lock:
            self.mesh_pbs.append(mesh_pb)
            print(len(self.mesh_pbs))
            self.meshes.append(Mesh(mesh_pb))

        self.message_queue.put_nowait(self.create_mesh_message(mesh_pb))

        self.update_targets(20)
        self.update_planes()

        self.message_queue.put_nowait(self.create_game_state_message())

    def update_planes(self):
        y_coords = np.sort(np.vstack(
            [m.vertices for m in self.meshes])[:, 1])
        sigma = len(y_coords) / config.MESH_PLANE_FINDING_BINS
        self.floor, self.ceiling = find_planes(
            y_coords, config.MESH_PLANE_FINDING_BINS, sigma / 5)
        logger.info('Planes updates: floor={}, ceiling={}'.format(
            self.floor, self.ceiling))

    def update_targets(self, num_targets):
        self.targets.clear()
        coords = np.sort(np.vstack([m.vertices for m in self.meshes]))
        for i in range(num_targets):
            x = random.uniform(coords[:, 0].min() - 1, coords[:, 0].max() + 1)
            z = random.uniform(coords[:, 2].min() - 1, coords[:, 2].max() + 1)
            y = (self.floor + 0.1
                 if random.uniform(0, 1) > 0.5
                 else self.ceiling - 0.1)
            self.targets.append([x, y, z])

    def create_game_state_message(self):
        msg = pb.Message()
        msg.type = pb.Message.GAME_STATE
        msg.device_id = config.SERVER_DEVICE_ID
        msg.game_state.floor_y = self.floor
        msg.game_state.ceiling_y = self.ceiling
        for target in self.targets:
            vec = pb.Vec3D()
            vec.x = target[0]
            vec.y = target[1]
            vec.z = target[2]
            msg.game_state.targets.extend([vec])
        return msg

    def create_mesh_message(self, mesh_pb):
        msg = pb.Message()
        msg.type = pb.Message.MESH
        msg.device_id = config.SERVER_DEVICE_ID
        msg.mesh.MergeFrom(mesh_pb)
        return msg


game_state = GameState()
