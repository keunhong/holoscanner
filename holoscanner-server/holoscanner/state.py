import time
import os
import threading
import random
import socket
import numpy as np
from numpy import linalg
from collections import OrderedDict
from skimage import morphology
from scipy.misc import imsave, toimage

from holoscanner import config
from holoscanner import proto
from holoscanner.proto import holoscanner_pb2 as pb
from holoscanner import base_logger
from holoscanner import util

logger = base_logger.getChild(__name__)


class Mesh:
    def __init__(self, mesh_pb, is_last=False):
        self.nvertices = len(mesh_pb.vertices)
        self.nfaces = int(len(mesh_pb.triangles) / 3)
        self.vertices = np.ndarray((self.nvertices, 3), dtype=float)
        self.mesh_id = mesh_pb.mesh_id
        self.faces = np.array(mesh_pb.triangles, dtype=int)
        for i, vert_pb in enumerate(mesh_pb.vertices):
            self.vertices[i, :] = (vert_pb.x, vert_pb.y, vert_pb.z)

        if mesh_pb.cam_rotation:
            rotation_mat = util.quat_to_mat(mesh_pb.cam_rotation.x,
                                            mesh_pb.cam_rotation.y,
                                            mesh_pb.cam_rotation.z,
                                            mesh_pb.cam_rotation.w)
            self.vertices = rotation_mat.dot(self.vertices.T).T
            self.vertices[:, 0] += mesh_pb.cam_position.x
            self.vertices[:, 1] += mesh_pb.cam_position.y
            self.vertices[:, 2] += mesh_pb.cam_position.z

        self.normals = self._compute_normals()
        self.is_last = is_last

    def to_proto(self):
        mesh_pb = pb.Mesh()
        for i in range(self.nvertices):
            v = pb.Vec3D()
            v.x = self.vertices[i, 0]
            v.y = self.vertices[i, 1]
            v.z = self.vertices[i, 2]
            mesh_pb.vertices.extend([v])
        mesh_pb.triangles.extend(self.faces.tolist())
        mesh_pb.is_last = self.is_last
        return mesh_pb

    def _compute_normals(self):
        normals = np.zeros((self.nfaces, 3))
        for i in range(self.nfaces):
            v1 = self.vertices[self.faces[i * 3 + 0]]
            v2 = self.vertices[self.faces[i * 3 + 1]]
            v3 = self.vertices[self.faces[i * 3 + 2]]
            normal = np.cross(v1 - v2, v3 - v2)
            normal /= linalg.norm(normal)
            normals[i] = normal
        return normals

    def __repr__(self):
        return 'Mesh(nvertices={}, nfaces={})'.format(
            self.nvertices, self.nfaces)


class Client:
    def __init__(self, client_id, ip, protocol, nickname='Anonymous',
                 is_ready=False):
        self.client_id = client_id
        self.ip = ip
        self.score = 0
        self.protocol = protocol
        self.meshes = []
        self.is_ready = is_ready
        self.is_next_mesh_new = True
        self.nickname = nickname

    def send_message(self, message):
        self.protocol.send_message(message)

    def new_mesh(self, mesh):
        cleared = False
        if self.is_next_mesh_new:
            cleared = True
            self.clear_meshes()
            self.is_next_mesh_new = False

        if mesh.is_last:
            self.is_next_mesh_new = True

        self.meshes.append(mesh)

        return cleared

    def clear_meshes(self):
        logger.info('Clearing meshes for client {}'.format(self.client_id))
        del self.meshes[:]

    def to_proto(self):
        client_pb = pb.Client()
        client_pb.device_id = self.client_id
        client_pb.score = self.score
        client_pb.is_ready = self.is_ready
        client_pb.nickname = self.nickname
        return client_pb

    def __repr__(self):
        return 'Client(nickname={}, id={}, score={})'.format(
            self.nickname, self.client_id, self.score)


