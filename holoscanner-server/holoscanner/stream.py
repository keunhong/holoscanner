import asyncio
from asyncio import streams
import struct
from holoscanner import base_logger
from holoscanner.proto.holoscanner_pb2 import Message, Mesh


logger = base_logger.getChild(__name__)


HEADER_SIZE = 8
HEADER_FMT = 'Q'


class HsServerProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        header_bytes = data[:HEADER_SIZE]
        msg_bytes = data[HEADER_SIZE:]
        header = struct.unpack(HEADER_FMT, header_bytes)
        msg = Message()
        msg.ParseFromString(msg_bytes)
        print('Received {}'.format(msg))

        ack = Message()
        ack.type = Message.ACK
        ack.device_id = 1
        ack_bytes = ack.SerializeToString()
        self.transport.write(struct.pack(HEADER_FMT, len(ack_bytes)))
        self.transport.write(ack_bytes)

        print('Close the client socket')
        self.transport.close()


class HsClientProtocol(asyncio.Protocol):

    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        print('Sending: {}'.format(self.message))
        msg_bytes = self.message.SerializeToString()
        header = struct.pack(HEADER_FMT, len(msg_bytes))
        transport.write(header)
        transport.write(msg_bytes)
        print('Data sent')

    def data_received(self, data):
        msg = Message()
        msg.ParseFromString(data)
        print('Data received: {!r}'.format(msg))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


# def _hs_decode_message(msg):
#     header =


# class HsStreamReader(streams.StreamReader):
#     @asyncio.coroutine
#     def read_msg(self):
#         header = yield from self.readexactly(HEADER_SIZE)
#         header = struct.unpack(HEADER_FMT, header)
#         print(header)
#         # msg_type, msg_length = unpack header
#         data = yield from self.readexactly(msg_length)


from holoscanner.proto.holoscanner_pb2 import Vec3D, Mesh, Face

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

