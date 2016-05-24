import os
import threading
import random
import asyncio
import numpy as np
from scipy.signal import argrelextrema
from scipy.ndimage.filters import gaussian_filter1d
from PIL import Image, ImageDraw
from skimage import measure
from skimage import morphology
from scipy.spatial import Delaunay
from numpy import linalg

from holoscanner import config
from holoscanner.proto import holoscanner_pb2 as pb
from holoscanner import base_logger

logger = base_logger.getChild(__name__)


def find_planes(y_coords, nbins, sigma=None):
    if sigma:
        y_coords = gaussian_filter1d(y_coords, sigma)

    hist, bin_edges = np.histogram(
        y_coords,
        bins=nbins)

    candate_planes = bin_edges[argrelextrema(hist, np.greater, order=2)]
    floor_y, ceiling_y = candate_planes.min(), candate_planes.max()

    return floor_y, ceiling_y


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


def compute_hull_mask(points, vertices, scale=100, alpha=0.3, remove_holes=True):
    transformed = points.copy()
    transformed[:, 0] -= points[:, 0].min()
    transformed[:, 1] -= points[:, 1].min()
    tri = Delaunay(transformed)
    keep = []
    offsetx = vertices[:, 0].min()
    offsetz = vertices[:, 2].min()
    # Points are in PIL convention (x, y).
    width = int(round(vertices[:, 0].max() - vertices[:, 0].min()) * scale)
    height = int(round(vertices[:, 2].max() - vertices[:, 2].min()) * scale)
    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    for simplex in tri.simplices:
        p = [(int(transformed[i, 0]*scale), int(transformed[i, 1]*scale)) for i in simplex]
        pm = [points[i, :] for i in simplex]
        if (linalg.norm(pm[0] - pm[1]) < alpha and
            linalg.norm(pm[1] - pm[2]) < alpha and
            linalg.norm(pm[0] - pm[2]) < alpha):
            draw.polygon(p, fill='#fff')
    im = np.array(im) == 255
    if remove_holes:
        im = morphology.remove_small_holes(im, min_size=scale**2)
    # Return to numpy convention (y, x).
    return im.T, offsetx, offsetz


class Mesh:
    def __init__(self, mesh_pb, client):
        self.nvertices = len(mesh_pb.vertices)
        self.nfaces = int(len(mesh_pb.triangles) / 3)
        self.vertices = np.ndarray((self.nvertices, 3), dtype=float)
        self.client = client
        self.mesh_id = mesh_pb.mesh_id
        self.faces = np.array(mesh_pb.triangles, dtype=int)
        for i, vert_pb in enumerate(mesh_pb.vertices):
            self.vertices[i, :] = (vert_pb.x, vert_pb.y, vert_pb.z)

        if mesh_pb.cam_rotation:
            rotation_mat = quat_to_mat(mesh_pb.cam_rotation.x,
                                       mesh_pb.cam_rotation.y,
                                       mesh_pb.cam_rotation.z,
                                       mesh_pb.cam_rotation.w)
            self.vertices = rotation_mat.dot(self.vertices.T).T
            self.vertices[:, 0] += mesh_pb.cam_position.x
            self.vertices[:, 1] += mesh_pb.cam_position.y
            self.vertices[:, 2] += mesh_pb.cam_position.z

        self.normals = self.compute_normals()

    def to_proto(self):
        mesh_pb = pb.Mesh()
        for i in range(self.nvertices):
            v = pb.Vec3D()
            v.x = self.vertices[i, 0]
            v.y = self.vertices[i, 1]
            v.z = self.vertices[i, 2]
            mesh_pb.vertices.extend([v])
        mesh_pb.triangles.extend(self.faces.tolist())
        return mesh_pb

    def compute_normals(self):
        normals = np.zeros((self.nfaces, 3))
        for i in range(self.nfaces):
            v1 = self.vertices[self.faces[i * 3 + 0]]
            v2 = self.vertices[self.faces[i * 3 + 1]]
            v3 = self.vertices[self.faces[i * 3 + 2]]
            normals[i] = np.cross(v1 - v2, v3 - v2)
        return normals

    def __repr__(self):
        return 'Mesh(nvertices={}, nfaces={})'.format(
            self.nvertices, self.nfaces)


class Client:
    def __init__(self, ip, protocol):
        self.ip = ip
        self.score = 0
        self.protocol = protocol

    def send_message(self, message):
        self.protocol.send_message(message)


