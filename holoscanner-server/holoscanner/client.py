import os
import asyncio
from holoscanner.game_server import HsClientProtocol
from holoscanner.proto.holoscanner_pb2 import Message
from holoscanner import config, base_logger

from holoscanner.proto.holoscanner_pb2 import Vec3D, Mesh, Face


logger = base_logger.getChild(__name__)


def model_to_proto(model, mesh):
    vertices = model.vertices
    faces = model.faces

    for row in range(vertices.shape[0]):
        vec = Vec3D()
        vec.x = float(vertices[row, 0])
        vec.y = float(vertices[row, 1])
        vec.z = float(vertices[row, 2])
        mesh.vertices.extend([vec])
    for f in faces:
        face = Face()
        face.v1 = f['vertices'][0]
        face.v2 = f['vertices'][1]
        face.v3 = f['vertices'][2]
        mesh.faces.extend([face])

    return mesh


if __name__=='__main__':
    messages = []
    for filename in os.listdir(config.MESHES_DIR):
        filepath = os.path.join(config.MESHES_DIR, filename)

        msg = Message()
        msg.type = Message.MESH
        msg.device_id = 10
        with open(filepath, 'rb') as f:
            msg.mesh.ParseFromString(f.read())

        messages.append(msg)

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: HsClientProtocol(messages, loop),
                                  '127.0.0.1', 8888)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
