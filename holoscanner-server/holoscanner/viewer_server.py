import asyncio
from autobahn.asyncio.websocket import (WebSocketServerProtocol,
                                        WebSocketServerFactory)
from holoscanner import config, base_logger
from holoscanner.proto.holoscanner_pb2 import Message
from holoscanner.state import game_state

logger = base_logger.getChild(__name__)


class RelayProtocol(WebSocketServerProtocol):
    def __init__(self):
        super().__init__()
        self.message_queue = asyncio.Queue()
        game_state.new_websocket_client(self.message_queue)

    def onConnect(self, request):
        logger.info("New WebSocket connection: {0}".format(request.peer))

    def onOpen(self):
        logger.info('WebSocket connection established.')

        with game_state.gs_lock:
            self.send_message(game_state.create_game_state_message())
            for mesh in game_state.meshes:
                self.send_message(game_state.create_mesh_message(mesh.to_proto()))
            self.send_message(game_state.create_game_state_message())

        while True:
            msg = yield from self.message_queue.get()
            self.send_message(msg)

    @asyncio.coroutine
    def onMessage(self, payload, isBinary):
        if not isBinary:
            logger.info('Not Binary {}'.format(payload.decode('utf8')))
        message = Message()
        message.ParseFromString(payload)
        if message.type == Message.CLEAR_MESHES:
            game_state.clear_meshes()

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {0}".format(reason))
        game_state.listeners.remove(self.message_queue)

    def send_message(self, msg):
        msg_bytes = msg.SerializeToString()
        # logger.info('Sending message ({} bytes).'.format(len(msg_bytes)))
        self.sendMessage(msg_bytes, isBinary=True)


def create_server_factory():
    factory = WebSocketServerFactory("ws://{}:{}".format(
        config.RELAY_LISTEN_ADDR, config.RELAY_LISTEN_PORT))
    factory.protocol = RelayProtocol
    return factory