class GameState:
    clients = {}

    lock = threading.RLock()
    meshes = []
    listeners = []

    floor = -10
    ceiling = 10
    target_counter = 0
    target_pbs = {}

    def new_hololens_client(self, ip, protocol):
        if ip not in self.clients:
            logger.info('Adding client with IP {}'.format(ip))
            self.clients[ip] = Client(ip, protocol)
        return self.clients[ip]

    def new_websocket_client(self, queue):
        self.listeners.append(queue)

    def send_to_websocket_clients(self, message):
        for queue in self.listeners:
            queue.put_nowait(message)

    def send_to_hololens_clients(self, message):
        for client in self.clients.values():
            client.send_message(message)

    def new_mesh(self, mesh_pb, client):
        with self.lock:
            mesh = Mesh(mesh_pb, client)
            self.meshes.append(mesh)
            # save_dir = config.MESHES_SAVE_DIR
            # save_path = os.path.join(save_dir, '{}_{}.bin'.format(
            #     client.ip, len(self.meshes)))
            # with open(save_path, 'wb') as f:
            #     f.write(mesh_pb.SerializeToString())

        self.send_to_websocket_clients(self.create_mesh_message(mesh.to_proto()))

        if mesh_pb.is_last:
            self.update_planes()
            self.update_targets(1)
            self.send_to_websocket_clients(self.create_game_state_message())
            self.send_to_hololens_clients(self.create_game_state_message())

    def clear_meshes(self):
        logger.info('Clearing meshes.')
        with self.lock:
            del self.meshes[:]

    def update_planes(self):
        y_coords = np.sort(np.vstack(
            [m.vertices for m in self.meshes])[:, 1])
        sigma = len(y_coords) / config.MESH_PLANE_FINDING_BINS
        self.floor, self.ceiling = find_planes(
            y_coords, config.MESH_PLANE_FINDING_BINS, sigma / 5)
        logger.info('Planes updates: floor={}, ceiling={}'.format(
            self.floor, self.ceiling))

    def update_targets(self, num_targets):
        self.target_pbs.clear()
        coords = np.sort(np.vstack([m.vertices for m in self.meshes]))

        is_near_floor = (coords[:, 1] - self.floor) < 0.1
        global_hull_mask, offsetx, offsetz = compute_hull_mask(
            coords[:, [0, 2]], coords)
        floor_hull_mask, _, _ = compute_hull_mask(
            coords[is_near_floor][:, [0, 2]], coords, remove_holes=False)
        sample_mask = global_hull_mask & ~floor_hull_mask
        cand_x, cand_z = np.where(sample_mask)

        for i in range(100):
            point_idx = random.randint(0, len(cand_x))
            x = cand_x[point_idx] / 100 + offsetx
            z = cand_z[point_idx] / 100 + offsetz
            y = self.floor + 0.15
            target_pb = pb.Target()
            target_pb.target_id = self.target_counter
            target_pb.position.x = x
            target_pb.position.y = y
            target_pb.position.z = z
            self.target_counter += 1
            self.target_pbs[target_pb.target_id] = target_pb

    def delete_target(self, target_id):
        logger.info('Deleting {} from {}'.format(
            target_id, self.target_pbs))
        if target_id in self.target_pbs:
            logger.info('Target {} deleted.'.format(target_id))
            del self.target_pbs[target_id]
            self.update_targets(1)
            self.send_to_websocket_clients(self.create_game_state_message())
            self.send_to_hololens_clients(self.create_game_state_message())

    def create_game_state_message(self):
        msg = pb.Message()
        msg.type = pb.Message.GAME_STATE
        msg.device_id = config.SERVER_DEVICE_ID
        msg.game_state.floor_y = self.floor
        msg.game_state.ceiling_y = self.ceiling
        msg.game_state.targets.extend(self.target_pbs.values())
        logger.info('Game state: {} targets'.format(len(self.target_pbs)))
        return msg

    def create_mesh_message(self, mesh_pb):
        msg = pb.Message()
        msg.type = pb.Message.MESH
        msg.device_id = config.SERVER_DEVICE_ID
        msg.mesh.MergeFrom(mesh_pb)
        return msg

    def create_ack(self):
        msg = pb.Message()
        msg.type = pb.Message.ACK
        return msg


game_state = GameState()
