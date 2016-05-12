import asyncio
from autobahn.asyncio.websocket import (WebSocketServerProtocol,
                                        WebSocketServerFactory)
from holoscanner import config, base_logger
from holoscanner.proto.holoscanner_pb2 import Message
from holoscanner import state
from holoscanner.state import game_state


logger = base_logger.getChild(__name__)


class RelayProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        logger.info("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        logger.info('WebSocket connection established.')

        with game_state.lock:
            for mesh_pb in game_state.mesh_pbs:
                self.send_message(state.create_mesh_message(mesh_pb))

        while True:
            msg = yield from game_state.message_queue.get()
            self.send_message(msg)

    @asyncio.coroutine
    def onMessage(self, payload, isBinary):
        if not isBinary:
            logger.info(payload.decode('utf8'))

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {0}".format(reason))

    def send_message(self, msg):
        msg_bytes = msg.SerializeToString()
        logger.info('Sending message ({} bytes).'.format(len(msg_bytes)))
        self.sendMessage(msg_bytes, isBinary=True)


def create_server_factory():
    factory = WebSocketServerFactory("ws://{}:{}".format(
        config.RELAY_LISTEN_ADDR, config.RELAY_LISTEN_PORT))
    factory.protocol = RelayProtocol
    return factory
