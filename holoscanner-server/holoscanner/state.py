import threading
import random
import numpy as np
from collections import OrderedDict
from scipy.signal import argrelextrema
from scipy.ndimage.filters import gaussian_filter1d
from PIL import Image, ImageDraw
from skimage import morphology
from scipy.misc import imsave

from holoscanner import config
from holoscanner.proto import holoscanner_pb2 as pb
from holoscanner import base_logger

logger = base_logger.getChild(__name__)


def find_floor_and_ceiling(y_coords, nbins, sigma=None):
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


def compute_hull_mask(faces, vertices, scale=100,
                      remove_holes=True, closing=False):
    transformed = vertices.copy()
    transformed[:, 0] -= vertices[:, 0].min()
    transformed[:, 2] -= vertices[:, 2].min()
    offsetx = vertices[:, 0].min()
    offsety = vertices[:, 2].min()
    width = int(round(vertices[:, 0].max() - vertices[:, 0].min()) * scale) + 1
    height = int(round(vertices[:, 2].max() - vertices[:, 2].min()) * scale) + 1

    im = Image.new('L', (width, height))
    draw = ImageDraw.Draw(im)
    for face in faces:
        p = [(int(transformed[i, 0] * scale), int(transformed[i, 2] * scale)) for i
             in face]
        draw.polygon(p, fill='#fff')

    im = np.array(im) == 255
    if closing:
        im = morphology.binary_closing(im, morphology.square(40))
    if remove_holes:
        im = morphology.remove_small_holes(im, min_size=scale ** 2)
    return im.T, offsetx, offsety


class Mesh:
    def __init__(self, mesh_pb):
        self.nvertices = len(mesh_pb.vertices)
        self.nfaces = int(len(mesh_pb.triangles) / 3)
        self.vertices = np.ndarray((self.nvertices, 3), dtype=float)
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

        self.normals = self._compute_normals()

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

    def _compute_normals(self):
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
    def __init__(self, client_id, ip, protocol):
        self.client_id = client_id
        self.ip = ip
        self.score = 0
        self.protocol = protocol
        self.meshes = []
        self.is_next_mesh_new = True

    def send_message(self, message):
        self.protocol.send_message(message)

    def new_mesh(self, mesh, is_last):
        if self.is_next_mesh_new:
            self.clear_meshes()
            self.is_next_mesh_new = False

        if is_last:
            self.is_next_mesh_new = True

        self.meshes.append(mesh)

    def clear_meshes(self):
        logger.info('Clearing meshes for client {}'.format(self.client_id))
        del self.meshes[:]

    def to_proto(self):
        client_pb = pb.Client()
        client_pb.device_id = self.client_id
        client_pb.score = self.score
        return client_pb