class GameState:
    clients = {
        config.SERVER_DEVICE_ID: Client(config.SERVER_DEVICE_ID,
                                        ip='127.0.0.1',
                                        protocol=None,
                                        nickname='Servy McServerface',
                                        is_ready=True)
    }

    clients_lock = threading.RLock()
    gs_lock = threading.RLock()
    listeners = []
    client_counter = 0

    floor = -5
    ceiling = 5
    target_counter = 1
    target_pbs = OrderedDict()

    def get_client(self, client_id):
        with self.clients_lock:
            return self.clients[client_id]

    def assign_name(self, client, hostname):
        device_name = hostname.split('.')[0]
        color = config.DEVICE_COLOR_MAP.get(device_name, config.DEFAULT_COLOR)
        client.nickname = color
        msg = pb.Message()
        msg.type = pb.Message.CLIENT_SET_NICKNAME
        msg.device_id = client.nickname
        client.send_message(msg)

    def new_hololens_client(self, client_id, ip, protocol):
        hostname = socket.gethostbyaddr(ip)[0]
        logger.info('Hololens client {} ({}) joined'.format(ip, hostname))
        with self.clients_lock:
            if client_id not in self.clients:
                self.clients[client_id] = Client(client_id, ip, protocol,
                                                 nickname=client_id)
                self.assign_name(self.clients[client_id], hostname)
                self.client_counter += 1
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
                if not client.client_id == config.SERVER_DEVICE_ID:
                    client.send_message(message)

    def check_end_game(self):
        for client in self.clients.values():
            if client.score >= 3 and client.client_id != config.SERVER_DEVICE_ID:
                logger.info('{} has won, GAME OVER.'.format(client.nickname))
                msg = pb.Message()
                msg.type = pb.Message.END_GAME
                msg.device_id = client.client_id
                self.send_to_hololens_clients(msg)
                self.send_to_websocket_clients(msg)
                return True
        return False

    def force_end_game(self):
        clients = list(self.clients.values())
        clients = [c for c in clients if c.client_id != '__server__']
        scores = [c.score for c in clients]
        winner = clients[np.argsort(scores)[-1]]
        logger.info('Forcing game end with {} (score={})'.format(
            winner.client_id, winner.score))
        msg = pb.Message()
        msg.type = pb.Message.END_GAME
        msg.device_id = winner.client_id
        self.send_to_hololens_clients(msg)
        self.send_to_websocket_clients(msg)

    def new_mesh(self, client_id, mesh_pb):
        with self.clients_lock:
            client = self.clients[client_id]

            filename = '{}_{}_{}.bin'.format(
                client_id, time.time(), len(client.meshes))
            with open(os.path.join(config.MESHES_SAVE_DIR, filename),
                      'wb') as f:
                bytes = mesh_pb.SerializeToString()
                f.write(bytes)

            mesh = Mesh(mesh_pb, mesh_pb.is_last)
            was_cleared = client.new_mesh(mesh)
            if was_cleared:
                logger.info('Starting to receive meshes from client {}'.format(
                    client_id))

        self.send_to_websocket_clients(
            proto.create_mesh_message(client_id, mesh.to_proto()))

        if mesh_pb.is_last:
            self.update_planes()
            self.update_targets(config.NUM_TARGETS_GEN)
            self.send_to_websocket_clients(self.create_game_state_message())

    def get_all_meshes(self):
        client_meshes = []
        with self.clients_lock:
            for client in self.clients.values():
                client_meshes.extend(client.meshes)
        return client_meshes

    def clear_meshes(self):
        logger.info('Clearing all meshes.')
        with self.clients_lock:
            for client in self.clients.values():
                client.clear_meshes()

    def clear_game_state(self):
        with self.gs_lock:
            self.target_pbs.clear()
            self.floor = -5
            self.ceiling = 5
        with self.clients_lock:
            for client in self.clients.values():
                client.score = 0
        self.send_to_websocket_clients(self.create_game_state_message())

    def update_planes(self):
        client_meshes = []
        for client in self.clients.values():
            client_meshes.extend(client.meshes)
        y_coords = np.sort(np.vstack(
            [m.vertices for m in client_meshes])[:, 1])
        sigma = len(y_coords) / config.MESH_PLANE_FINDING_BINS
        self.floor, self.ceiling = util.find_floor_and_ceiling(
            y_coords, config.MESH_PLANE_FINDING_BINS, sigma / 4)

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

    def update_targets(self, num_targets, keep_first=True, force=False):
        if not self.is_game_started():
            logger.info('Game has not started; skipping target generation.')
            return

        with self.gs_lock:
            first_target = None
            if keep_first and len(self.target_pbs) > 0:
                first_target = self.target_pbs.popitem(last=False)[1]
            self.target_pbs.clear()
            if first_target is not None:
                self.target_pbs[first_target.target_id] = first_target

        vertices, normals, faces = self.get_concatenated_meshes()
        if not force and vertices.shape[0] < 10:
            logger.info('Not computing targets: not enough mesh data.')
            return

        per_vertex_normals = util.compute_per_vertex_normals(
            vertices, normals, faces)

        # Global map computation.
        global_hull_mask, global_xmin, global_zmin, global_xmax, global_zmax = \
            util.compute_hull_mask(
                faces, vertices, remove_holes=True, closing=True)
        erosion_size = int(0.05 * min(global_hull_mask.shape))
        global_hull_mask = morphology.binary_erosion(
            global_hull_mask, selem=morphology.square(erosion_size))
        logger.debug('Eroding global mask by {}'.format(erosion_size))

        # Wall SDF computation.
        normal_mean_x, normal_mean_z, wall_xedges, wall_zedges = \
            util.compute_2d_normals(vertices, per_vertex_normals,
                                    self.floor, self.ceiling, global_hull_mask)
        wall_sdf = util.bfs_sdf(normal_mean_x, normal_mean_z)
        util.save_im(os.path.join(config.IMAGE_SAVE_DIR, 'wall_sdf.png'),
                     wall_sdf)
        logger.info('Wall SDF computed min={}, max={}'.format(
            wall_sdf.min(), wall_sdf.max()))
        if len(np.unique(wall_sdf)) <= 1:
            logger.warning('Wall SDF does not have enough values!'
                           'unique={}'.format(np.unique(wall_sdf)))
            wall_exclude_mask = np.zeros(wall_sdf.shape, dtype=np.bool)
        else:
            wall_exclude_mask = morphology.binary_dilation(
                wall_sdf <= 0, selem=morphology.square(erosion_size / 4))
        util.save_im(os.path.join(config.IMAGE_SAVE_DIR, 'wall_mask.png'),
                     wall_exclude_mask)

        # Floor/Ceiling hole detection.
        near_floor_inds = set(np.where(
            (vertices[:, 1] - self.floor) < 0.2)[0])
        near_ceiling_inds = set(np.where(
            (vertices[:, 1] - self.ceiling) < 0.2)[0])

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
        floor_hull_mask, _, _, _, _ = util.compute_hull_mask(
            floor_faces, vertices, remove_holes=False)
        floor_sample_mask = global_hull_mask & ~floor_hull_mask
        floor_cand_x, floor_cand_z = np.where(floor_sample_mask)

        ceiling_faces = np.array(ceiling_faces, dtype=np.uint32)
        ceiling_hull_mask, _, _, _, _ = util.compute_hull_mask(
            ceiling_faces, vertices, remove_holes=False)
        ceiling_sample_mask = global_hull_mask & ~ceiling_hull_mask
        ceiling_cand_x, ceiling_cand_z = np.where(ceiling_sample_mask)

        imsave(os.path.join(config.IMAGE_SAVE_DIR, 'global_map.png'),
               global_hull_mask)
        imsave(os.path.join(config.IMAGE_SAVE_DIR, 'floor_map.png'),
               floor_hull_mask)
        imsave(os.path.join(config.IMAGE_SAVE_DIR, 'floor_cand.png'),
               floor_sample_mask)
        imsave(os.path.join(config.IMAGE_SAVE_DIR, 'ceiling_map.png'),
               ceiling_hull_mask)
        imsave(os.path.join(config.IMAGE_SAVE_DIR, 'ceiling_cand.png'),
               ceiling_sample_mask)

        with self.gs_lock:
            target_count = len(self.target_pbs)
            iters = 0
            while target_count < num_targets and iters < 1000:
                iters += 1
                # Randomly generate on ceiling or floor.
                is_floor = random.random() < 0.5
                if is_floor and len(floor_cand_x) > 0:
                    point_idx = random.randint(0, len(floor_cand_x) - 1)
                    x = floor_cand_x[
                            point_idx] / config.HULL_SCALE + global_xmin
                    z = floor_cand_z[
                            point_idx] / config.HULL_SCALE + global_zmin
                    y = self.floor + 0.15
                elif not is_floor and len(ceiling_cand_x) > 0:
                    point_idx = random.randint(0, len(ceiling_cand_x) - 1)
                    x = ceiling_cand_x[
                            point_idx] / config.HULL_SCALE + global_xmin
                    z = ceiling_cand_z[
                            point_idx] / config.HULL_SCALE + global_zmin
                    y = self.ceiling - 0.15
                else:
                    continue

                xind = max(0, min(np.searchsorted(wall_xedges, x),
                                  len(wall_xedges) - 2))
                zind = max(0, min(np.searchsorted(wall_zedges, z),
                                  len(wall_zedges) - 2))
                if wall_exclude_mask[xind, zind]:
                    continue

                target_pb = pb.Target()
                target_pb.target_id = self.target_counter
                target_pb.position.x = x
                target_pb.position.y = y
                target_pb.position.z = z
                self.target_counter += 1
                self.target_pbs[target_pb.target_id] = target_pb
                target_count += 1

        if target_count == 0:
            logger.info('Could not generate more targets, ending game!')
            self.force_end_game()

        logger.info('Generated {} targets for a total of {}.'.format(
            target_count, len(self.target_pbs)))

    def target_found(self, client_id, target_id):
        logger.info('Deleting target_id={} ({} targets exist)'.format(
            target_id, len(self.target_pbs)))
        if target_id in self.target_pbs:
            old_target = self.target_pbs[target_id]

            def comparator(item):
                _, target = item
                o = old_target.position
                t = target.position
                return (o.x - t.x) ** 2 + (o.y - t.y) ** 2 + (o.z - t.z) ** 2

            self.clients[client_id].score += 1
            logger.info('Client {} found target_id={}, score={}'.format(
                client_id, target_id, self.clients[client_id].score))
            del self.target_pbs[target_id]
            sorted_items = sorted(self.target_pbs.items(),
                                  key=comparator,
                                  reverse=True)
            if len(sorted_items) >= 7:
                divide_idx = int(5 * len(sorted_items) / 7)
                half_1 = sorted_items[:divide_idx]
                half_2 = sorted_items[divide_idx:]
                random.shuffle(half_1)
                sorted_items = half_1 + half_2
            self.target_pbs = OrderedDict(sorted_items)
            if len(self.target_pbs) == 0:
                self.update_targets(config.NUM_TARGETS_GEN)
            self.game_state_summary()

        self.send_to_websocket_clients(self.create_game_state_message())

        if not self.check_end_game():
            self.send_to_hololens_clients(
                self.create_game_state_message(max_targets=1))


    def client_position_updated(self, client_id, client_position_pb):
        msg = pb.Message()
        msg.device_id = client_id
        msg.type = pb.Message.CLIENT_POSITION
        msg.client_position.MergeFrom(client_position_pb)
        self.send_to_websocket_clients(msg)

    def client_ready(self, client_id):
        if client_id not in self.clients:
            logger.warning(
                'Client {} is ready but is not in game state.'.format(
                    client_id))
            return

        logger.info('Client {} is ready!'.format(client_id))
        self.clients[client_id].is_ready = True

        if self.is_game_started():
            logger.info('All clients ready: GAME HAS STARTED!')
            self.update_targets(config.NUM_TARGETS_GEN)
            self.send_to_hololens_clients(proto.create_game_started_message())
            self.send_to_hololens_clients(
                self.create_game_state_message(max_targets=1))
            self.send_to_websocket_clients(self.create_game_state_message())

    def is_game_started(self):
        is_started = True
        for client_id, client in self.clients.items():
            if client_id != config.SERVER_DEVICE_ID:
                is_started &= client.is_ready
        return is_started

    def create_game_state_message(self, max_targets=1):
        with self.gs_lock:
            msg = pb.Message()
            msg.type = pb.Message.GAME_STATE
            msg.device_id = config.SERVER_DEVICE_ID
            msg.game_state.floor_y = self.floor
            msg.game_state.ceiling_y = self.ceiling
            targets = list(self.target_pbs.values())
            if max_targets is not None:
                targets = [t for t in targets[:min(max_targets, len(targets))]]
            msg.game_state.targets.extend(targets)
            msg.game_state.clients.extend(
                [c.to_proto() for c in self.clients.values()])
            # if max_targets is not None:
            #     logger.info(msg.game_state)
            return msg

    def game_state_summary(self):
        return """
=============
State Summary
=============
Clients   : {}
# Targets : {}
Floor     : {}
Ceiling   : {}

""".format(list(self.clients.values()), len(self.target_pbs),
           self.floor, self.ceiling)


game_state = GameState()
