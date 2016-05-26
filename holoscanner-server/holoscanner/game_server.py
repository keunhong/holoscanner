import os
import asyncio
import struct
import threading
from enum import Enum
from holoscanner import base_logger
from holoscanner import proto
from holoscanner.proto.holoscanner_pb2 import Message
from holoscanner.state import game_state

logger = base_logger.getChild(__name__)

HEADER_SIZE = 8
HEADER_FMT = 'Q'


class ServerState(Enum):
    WAITING = 1
    RECEIVING = 2


def pack_message(message):
    msg_bytes = message.SerializeToString()
    header = struct.pack(HEADER_FMT, len(msg_bytes))

    return header + msg_bytes


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
        self.client_id = None
        self.send_lock = threading.RLock()

    def connection_made(self, transport):
        ip, port = transport.get_extra_info('peername')
        client_id = '{}:{}'.format(ip, port)
        self.transport = transport
        self.client_id = game_state.new_hololens_client(client_id, ip, self)
        logger.info('Hololense connection from {}:{}, '
                    'adding as client_id={}'.format(ip, port, self.client_id))

    def connection_lost(self, exc):
        game_state.remove_hololens_client(self.client_id)

    def handle_bytes(self, data):
        bytes_processed = 0
        if self.state == ServerState.WAITING:
            header_bytes = data[:HEADER_SIZE]
            self.data_size = struct.unpack(HEADER_FMT, header_bytes)[0]
            self.state = ServerState.RECEIVING
            bytes_processed = HEADER_SIZE
        elif self.state == ServerState.RECEIVING:
            logger.debug("Receiving message part...")
            logger.debug('Data size {}'.format(len(data)))
            bytes_left = self.data_size - len(self.data)
            self.data += data[:bytes_left]
            bytes_processed += bytes_left

        if len(self.data) == self.data_size:
            msg = Message()
            msg.ParseFromString(self.data)
            logger.debug('Received message of type {}, size {}'.format(
                msg.type, self.data_size))
            if msg.type == Message.MESH:
                game_state.new_mesh(self.client_id, msg.mesh)
                message = proto.create_ack()
                self.send_message(message)
            elif msg.type == Message.GAME_STATE_REQUEST:
                message = game_state.create_game_state_message(max_targets=1)
                self.send_message(message)
            elif msg.type == Message.FIN:
                logger.info('Closing the client gSocket')
                self.transport.close()
            elif msg.type == Message.TARGET_FOUND:
                logger.info('Target found: {}'.format(msg.target_id))
                game_state.target_found(self.client_id, msg.target_id)
            elif msg.type == Message.CLIENT_POSITION:
                game_state.client_position_updated(self.client_id,
                                                   msg.client_position)
            elif msg.type == Message.CLIENT_READY:
                game_state.client_ready(self.client_id)
            else:
                logger.error('Unknown message type {} received'.format(
                    msg.type))

            self.data = bytes()
            self.data_size = 0
            self.state = ServerState.WAITING

        return bytes_processed

    def send_message(self, message):
        with self.send_lock:
            bytes = pack_message(message)
            logger.debug('Sending message of type {} ({} bytes).'.format(
                message.type, len(bytes)))
            self.transport.write(bytes)

    def data_received(self, data):
        bytes_processed = 0
        while bytes_processed < len(data):
            bytes_processed += self.handle_bytes(data[bytes_processed:])


class HsClientProtocol(asyncio.Protocol):
    def __init__(self, messages, loop):
        self.messages = messages
        self.loop = loop

    def connection_made(self, transport):
        self.transport = transport
        logger.info('Sending {} messages'.format(len(self.messages)))
        for msg in self.messages:
            self.send_message(msg)

    def data_received(self, data):
        data = data[HEADER_SIZE:]
        msg = Message()
        msg.ParseFromString(data)
        logger.info('Data received: length={}, type={}'.format(
            len(data), msg.type))

        # if msg.type == Message.GAME_STATE:
        #     target_found_msg = Message()
        #     target_found_msg.type = Message.TARGET_FOUND
        #     target_found_msg.target_id = msg.game_state.gTargets[0].target_id
        #     print(target_found_msg)
        #     self.send_message(target_found_msg)

    def send_message(self, message):
        bytes = pack_message(message)
        logger.info('Sending message of type {} ({} bytes).'.format(
            message.type, len(bytes)))
        self.transport.write(bytes)

    def connection_lost(self, exc):
        logger.info('The server closed the connection')
        logger.info('Stop the event loop')
        self.loop.stop()
