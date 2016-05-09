import os
import asyncio
import struct
from enum import Enum
from holoscanner import base_logger
from holoscanner.proto.holoscanner_pb2 import Message, Mesh
from holoscanner.state import GameState


logger = base_logger.getChild(__name__)
state = GameState()


HEADER_SIZE = 8
HEADER_FMT = 'Q'

class ServerState(Enum):
    WAITING = 1
    RECEIVING = 2


def save_mesh(mesh):
    print('Processing Mesh...')
    mesh_id = 0
    filedir = '/home/kpar/src/team8/holoscanner-server/meshes/'
    filename = 'mesh_{}.bin'.format(mesh_id)
    while os.path.exists(os.path.join(filedir, filename)):
        mesh_id += 1
        filename = 'mesh_{}.bin'.format(mesh_id)
    with open(os.path.join(filedir, filename), 'bw+') as f:
        f.write(mesh.SerializeToString())


class HsServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.state = ServerState.WAITING
        self.data = bytes()
        self.data_size = 0

    def make_ack(self):
        ack = Message()
        ack.type = Message.ACK
        ack.device_id = 1
        ack_bytes = ack.SerializeToString()
        return ack_bytes

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        logger.info('Connection from {}'.format(peername))
        self.transport = transport

    def handle_bytes(self, data):
        bytes_processed = 0
        if self.state == ServerState.WAITING:
            logger.info("Receiving new message...")
            header_bytes = data[:HEADER_SIZE]
            self.data_size = struct.unpack(HEADER_FMT, header_bytes)[0]
            self.state = ServerState.RECEIVING
            logger.info('Total message size is {}'.format(self.data_size))
            bytes_processed = HEADER_SIZE
        elif self.state == ServerState.RECEIVING:
            logger.info("Receiving message part...")
            logger.info('Data size {}'.format(len(data)))
            bytes_left = self.data_size - len(self.data)
            self.data += data[:bytes_left]
            bytes_processed += bytes_left

        if len(self.data) == self.data_size:
            msg = Message()
            msg.ParseFromString(self.data)
            logger.info('Received message of type {}'.format(msg.type))
            if msg.type == Message.MESH:
                logger.info('MESH RECEIVED')
                # save_mesh(msg.mesh)
                ack_bytes = self.make_ack()
                self.transport.write(struct.pack(HEADER_FMT, len(ack_bytes)))
                self.transport.write(ack_bytes)
            elif msg.type == Message.FIN:
                logger.info('Closing the client socket')
                self.transport.close()
            else:
                logger.error('Unknown message type {} received'.format(
                    msg.type))

            self.data = bytes()
            self.data_size = 0
            self.state = ServerState.WAITING

        return bytes_processed

    def data_received(self, data):
        bytes_processed = 0
        while bytes_processed < len(data):
            bytes_processed += self.handle_bytes(data[bytes_processed:])


class HsClientProtocol(asyncio.Protocol):

    def __init__(self, messages, loop):
        self.messages = messages
        self.loop = loop

    def connection_made(self, transport):
        logger.info('Sending {} messages'.format(len(self.messages)))
        for msg in self.messages:
            msg_bytes = msg.SerializeToString()
            header = struct.pack(HEADER_FMT, len(msg_bytes))
            transport.write(header)
            transport.write(msg_bytes)
            logger.info('{} bytes sent'.format(len(msg_bytes)))

        msg = Message()
        msg.type = Message.FIN
        msg_bytes = msg.SerializeToString()
        header = struct.pack(HEADER_FMT, len(msg_bytes))
        transport.write(header)
        transport.write(msg_bytes)


    def data_received(self, data):
        msg = Message()
        msg.ParseFromString(data)
        logger.info('Data received: type={}'.format(msg.type))

    def connection_lost(self, exc):
        logger.info('The server closed the connection')
        logger.info('Stop the event loop')
        self.loop.stop()