class GameState:

    clients = {
        '__server__': Client('__server__', '127.0.0.1', None)
    }

    clients_lock = threading.RLock()
    gs_lock = threading.RLock()
    listeners = []

    floor = -5
    ceiling = 5
    target_counter = 0
    target_pbs = OrderedDict()

    def new_hololens_client(self, client_id, ip, protocol):
        logger.info('Hololens client {} joined'.format(ip))
        with self.clients_lock:
            if client_id not in self.clients:
                self.clients[client_id] = Client(client_id, ip, protocol)
        self.send_to_websocket_clients(self.create_game_state_message())
        return client_id

    def new_websocket_client(self, queue):
        self.listeners.append(queue)

    def remove_hololens_client(self, client_id):
        logger.info('Hololens client {} left.'.format(client_id))
        with self.clients_lock:
            if client_id in self.clients:
                del self.clients[client_id]
        self.send_to_websocket_clients(self.create_game_state_message())

    def send_to_websocket_clients(self, message):
        for queue in self.listeners:
            queue.put_nowait(message)

    def send_to_hololens_clients(self, message):
        with self.clients_lock:
            for client in self.clients.values():
                if not client.client_id == '__server__':
                    client.send_message(message)

    def new_mesh(self, client_id, mesh_pb):
        with self.clients_lock:
            client = self.clients[client_id]
            mesh = Mesh(mesh_pb)
            client.new_mesh(mesh, mesh_pb.is_last)
        self.send_to_websocket_clients(self.create_mesh_message(mesh.to_proto()))

        if mesh_pb.is_last:
            self.update_planes()
            self.update_targets(100)
            self.send_to_websocket_clients(self.create_game_state_message())

    def get_all_meshes(self):
        client_meshes = []
        with self.clients_lock:
            for client in self.clients.values():
                client_meshes.extend(client.meshes)
        return client_meshes

    def clear_meshes(self):
        logger.info('Clearing meshes.')
        with self.clients_lock:
            for client in self.clients.values():
                client.clear_meshes()

    def clear_game_state(self):
        with self.gs_lock:
            self.target_pbs.clear()
            self.floor = -5
            self.ceiling = 5
        self.send_to_websocket_clients(self.create_game_state_message())

    def update_planes(self):
        client_meshes = []
        for client in self.clients.values():
            client_meshes.extend(client.meshes)
        y_coords = np.sort(np.vstack(
            [m.vertices for m in client_meshes])[:, 1])
        sigma = len(y_coords) / config.MESH_PLANE_FINDING_BINS
        self.floor, self.ceiling = find_floor_and_ceiling(
            y_coords, config.MESH_PLANE_FINDING_BINS, sigma / 3)
        logger.info('Planes updates: floor={}, ceiling={}'.format(
            self.floor, self.ceiling))

    def get_concatenated_meshes(self):
        vertices = []
        normals = []
        faces = []
        base_index = 0
        with self.clients_lock:
            for mesh in self.get_all_meshes():
                vertices.extend([vertex for vertex in mesh.vertices])
                normals.extend([normal for normal in mesh.normals])
                faces.extend([[mesh.faces[3 * i] + base_index,
                               mesh.faces[3 * i + 1] + base_index,
                               mesh.faces[3 * i + 2] + base_index]
                              for i in range(mesh.nfaces)])
                base_index = len(vertices)
        vertices = np.array(vertices)
        normals = np.array(normals)
        faces = np.array(faces, dtype=np.uint32)
        return vertices, normals, faces

    def update_targets(self, num_targets):
        with self.gs_lock:
            self.target_pbs.clear()

        vertices, normals, faces = self.get_concatenated_meshes()

        global_hull_mask, offsetx, offsetz = compute_hull_mask(
            faces, vertices, remove_holes=True, closing=True)
        erosion_size = 0.04 * min(global_hull_mask.shape)
        global_hull_mask = morphology.binary_erosion(global_hull_mask,
                                  selem=morphology.square(erosion_size))
        logger.info('Eroding global mask by {}'.format(erosion_size))

        near_floor_inds = np.where((vertices[:, 1] - self.floor) < 0.2)[0]
        near_ceiling_inds = np.where((vertices[:, 1] - self.ceiling) < 0.2)[0]

        floor_faces = []
        ceiling_faces = []
        for face in faces:
            if (face[0] in near_floor_inds or
                    face[1] in near_floor_inds or
                    face[2] in near_floor_inds):
                floor_faces.append(face)
            if (face[0] in near_ceiling_inds or
                        face[1] in near_ceiling_inds or
                        face[2] in near_ceiling_inds):
                ceiling_faces.append(face)

        floor_faces = np.array(floor_faces, dtype=np.uint32)
        floor_hull_mask, _, _ = compute_hull_mask(
            floor_faces, vertices, remove_holes=False)
        floor_sample_mask = global_hull_mask & ~floor_hull_mask
        floor_cand_x, floor_cand_z = np.where(floor_sample_mask)

        ceiling_faces = np.array(ceiling_faces, dtype=np.uint32)
        ceiling_hull_mask, _, _ = compute_hull_mask(
            ceiling_faces, vertices, remove_holes=False)
        ceiling_sample_mask = global_hull_mask & ~ceiling_hull_mask
        ceiling_cand_x, ceiling_cand_z = np.where(ceiling_sample_mask)

        imsave('/home/kpar/www/global_map.png', global_hull_mask)
        imsave('/home/kpar/www/floor_map.png', floor_hull_mask)
        imsave('/home/kpar/www/floor_cand.png', floor_sample_mask)
        imsave('/home/kpar/www/ceiling_map.png', ceiling_hull_mask)
        imsave('/home/kpar/www/ceiling_cand.png', ceiling_sample_mask)

        with self.gs_lock:
            for i in range(num_targets):
                # Randomly generate on ceiling or floor.
                if random.random() < 0.5:
                    point_idx = random.randint(0, len(floor_cand_x))
                    x = floor_cand_x[point_idx] / 100 + offsetx
                    z = floor_cand_z[point_idx] / 100 + offsetz
                    y = self.floor + 0.15
                else:
                    point_idx = random.randint(0, len(ceiling_cand_x))
                    x = ceiling_cand_x[point_idx] / 100 + offsetx
                    z = ceiling_cand_z[point_idx] / 100 + offsetz
                    y = self.ceiling - 0.15
                target_pb = pb.Target()
                target_pb.target_id = self.target_counter
                target_pb.position.x = x
                target_pb.position.y = y
                target_pb.position.z = z
                self.target_counter += 1
                self.target_pbs[target_pb.target_id] = target_pb

        logger.info('Generated {} targets.'.format(len(self.target_pbs)))

    def target_found(self, client_id, target_id):
        logger.info('Deleting target_id={} ({} targets exist)'.format(
            target_id, len(self.target_pbs)))
        if target_id in self.target_pbs:
            old_target = self.target_pbs[target_id]

            def comparator(item):
                _, target = item
                return np.linalg.norm(
                    np.array([old_target.position.x,
                              old_target.position.y,
                              old_target.position.z]) -
                    np.array([target.position.x,
                              target.position.y,
                              target.position.z]))
            self.clients[client_id].score += 1
            logger.info('Client {} found target_id={}, score={}'.format(
                client_id, target_id, self.clients[client_id].score))
            del self.target_pbs[target_id]
            self.target_pbs = OrderedDict(sorted(self.target_pbs.items(),
                                                 key=comparator,
                                                 reverse=True))
            if len(self.target_pbs) == 0:
                self.update_targets(100)
            self.send_to_websocket_clients(self.create_game_state_message())
            self.send_to_hololens_clients(
                self.create_game_state_message(max_targets=1))

    def create_game_state_message(self, max_targets=None):
        with self.gs_lock:
            msg = pb.Message()
            msg.type = pb.Message.GAME_STATE
            msg.device_id = config.SERVER_DEVICE_ID
            msg.game_state.floor_y = self.floor
            msg.game_state.ceiling_y = self.ceiling
            targets = list(self.target_pbs.items())
            if max_targets is not None:
                targets = [t[1] for t in targets[:min(max_targets, len(targets))]]
            else:
                targets = [t[1] for t in targets]
            msg.game_state.targets.extend(targets)
            msg.game_state.clients.extend(
                [c.to_proto() for c in self.clients.values()])
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
